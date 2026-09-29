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
    def check(self, models=None, error=None, tk_error=None, options=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = io.StringIO()
            with patch.object(launcher.LocalModel, 'installed_models', return_value=models, side_effect=error), patch('tkinter.Tk', side_effect=tk_error) as window, patch.object(launcher.subprocess, 'Popen') as process, contextlib.redirect_stdout(output):
                result = launcher.main(['--check',*options], root)
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

    def test_selected_model_requires_exact_advertised_id(self):
        for model, expected in [('coder:7b', 0), ('missing', 1)]:
            with self.subTest(model=model):
                result, output = self.check([{'name':'coder:7b'}], options=['--model',model])
                self.assertEqual(result, expected)
                self.assertIn('coder:7b', output)

    def test_options_are_check_only_and_remote_hosts_are_rejected(self):
        with patch.object(launcher.subprocess, 'Popen') as process, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                launcher.main(['--endpoint','http://localhost:1234'])
            self.assertEqual(raised.exception.code, 2)
            process.assert_not_called()
        with patch('urllib.request.build_opener') as build:
            result, output = self.check(options=['--endpoint','https://remote.example'])
            self.assertEqual(result, 1)
            self.assertIn('local model server', output)
            build.assert_not_called()

    def test_custom_compatible_endpoint_is_forwarded(self):
        with patch.object(launcher, 'LocalModel') as model_type:
            model_type.return_value.installed_models.return_value = [{'name':'coder'}]
            result, _ = self.check(options=['--endpoint','http://localhost:1234','--backend','openai-compatible','--model','coder'])
            self.assertEqual(result, 0)
            model_type.assert_called_once_with('coder','http://localhost:1234','openai-compatible')


class CompatibleDiscovery(unittest.TestCase):
    def discover(self, payload):
        opener = MagicMock()
        opener.open.return_value.__enter__.return_value.read.return_value = payload
        with patch('urllib.request.build_opener',return_value=opener) as build:
            result = launcher.LocalModel('', 'http://127.0.0.1:1234', 'openai-compatible').installed_models()
        opener.open.assert_called_once_with('http://127.0.0.1:1234/v1/models', timeout=5)
        opener.open.return_value.__enter__.return_value.read.assert_called_once_with(1_000_001)
        self.assertEqual(build.call_args.args[0].proxies, {})
        self.assertIsInstance(build.call_args.args[1], launcher.NoRedirect)
        return result

    def test_model_ids_and_empty_list(self):
        self.assertEqual(self.discover(b'{"data":[{"id":"local-coder"}]}'), [{'name':'local-coder'}])
        self.assertEqual(self.discover(b'{"data":[]}'), [])

    def test_malformed_or_oversized_lists_fail_closed(self):
        for payload in (b'not JSON', b'[]', b'{}', b'{"data":null}', b'{"data":[null]}', b'{"data":[{"id":42}]}', b'{"data":[{"id":" "}]}', b' ' * 1_000_001):
            with self.subTest(size=len(payload), prefix=payload[:50]):
                with self.assertRaises(ValueError): self.discover(payload)

    def test_unknown_backend_is_rejected_before_network(self):
        with patch('urllib.request.build_opener') as build:
            with self.assertRaises(ValueError): launcher.LocalModel('', backend='unknown')
            build.assert_not_called()
