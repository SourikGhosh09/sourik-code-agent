"""Validate the trusted repair fixtures without a local model."""
from pathlib import Path
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest

from scripts.evaluate_local import INVOICE_FILES, INVOICE_FIXED, approve_invoice, TAG_FILES, TAG_FIXED, TAG_CHECKS, approve_tags


class InvoiceEvaluation(unittest.TestCase):
    files = INVOICE_FILES
    fixed = INVOICE_FIXED
    approve = staticmethod(approve_invoice)
    source = "invoice.py"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write(self.files)

    def write(self, files):
        for name, content in files.items():
            (self.root / name).write_text(content, encoding='utf-8')

    def test_broken_fixture_fails_and_minimal_repairs_pass(self):
        self.assertTrue(self.approve(self.root, ['python', '-m', 'unittest', 'discover']))
        def run():
            return subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover'],
                                  cwd=self.root, capture_output=True, text=True, timeout=15)
        broken = run()
        self.assertNotEqual(broken.returncode, 0)
        self.assertIn('failures=2', broken.stderr)
        self.write(self.fixed)
        self.assertTrue(self.approve(self.root, ['python', '-m', 'unittest', 'discover']))
        fixed = run()
        self.assertEqual(fixed.returncode, 0, fixed.stderr)

    def test_modified_tests_validation_and_extra_code_are_denied(self):
        command = ['python', '-m', 'unittest', 'discover']
        for name in self.files:
            with self.subTest(name=name):
                (self.root / name).write_text(self.files[name] + "\nprint('unexpected')\n", encoding='utf-8')
                self.assertFalse(self.approve(self.root, command))
                self.write(self.files)
        (self.root / 'sitecustomize.py').write_text('print("unexpected")', encoding='utf-8')
        self.assertFalse(self.approve(self.root, command))

    def test_commands_and_missing_files_fail_closed(self):
        for command in ([], ['python', '-c', 'print(1)'], ['pip', 'install', 'x'],
                        ['other-python', '-m', 'unittest', 'discover']):
            self.assertFalse(self.approve(self.root, command))
        (self.root / self.source).unlink()
        self.assertFalse(self.approve(self.root, ['python', '-m', 'unittest', 'discover']))


class TagEvaluation(InvoiceEvaluation):
    files = TAG_FILES
    fixed = TAG_FIXED
    approve = staticmethod(approve_tags)
    source = 'catalog.py'

    def test_independent_checks_require_both_repairs(self):
        for repaired in ((), ('normalization.py',), ('catalog.py',), ('normalization.py', 'catalog.py')):
            with self.subTest(repaired=repaired):
                self.write(TAG_FILES)
                self.write({name: TAG_FIXED[name] for name in repaired})
                self.assertTrue(approve_tags(self.root, ['python', '-m', 'unittest', 'discover']))
                result = subprocess.run([sys.executable, '-I', '-B', '-c',
                    'import sys; sys.path.insert(0, ' + repr(str(self.root)) + ');\n' + TAG_CHECKS],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode == 0, len(repaired) == 2, result.stderr)


class EvaluationOptions(unittest.TestCase):
    def test_existing_commands_keep_their_defaults(self):
        from scripts.evaluate_local import parse_arguments
        args = parse_arguments(['qwen2.5-coder:7b','--multifile'])
        self.assertEqual(args.model, 'qwen2.5-coder:7b')
        self.assertEqual(args.backend, 'ollama')
        self.assertEqual(args.endpoint, 'http://127.0.0.1:11434')
        self.assertTrue(args.multifile)
        self.assertEqual(parse_arguments([]).model, 'qwen2.5-coder:3b')

    def test_configured_runtime_and_invalid_options(self):
        from scripts.evaluate_local import parse_arguments, main
        args = parse_arguments(['coder','--tags','--backend','openai-compatible','--endpoint','http://localhost:1234'])
        self.assertEqual((args.model,args.backend,args.endpoint,args.tags), ('coder','openai-compatible','http://localhost:1234',True))
        for values in (['--tags','--multifile'], ['--backend','unknown'], ['--unknown']):
            with self.subTest(values=values), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error: parse_arguments(values)
                self.assertEqual(error.exception.code, 2)
        with self.assertRaisesRegex(ValueError, 'local model server'):
            main(['coder','--endpoint','https://remote.example','--tags'])
