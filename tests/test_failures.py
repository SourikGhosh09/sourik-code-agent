import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from local_agent.agent import Agent
from local_agent.tools import Tools
from tests.test_agent import ScriptedModel

class Failures(unittest.TestCase):
    def test_edit_after_verification_cannot_complete(self):
        with tempfile.TemporaryDirectory() as root:
            actions=[{'plan':['Test then change']},{'tool':'run','argv':[sys.executable,'-c','assert 2+2==4'],'verify':True},{'tool':'write','path':'new.py','content':'broken syntax !'},{'done':'Done'}]
            agent=Agent(root,ScriptedModel(actions),{'max_steps':4},approve=lambda a:True)
            self.assertEqual(agent.run('Check completion gate'),'FAILED')
    def test_whole_file_source_fences_are_normalized(self):
        with tempfile.TemporaryDirectory() as root:
            tools=Tools(root,threading.Event())
            tools.execute({'tool':'write','path':'app.py','content':'```python\nx = 3\n```'})
            self.assertEqual((Path(root)/'app.py').read_text(),'x = 3\n')
            tools.execute({'tool':'write','path':'README.md','content':'```python\nx = 3\n```'})
            self.assertTrue((Path(root)/'README.md').read_text().startswith('```'))
    def test_unchanged_edits_do_not_advance_revision(self):
        with tempfile.TemporaryDirectory() as root:
            tools=Tools(root,threading.Event())
            action={'tool':'write','path':'a.py','content':'x=1'}
            tools.execute(action)
            revision=tools.revision
            self.assertIn('unchanged',tools.execute(action))
            self.assertEqual(tools.revision,revision)
    def test_zero_tests_do_not_verify(self):
        with tempfile.TemporaryDirectory() as root:
            tools=Tools(root,threading.Event(),lambda a:True)
            result=tools.execute({'tool':'run','argv':[sys.executable,'-m','unittest','discover']})
            self.assertIn(result['exit_code'],(0,5))
            self.assertIn('No tests',result['error'])
            self.assertEqual(tools.verified_revision,-1)
    def test_standard_test_command_verifies_without_model_flag(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root)/'test_example.py').write_text('import unittest\nclass Example(unittest.TestCase):\n def test_sum(self): self.assertEqual(2+3,5)\n')
            tools=Tools(root,threading.Event(),lambda a:True)
            result=tools.execute({'tool':'run','argv':[sys.executable,'-m','unittest','discover']})
            self.assertTrue(result['verification'])
            self.assertEqual(tools.verified_revision,tools.revision)
    def test_project_history_remains_readable(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root)/'PROJECT_LOG.txt').write_text('Previous verified work')
            tools=Tools(root,threading.Event())
            self.assertEqual(tools.execute({'tool':'read','path':'PROJECT_LOG.txt'})['content'],'Previous verified work')
            self.assertNotIn('PROJECT_LOG.txt',tools.files())
    def test_log_cannot_be_overwritten_through_alias(self):
        with tempfile.TemporaryDirectory() as root:
            tools=Tools(root,threading.Event())
            with self.assertRaises(PermissionError):
                tools.execute({'tool':'write','path':'./PROJECT_LOG.txt','content':'erased'})
    def test_invalid_model_response_recovers(self):
        class BadModel:
            def __init__(self): self.count=0
            def generate(self,messages,config):
                self.count+=1
                if self.count==1: raise ValueError('Malformed response')
                if self.count==2: return {'plan':['Verify arithmetic']}
                if self.count==3: return {'tool':'run','argv':[sys.executable,'-c','assert 2+2==4'],'verify':True}
                return {'done':'Verified'}
        with tempfile.TemporaryDirectory() as root:
            agent=Agent(root,BadModel(),{'max_steps':4},approve=lambda a:True)
            self.assertEqual(agent.run('Verify arithmetic'),'COMPLETED')
    def test_log_link_does_not_escape_project(self):
        with tempfile.TemporaryDirectory() as base:
            root=Path(base)/'project'; root.mkdir()
            outside=Path(base)/'outside'; outside.write_text('unchanged')
            try: (root/'PROJECT_LOG.txt').symlink_to(outside)
            except OSError: self.skipTest('OS does not permit symlink creation')
            agent=Agent(root,ScriptedModel([]),{})
            self.assertEqual(agent.run('Inspect'),'FAILED')
            self.assertEqual(outside.read_text(),'unchanged')
