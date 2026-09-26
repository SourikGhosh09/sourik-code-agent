"""Policy behavior and integration tests; no real model is used here."""
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

from local_agent.agent import Agent
from local_agent.context import repository_map
from local_agent.simplicity import SimplicityEngine, dependencies, installation
from local_agent.tools import Tools
from tests.test_agent import ScriptedModel


class SimplicityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tools = Tools(self.root,threading.Event())

    def tearDown(self):
        self.temp.cleanup()

    def engine(self):
        return SimplicityEngine(self.tools,repository_map(self.tools))

    def test_reuse_candidates_and_caller_search(self):
        (self.root/'existing.py').write_text('def normalize(value): return value.strip()\n')
        (self.root/'caller.py').write_text('from existing import normalize\nnormalize("a")\n')
        engine = self.engine()
        evidence = engine.inspect('Fix normalize')
        matches = next(item['matches'] for item in evidence if 'matches' in item)
        self.assertIn('caller.py',{m['path'] for m in matches})
        action = {'tool':'write','path':'copy.py','content':'def normalize(value): return value.strip()\n'}
        decision = engine.before(action)
        self.assertTrue(decision['reconsider'])
        self.assertIn('existing.py',str(decision))
        self.assertFalse((self.root/'copy.py').exists())

    def test_dependency_gate_allows_justified_need_but_not_permission(self):
        engine = self.engine()
        action = {'tool':'run','argv':['python','-m','pip','install','example']}
        self.assertTrue(engine.before(action)['reconsider'])
        action['simplicity'] = 'The requested protocol is provided by this package; existing/native APIs lack it.'
        self.assertFalse(engine.before(action)['reconsider'])
        with self.assertRaises(PermissionError): self.tools.execute(action)
        self.assertTrue(installation(['uv','add','example']))
        self.assertFalse(installation(['python','-m','unittest','discover']))

    def test_manifests_distinguish_existing_and_new_dependencies(self):
        (self.root/'package.json').write_text('{"dependencies":{"react":"1"},"devDependencies":{"test":"1"}}')
        engine = self.engine()
        engine.inspect()
        action = {'tool':'write','path':'package.json','content':'{"dependencies":{"react":"2"},"devDependencies":{"test":"1"}}'}
        self.assertIsNone(engine.before(action))
        action['content'] = '{"dependencies":{"react":"2","extra":"1"}}'
        self.assertTrue(engine.before(action)['reconsider'])
        self.assertEqual(dependencies('pyproject.toml','[project]\ndependencies=["requests>=2"]\n[project.optional-dependencies]\ntest=["pytest"]'),{'requests','pytest'})
        self.assertEqual(dependencies('requirements.txt','# comment\nrequests>=2\n'),{'requests'})

    def test_legitimate_large_change_can_replan_or_explain(self):
        engine = self.engine()
        engine.plan({'change_budget':{'files':0,'new_files':0,'dependencies':0,'complexity':'check only'}})
        action = {'tool':'write','path':'worker_manager.py','content':'class WorkerManager: pass'}
        self.assertTrue(engine.before(action)['reconsider'])
        action['simplicity'] = 'User requested concurrent workers with shared cancellation ownership.'
        self.assertFalse(engine.before(action)['reconsider'])
        engine.plan({'change_budget':{'files':20,'new_files':10,'dependencies':2,'complexity':'Requested multi-file feature'}})
        self.assertIsNone(engine.before({'tool':'write','path':'feature.py','content':'value=1'}))
        with self.assertRaises(ValueError): engine.plan({'change_budget':{'files':-1}})

    def test_unread_file_requires_evidence_before_modification(self):
        (self.root/'original.py').write_text('value=1')
        engine = self.engine()
        action = {'tool':'patch','path':'original.py','old':'1','new':'2'}
        decision = engine.before(action)
        self.assertTrue(decision['reconsider'])
        self.assertEqual(decision['evidence']['content'],'value=1')
        self.assertIsNone(engine.before(action))

    def test_diff_counts_actual_changes_and_preserves_prior_work(self):
        (self.root/'original.py').write_text('user_change=1')
        engine = self.engine()
        self.tools.snapshot('original.py')  # test commands checkpoint unchanged files too
        self.tools.execute({'tool':'write','path':'new.py','content':'value=2'})
        report = engine.review()
        self.assertEqual(report['counts']['files'],1)
        self.assertEqual(report['files'],['new.py'])
        self.assertNotIn('user_change',report['diff'])
        self.assertEqual((self.root/'original.py').read_text(),'user_change=1')

    def test_inspection_never_reads_secrets_or_runs_commands(self):
        (self.root/'.env').write_text('SECRET=private')
        (self.root/'app.py').write_text('token=private\n')
        engine = self.engine()
        evidence = engine.inspect()
        self.assertNotIn('private',str(evidence))
        self.assertNotIn('.env',str(evidence))
        with self.assertRaises(PermissionError):
            engine.before({'tool':'write','path':'../outside.py','content':'x=1'})

    def test_no_change_task_still_verifies_and_reviews(self):
        (self.root/'app.py').write_text('value=3')
        actions = [{'plan':['Verify existing value']},
                   {'tool':'run','argv':[sys.executable,'-c','from app import value; assert value == 3'],'verify':True},
                   {'done':'Already implemented; no changes needed.'}]
        events = []
        model = ScriptedModel(actions)
        agent = Agent(self.root,model,{},events.append,lambda args:True)
        self.assertEqual(agent.run('Ensure value equals 3'),'COMPLETED')
        reviews = [e['data'] for e in events if e['kind']=='simplicity' and e['data']['phase']=='review']
        self.assertEqual(reviews[-1]['counts']['files'],0)
        self.assertEqual((self.root/'app.py').read_text(),'value=3')

    def test_final_diff_is_present_in_model_context(self):
        class InspectingModel(ScriptedModel):
            def generate(inner,messages,config):
                action = super(InspectingModel,inner).generate(messages,config)
                if 'done' in action:
                    self.assertIn('simplicity_review',messages[-1]['content'])
                    self.assertIn('after/app.py',messages[-1]['content'])
                return action
        actions = [{'plan':['Implement value']}, {'tool':'write','path':'app.py','content':'value=3'},
                   {'tool':'run','argv':[sys.executable,'-c','from app import value; assert value == 3'],'verify':True},
                   {'done':'Verified'}]
        agent = Agent(self.root,InspectingModel(actions),{},approve=lambda args:True)
        self.assertEqual(agent.run('Create value'),'COMPLETED')

    def test_gate_does_not_execute_until_explanation(self):
        actions = [{'plan':['Add required worker management']},
                   {'tool':'write','path':'worker_manager.py','content':'value=3'},
                   {'tool':'write','path':'worker_manager.py','content':'value=3','simplicity':'User explicitly requested this existing architecture boundary.'},
                   {'tool':'run','argv':[sys.executable,'-c','from worker_manager import value; assert value==3'],'verify':True},
                   {'done':'Verified'}]
        events = []
        agent = Agent(self.root,ScriptedModel(actions),{},events.append,lambda args:True)
        self.assertEqual(agent.run('Add worker management'),'COMPLETED')
        writes = [e for e in events if e['kind']=='action' and e['data'].get('tool')=='write']
        self.assertEqual(len(writes),1)
        self.assertTrue(any(e['kind']=='simplicity' and e['data'].get('reconsider') for e in events))

    def test_module_entrypoint_still_opens_existing_ui(self):
        import runpy
        with patch('local_agent.ui.main') as main:
            runpy.run_module('local_agent',run_name='__main__')
        main.assert_called_once_with()

    def test_growth_reconsideration_is_required_in_schema_and_final_result(self):
        case = self
        class BudgetModel(ScriptedModel):
            def generate(inner,messages,config):
                action = super(BudgetModel,inner).generate(messages,config)
                if 'simplicity' in action:
                    schema = config['response_schema']
                    shapes = schema.get('anyOf',[schema])
                    target = next(shape for shape in shapes if
                                  ('done' in shape['properties'] if 'done' in action else
                                   shape['properties'].get('tool', {}).get('enum') == [action['tool']]))
                    case.assertIn('simplicity', target['required'])
                return action
        actions = [{'plan':['Implement a necessary feature'], 'change_budget':{'files':0,'new_files':0,'dependencies':0,'complexity':'initial estimate'}},
                   {'tool':'write','path':'app.py','content':'value=3'},
                   {'tool':'write','path':'app.py','content':'value=3','simplicity':'The requested feature needs this source file; none exists to modify.'},
                   {'tool':'run','argv':[sys.executable,'-c','from app import value; assert value==3'],'verify':True},
                   {'done':'Verified'},
                   {'done':'Verified','simplicity':'One new source file was necessary for the requested feature.'}]
        events = []
        agent = Agent(self.root,BudgetModel(actions),{},events.append,lambda args:True)
        self.assertEqual(agent.run('Create the requested feature'),'COMPLETED')
        self.assertEqual(sum(e['kind']=='model_response' and 'done' in e['data'] for e in events),2)

    def test_added_diff_evidence_obeys_resource_bound(self):
        self.tools.execute({'tool':'write','path':'long.py','content':'value=1\n'*100})
        engine = SimplicityEngine(self.tools,repository_map(self.tools),context_limit=256)
        report = engine.review()
        self.assertLessEqual(len(report['diff']),256)
        self.assertTrue(report['diff_truncated'])
