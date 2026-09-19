import contextlib
import io
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import MagicMock,patch

@unittest.skipUnless(os.name=='nt','Windows portable runtime launcher')
class Launcher(unittest.TestCase):
    def test_waits_until_server_is_ready(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'scripts').mkdir()
            (root/'.runtime'/'ollama').mkdir(parents=True)
            (root/'.runtime'/'ollama'/'ollama.exe').touch()
            script=root/'scripts'/'start_local_runtime.py'
            script.write_text((Path(__file__).resolve().parents[1]/'scripts'/'start_local_runtime.py').read_text())
            response=MagicMock()
            response.__enter__.return_value.status=200
            opener=MagicMock()
            opener.open.side_effect=[OSError('not running'),OSError('starting'),response]
            process=MagicMock(pid=4321)
            output=io.StringIO()
            with patch('urllib.request.build_opener',return_value=opener),patch('subprocess.Popen',return_value=process),patch('time.sleep'),contextlib.redirect_stdout(output):
                runpy.run_path(str(script),run_name='__main__')
            self.assertEqual(opener.open.call_count,3)
            self.assertIn('server is ready',output.getvalue())
            self.assertEqual((root/'.runtime'/'server.pid').read_text(),'4321')
