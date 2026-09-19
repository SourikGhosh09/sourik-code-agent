import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
from local_agent.tools import Tools
from local_agent.storage import Store

@unittest.skipUnless(os.name=='nt','Windows junction test')
class JunctionBoundary(unittest.TestCase):
    def test_junction_and_metadata_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d); root=base/'project'; root.mkdir()
            outside=base/'outside'; outside.mkdir()
            (outside/'sentinel.txt').write_text('unchanged')
            link=root/'jump'
            proc=subprocess.run(['cmd','/c','mklink','/J',str(link),str(outside)],capture_output=True)
            if proc.returncode: self.skipTest('Junction creation unavailable')
            try:
                tools=Tools(root,threading.Event())
                with self.assertRaises(PermissionError):
                    tools.execute({'tool':'read','path':'jump/sentinel.txt'})
                self.assertNotIn('jump/sentinel.txt',[n.replace(chr(92),'/') for n in tools.files()])
            finally:
                link.rmdir()
            second=base/'second'; second.mkdir(); metadata=second/'.agent'
            subprocess.run(['cmd','/c','mklink','/J',str(metadata),str(outside)],capture_output=True,check=True)
            try:
                with self.assertRaises(PermissionError): Store(second)
                self.assertEqual((outside/'sentinel.txt').read_text(),'unchanged')
            finally:
                metadata.rmdir()
