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
