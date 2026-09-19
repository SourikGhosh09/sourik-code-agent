import json
from pathlib import Path
import tempfile
import threading
import unittest
from local_agent.models import LocalModel
from local_agent.tools import Tools,redact
from local_agent.storage import Store
from local_agent.context import repository_map


class Recovery(unittest.TestCase):
    def test_persisted_checkpoint(self):
        with tempfile.TemporaryDirectory() as d:
            tools=Tools(d,threading.Event())
            tools.execute({'tool':'write','path':'a.txt','content':'hello'})
            reopened=Tools(d,threading.Event())
            reopened.load_checkpoint(tools.checkpoint)
            reopened.rollback()
            self.assertFalse((Path(d)/'a.txt').exists())
    def test_crash_state_and_memory(self):
        with tempfile.TemporaryDirectory() as d:
            store=Store(d)
            task=store.task('unfinished')
            store.remember('command','python -m unittest')
            store.close()
            store=Store(d)
            self.assertEqual(store.db.execute('SELECT state FROM tasks WHERE id=?',(task,)).fetchone()[0],'INTERRUPTED')
            self.assertIn('command',store.memories())
            store.forget('command')
            self.assertEqual(store.memories(),{})
            store.close()
    def test_context_and_ignore(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'.gitignore').write_text('generated/\n*.log')
            (root/'generated').mkdir()
            (root/'generated'/'junk.py').write_text('junk')
            (root/'a.py').write_text('def add(a,b): return a+b')
            (root/'.env').write_text('SECRET=no')
            tools=Tools(d,threading.Event())
            rows=repository_map(tools)
            self.assertEqual([r['symbols'] for r in rows if r['path']=='a.py'],[['add']])
            self.assertNotIn('.env',tools.files())
            self.assertNotIn('generated/junk.py',[s.replace('\\','/') for s in tools.files()])
    def test_bounded_file_context(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'long.txt').write_text('line\n'*300)
            tools=Tools(d,threading.Event())
            result=tools.execute({'tool':'read','path':'long.txt'})
            self.assertTrue(result['truncated'])
            self.assertEqual(result['content'].count('line'),120)
            result=tools.execute({'tool':'read','path':'long.txt','start_line':290})
            self.assertFalse(result['truncated'])
            self.assertEqual(result['content'].count('line'),11)
    def test_hardware_model_selection(self):
        from local_agent.resources import choose_model
        hw={'available':4*1024**3,'gpu':'GPU, 12288 MiB, 11000 MiB'}
        models=[{'name':'small','size':2*1024**3},{'name':'medium','size':5*1024**3},{'name':'too-big','size':20*1024**3}]
        self.assertEqual(choose_model(hw,models,'Eco'),'small')
        self.assertEqual(choose_model(hw,models,'Auto'),'medium')
        hw['gpu']='GPU, 12288 MiB, 4000 MiB'
        models[1]['loaded_vram']=int(5.5*1024**3)
        self.assertEqual(choose_model(hw,models,'Auto'),'medium')
        with self.assertRaises(ValueError):
            choose_model({'available':512*1024**2},models)
    def test_redaction(self):
        self.assertNotIn('sensitive',redact('password=sensitive'))
    def test_model_http_contracts(self):
        from unittest.mock import patch,MagicMock
        for backend in ('ollama','openai-compatible'):
            data={'message':{'content':'{"plan":["inspect"]}'}} if backend=='ollama' else {'choices':[{'message':{'content':'{"plan":["inspect"]}'}}]}
            response=MagicMock()
            response.__enter__.return_value.read.return_value=json.dumps(data).encode()
            opener=MagicMock()
            opener.open.return_value=response
            with patch('urllib.request.build_opener',return_value=opener):
                result=LocalModel('test',backend=backend).generate([],{'num_ctx':4096})
            self.assertEqual(result,{'plan':['inspect']})
