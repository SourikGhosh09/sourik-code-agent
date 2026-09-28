import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock,patch

from scripts import start_local_runtime as launcher

@unittest.skipUnless(os.name=='nt','Windows portable runtime launcher')
class Launcher(unittest.TestCase):
    def test_waits_until_server_is_ready(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'.runtime'/'ollama').mkdir(parents=True)
            (root/'.runtime'/'ollama'/'ollama.exe').touch()
            response=MagicMock()
            response.__enter__.return_value.status=200
            opener=MagicMock()
            opener.open.side_effect=[OSError('not running'),OSError('starting'),response]
            process=MagicMock(pid=4321)
            output=io.StringIO()
            with patch('urllib.request.build_opener',return_value=opener),patch('subprocess.Popen',return_value=process),patch('time.sleep'),contextlib.redirect_stdout(output):
                launcher.main([], root)
            self.assertEqual(opener.open.call_count,3)
            self.assertIn('server is ready',output.getvalue())
            self.assertEqual((root/'.runtime'/'server.pid').read_text(),'4321')

class SetupCheck(unittest.TestCase):
    def check(self, models=None, error=None, tk_error=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = io.StringIO()
            with patch.object(launcher.LocalModel, 'installed_models', return_value=models, side_effect=error), patch('tkinter.Tk', side_effect=tk_error) as window, patch.object(launcher.subprocess, 'Popen') as process, contextlib.redirect_stdout(output):
                result = launcher.main(['--check'], root)
            process.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])
            if tk_error is None:
                window.return_value.destroy.assert_called_once()
            return result, output.getvalue()

    def test_running_server_needs_no_portable_runtime(self):
        result, output = self.check([{'name': 'local-coder:7b'}])
        self.assertEqual(result, 0)
        self.assertIn('local-coder:7b', output)
        self.assertIn('absent (optional', output)

    def test_missing_models_and_server_produce_actionable_failures(self):
        for models, error, message in [([], None, 'Install a coding model'), (None, OSError('offline'), 'Start Ollama'), (None, ValueError('bad JSON'), 'Start Ollama')]:
            with self.subTest(message=message, error=error):
                result, output = self.check(models, error)
                self.assertEqual(result, 1)
                self.assertIn(message, output)

    def test_invalid_model_response_cannot_pass_readiness(self):
        for models in (None, [None], [{'name': ''}], [{'name': 42}]):
            with self.subTest(models=models):
                result, _ = self.check(models)
                self.assertEqual(result, 1)

    def test_missing_desktop_and_old_python_fail_readiness(self):
        import tkinter
        result, output = self.check([{'name': 'coder'}], tk_error=tkinter.TclError('no display'))
        self.assertEqual(result, 1)
        self.assertIn('desktop session', output)
        with patch.object(launcher.sys, 'version_info', (3, 11)):
            result, output = self.check([{'name': 'coder'}])
        self.assertEqual(result, 1)
        self.assertIn('MISSING: Python', output)

    def test_missing_portable_runtime_explains_separate_install(self):
        with tempfile.TemporaryDirectory() as directory, patch('urllib.request.build_opener') as opener, patch.object(launcher.subprocess, 'Popen') as process:
            opener.return_value.open.side_effect = OSError('offline')
            with self.assertRaisesRegex(SystemExit, 'Start your separately installed Ollama'):
                launcher.main([], Path(directory))
            process.assert_not_called()

    def test_launcher_disables_proxies_and_redirects(self):
        with patch('urllib.request.build_opener') as build, contextlib.redirect_stdout(io.StringIO()):
            launcher.main([])
        handlers = build.call_args.args
        self.assertEqual(handlers[0].proxies, {})
        self.assertIsInstance(handlers[1], launcher.NoRedirect)
