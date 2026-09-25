"""Validate the trusted invoice fixture without a local model."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.evaluate_local import INVOICE_FILES, INVOICE_FIXED, approve_invoice


class InvoiceEvaluation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write(INVOICE_FILES)

    def write(self, files):
        for name, content in files.items():
            (self.root / name).write_text(content, encoding='utf-8')

    def test_broken_fixture_fails_and_minimal_repairs_pass(self):
        self.assertTrue(approve_invoice(self.root, ['python', '-m', 'unittest', 'discover']))
        def run():
            return subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover'],
                                  cwd=self.root, capture_output=True, text=True, timeout=15)
        broken = run()
        self.assertNotEqual(broken.returncode, 0)
        self.assertIn('failures=2', broken.stderr)
        self.write(INVOICE_FIXED)
        self.assertTrue(approve_invoice(self.root, ['python', '-m', 'unittest', 'discover']))
        fixed = run()
        self.assertEqual(fixed.returncode, 0, fixed.stderr)

    def test_modified_tests_validation_and_extra_code_are_denied(self):
        command = ['python', '-m', 'unittest', 'discover']
        for name in ('test_invoice.py', 'validation.py', 'line_items.py', 'invoice.py'):
            with self.subTest(name=name):
                (self.root / name).write_text(INVOICE_FILES[name] + "\nprint('unexpected')\n", encoding='utf-8')
                self.assertFalse(approve_invoice(self.root, command))
                self.write(INVOICE_FILES)
        (self.root / 'sitecustomize.py').write_text('print("unexpected")', encoding='utf-8')
        self.assertFalse(approve_invoice(self.root, command))

    def test_commands_and_missing_files_fail_closed(self):
        for command in ([], ['python', '-c', 'print(1)'], ['pip', 'install', 'x'],
                        ['other-python', '-m', 'unittest', 'discover']):
            self.assertFalse(approve_invoice(self.root, command))
        (self.root / 'invoice.py').unlink()
        self.assertFalse(approve_invoice(self.root, ['python', '-m', 'unittest', 'discover']))
