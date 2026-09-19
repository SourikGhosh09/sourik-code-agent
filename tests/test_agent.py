import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from local_agent.agent import Agent
from local_agent.models import LocalModel
from local_agent.resources import profile
from local_agent.tools import Tools


class ScriptedModel:
    """Test fixture, never used by the production UI."""
    def __init__(self,actions):
        self.actions = iter(actions)
    def generate(self,messages,config):
        return next(self.actions)


class Acceptance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cancel = threading.Event()
        self.tools = Tools(self.root,self.cancel,lambda argv: True)
    def tearDown(self):
        self.temp.cleanup()
    def test_empty_project_repair_and_verify(self):
        actions = [ {'plan':['Create calculator and test it']}, {'tool':'list'},
            {'tool':'write','path':'app.py','content':'def add(a,b): return a-b\n'},
            {'tool':'run','argv':[sys.executable,'-c','from app import add; assert add(2,3)==5'],'verify':True},
            {'tool':'patch','path':'app.py','old':'a-b','new':'a+b'},
            {'tool':'run','argv':[sys.executable,'-c','from app import add; assert add(2,3)==5'],'verify':True},
            {'done':'Addition works'}]
        events=[]
        agent=Agent(self.root,ScriptedModel(actions),{'max_steps':12},events.append,lambda argv:True)
        self.assertEqual(agent.run('Build an addition function'),'COMPLETED')
        self.assertTrue(any(e['data']=='REPAIRING' for e in events))
        self.assertIn('+def add',agent.tools.diff())
        self.assertTrue((self.root/'PROJECT_LOG.txt').exists())
        agent.tools.rollback()
        self.assertFalse((self.root/'app.py').exists())
    def test_existing_project(self):
        (self.root/'maths.py').write_text('def double(n): return n+2\n')
        actions=[{'plan':['Inspect and fix double']},{'tool':'read','path':'maths.py'},
            {'tool':'patch','path':'maths.py','old':'n+2','new':'n*2'},
            {'tool':'run','argv':[sys.executable,'-c','from maths import double; assert double(4)==8'],'verify':True},
            {'done':'Fixed doubling'}]
        agent=Agent(self.root,ScriptedModel(actions),{},approve=lambda argv:True)
        self.assertEqual(agent.run('Fix double'),'COMPLETED')
        agent.tools.rollback()
        self.assertIn('n+2',(self.root/'maths.py').read_text())
    def test_false_completion_rejected(self):
        agent=Agent(self.root,ScriptedModel([{'done':'Done'}]*3),{'max_steps':3})
        self.assertEqual(agent.run('Build an app'),'FAILED')
    def test_boundaries_and_secrets(self):
        for name in ('../outside','C:/outside','.env','.git/config','x/private.pem','file:stream','.ENV','.GiT/config','.AGENT/state.sqlite','.git./config','NUL.txt','file. '):
            with self.assertRaises((ValueError,PermissionError)):
                self.tools.execute({'tool':'write','path':name,'content':'bad'})
    def test_permission_denied(self):
        tools=Tools(self.root,self.cancel)
        with self.assertRaises(PermissionError):
            tools.execute({'tool':'run','argv':[sys.executable,'-c','print(1)']})
    def test_timeout(self):
        out=self.tools.execute({'tool':'run','argv':[sys.executable,'-c','import time; time.sleep(20)'],'timeout':1,'verify':True})
        self.assertTrue(out['error'])
        self.assertEqual(self.tools.verified_revision,-1)
    def test_cancel(self):
        self.cancel.set()
        with self.assertRaises(InterruptedError):
            self.tools.execute({'tool':'list'})
    def test_profiles(self):
        hw={'threads':20,'available':8*1024**3}
        eco,high=profile(hw,'Eco'),profile(hw,'High')
        self.assertLess(eco['num_thread'],high['num_thread'])
        self.assertLess(eco['num_ctx'],high['num_ctx'])
        self.assertEqual(profile(hw,'High',cpu=2)['num_thread'],2)
    def test_local_only(self):
        with self.assertRaises(ValueError):
            LocalModel('model','https://remote.example')
    def test_patch_requires_unique_match(self):
        (self.root/'file').write_text('xx')
        with self.assertRaises(ValueError):
            self.tools.execute({'tool':'patch','path':'file','old':'x','new':'y'})


if __name__=='__main__':
    unittest.main()
