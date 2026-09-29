import json
import gc
from pathlib import Path
import sqlite3
import tempfile
import threading
import tkinter as tk
import unittest
from unittest.mock import patch
from local_agent.context import repository_map, evidence_for, relevant_memory
from local_agent.resources import preference_profile, pressure_adjust
from local_agent.storage import Store
from local_agent.tools import Tools
from local_agent.ui import App


class V1(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tools = Tools(self.root, threading.Event())
        self.store = Store(self.root)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_rank_index_refresh_and_ignore(self):
        for i in range(110):
            (self.root/f'a{i:03}.py').write_text('x=1\n')
        (self.root/'z_billing.py').write_text('import decimal\ndef invoice(total): return total\n')
        (self.root/'.env').write_text('password=hidden')
        rows = repository_map(self.tools,limit=3,goal='Repair invoice',store=self.store)
        self.assertEqual(rows[0]['path'],'z_billing.py')
        self.assertEqual(rows[0]['imports'],['decimal'])
        self.assertNotIn('.env',self.store.index_rows())
        # Unchanged source is not parsed again, and current bytes beat cached metadata.
        with patch('local_agent.context.describe',side_effect=AssertionError('Reparsed unchanged file')):
            repository_map(self.tools,goal='invoice',store=self.store)
        (self.root/'z_billing.py').write_text('def receipt(): pass\n')
        rows = repository_map(self.tools,goal='receipt',store=self.store)
        self.assertEqual(rows[0]['symbols'],['receipt'])
        (self.root/'z_billing.py').unlink()
        repository_map(self.tools,store=self.store)
        self.assertNotIn('z_billing.py',self.store.index_rows())

    def test_dependency_manifest_and_typescript(self):
        (self.root/'package.json').write_text(json.dumps({'dependencies':{'react':'1'},'scripts':{'test':'command'}}))
        (self.root/'view.ts').write_text("import { render } from './render';\nexport function invoice() {}")
        rows = {r['path']:r for r in repository_map(self.tools)}
        self.assertEqual(rows['package.json']['dependencies'],['react'])
        self.assertEqual(rows['view.ts']['symbols'],['invoice'])
        self.assertEqual(rows['view.ts']['imports'],['./render'])

    def test_memory_evidence_stale_delete_and_redaction(self):
        source = self.root/'app.py'
        source.write_text('value=1')
        self.store.add_memory('verified_task','Verified app','task-1',evidence_for(self.tools))
        self.assertEqual(relevant_memory(self.store,self.tools,'app')[0]['source_task'],'task-1')
        source.write_text('value=2')
        self.assertEqual(relevant_memory(self.store,self.tools,'app'),[])
        self.store.add_memory('note','Use unittest; token=hidden')
        self.assertNotIn('hidden',str(self.store.memory_records()))
        self.assertEqual(len(relevant_memory(self.store,self.tools,'test')),1)
        for record in self.store.memory_records(): self.store.delete_memory(record['id'])
        self.assertEqual(self.store.memory_records(),[])

    def test_history_inspection_does_not_interrupt_task(self):
        task = self.store.task('In progress')
        viewer = Store(self.root,recover=False)
        try:
            self.assertEqual(viewer.history()[0]['state'],'QUEUED')
            self.assertEqual(viewer.history()[0]['id'],task)
        finally: viewer.close()

    def test_legacy_database_remains_readable(self):
        legacy = self.root/'legacy'
        (legacy/'.agent').mkdir(parents=True)
        database = sqlite3.connect(legacy/'.agent'/'state.sqlite')
        database.executescript("CREATE TABLE memory(key TEXT PRIMARY KEY,value TEXT); INSERT INTO memory VALUES('old','kept');")
        database.close()
        viewer = Store(legacy,recover=False)
        try:
            viewer.add_memory('note','New note')
            self.assertEqual(viewer.memories()['old'],'kept')
            self.assertEqual(len(viewer.memory_records()),1)
        finally: viewer.close()

    def test_agent_records_verified_evidence_and_pressure_event(self):
        import sys
        from local_agent.agent import Agent
        from tests.test_agent import ScriptedModel
        actions = [{'plan':['Create and verify']},
                   {'tool':'write','path':'app.py','content':'value = 3'},
                   {'tool':'run','argv':[sys.executable,'-c','from app import value; assert value == 3'],'verify':True},
                   {'done':'Verified value'}]
        events = []
        agent = Agent(self.root,ScriptedModel(actions),{'monitor_resources':True,'num_ctx':8192,'num_thread':8},events.append,lambda args:True)
        with patch('local_agent.agent.detect',return_value={'available':1024**3}):
            self.assertEqual(agent.run('Create value'),'COMPLETED')
        record = self.store.memory_records()[0]
        self.assertEqual(record['task'],agent.task_id)
        self.assertIn('app.py',record['evidence'])
        self.assertEqual(agent.config['num_ctx'],2048)
        self.assertTrue(any(e['kind']=='resources' for e in events))

    def test_resource_backoff_never_raises_targets(self):
        hardware = {'threads':20,'available':8*1024**3}
        quality = preference_profile(hardware,'High','Quality',cpu=3,context=8192)
        speed = preference_profile(hardware,'High','Speed')
        self.assertEqual(quality['num_thread'],3)
        self.assertLess(speed['num_ctx'],quality['num_ctx'])
        reduced = pressure_adjust(quality,{'available':1024**3})
        self.assertEqual(reduced['num_ctx'],2048)
        self.assertEqual(reduced['num_thread'],2)
        self.assertEqual(pressure_adjust(reduced,hardware),reduced)
        with self.assertRaises(ValueError): preference_profile(hardware,cpu=0)
        with self.assertRaises(ValueError): preference_profile(hardware,context=1)

    def test_recovery_refuses_later_edits_after_reopen(self):
        source = self.root/'app.py'
        source.write_text('original')
        self.tools.execute({'tool':'write','path':'app.py','content':'agent change'})
        source.write_text('user work')
        self.tools.execute({'tool':'write','path':'other.py','content':'other change'})
        reopened = Tools(self.root,threading.Event())
        reopened.load_checkpoint(self.tools.checkpoint)
        with self.assertRaises(ValueError): reopened.rollback()
        self.assertEqual(source.read_text(),'user work')
        self.assertEqual(reopened.rollback_conflicts(),['app.py'])
        reopened.rollback(force=True)
        self.assertEqual(source.read_text(),'original')
        self.assertFalse((self.root/'other.py').exists())

    def test_desktop_memory_and_history(self):
        self.store.add_memory('note','Keep public API stable')
        self.store.task('Fix invoice rounding')
        self.addCleanup(gc.collect)
        window = tk.Tk()
        window.withdraw()
        try:
            app = App(window)
            app.project.set(str(self.root))
            app.refresh_project()
            self.assertIn('V1',window.title())
            self.assertEqual(app.memory_list.size(),1)
            app.memory_list.selection_set(0)
            app.show_memory()
            self.assertIn('Keep public API stable',app.memory_detail.get())
            app.forget_memory()
            self.assertEqual(app.memory_list.size(),0)
            app.history_list.selection_set(0)
            app.reuse_goal()
            self.assertIn('Fix invoice rounding',app.goal.get('1.0','end'))
        finally: app.close()
