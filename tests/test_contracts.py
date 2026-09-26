"""Action completeness and recovery evidence regressions."""
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

from local_agent import __version__
from local_agent.agent import Agent
from local_agent.contracts import REQUIRED_FIELDS, response_schema, validate_action
from tests.test_agent import ScriptedModel


class Contracts(unittest.TestCase):
    def test_tool_specific_schema_requires_parameters(self):
        for verified in (False, True):
            shapes = response_schema(True, verified, True)['anyOf']
            actions = [s for s in shapes if 'tool' in s['properties']]
            self.assertEqual(len(actions), len(REQUIRED_FIELDS))
            for shape in actions:
                tool = shape['properties']['tool']['enum'][0]
                self.assertTrue(set(REQUIRED_FIELDS[tool]).issubset(shape['required']))
                self.assertEqual('simplicity' in shape['required'], tool in ('write', 'patch', 'move', 'delete'))
                if tool == 'patch':
                    self.assertNotIn('start_line', shape['properties'])

    def test_incomplete_patch_recovery_keeps_failing_test_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'app.py').write_text('def add(a,b): return a-b\n', encoding='utf-8')
            (root/'test_app.py').write_text('import unittest\nfrom app import add\nclass Check(unittest.TestCase):\n def test_add(self): self.assertEqual(add(2,3),5)\n', encoding='utf-8')
            case = self
            class Model(ScriptedModel):
                def generate(inner, messages, config):
                    action = super(Model, inner).generate(messages, config)
                    if action.get('old') == 'a-b':
                        context = str(messages)
                        case.assertIn('Last failing command evidence', context)
                        case.assertIn('test_add', context)
                        case.assertIn('patch requires fields', context)
                    return action
            actions = [{'plan':['Repair addition']}, {'tool':'patch','path':'app.py'},
                       {'tool':'patch','path':'app.py'},
                       {'tool':'patch','path':'app.py','old':'a-b','new':'a+b'},
                       {'tool':'run','argv':[sys.executable,'-m','unittest','discover']},
                       {'done':'Addition verified'}]
            events = []
            agent = Agent(root, Model(actions), {}, events.append, lambda argv: True)
            self.assertEqual(agent.run('Repair add without weakening tests'), 'COMPLETED')
            patches = [e for e in events if e['kind']=='action' and e['data'].get('tool')=='patch']
            self.assertEqual(len(patches), 1)

    def test_empty_replacement_allowed_and_version_matches_metadata(self):
        validate_action({'tool':'patch','path':'app.py','old':'unused','new':''})
        with self.assertRaisesRegex(ValueError, 'exact existing text'):
            validate_action({'tool':'patch','path':'app.py','old':'','new':'x'})
        with self.assertRaisesRegex(ValueError, 'Run approved tests'):
            validate_action({'tool':'patch','path':'app.py','old':'same','new':'same'})
        metadata = tomllib.loads((Path(__file__).resolve().parents[1]/'pyproject.toml').read_text(encoding='utf-8'))
        self.assertEqual(metadata['project']['version'], __version__)

    def test_repeated_unchanged_invoice_write_refreshes_remaining_failure(self):
        from scripts.evaluate_local import INVOICE_FILES, INVOICE_FIXED, approve_invoice
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name, content in INVOICE_FILES.items():
                (root/name).write_text(content, encoding='utf-8')
            case = self
            class Model(ScriptedModel):
                def generate(inner, messages, config):
                    action = super(Model, inner).generate(messages, config)
                    if action.get('path') == 'line_items.py' and action.get('tool') == 'write':
                        case.assertIn('Unchanged edit: invoice.py', str(messages))
                        case.assertIn('Last failing command evidence', str(messages))
                        case.assertIn('test_line', str(messages))
                        case.assertIn('unit_cents + quantity', str(messages))
                    return action
            invoice = {'tool':'write', 'path':'invoice.py', 'content':INVOICE_FIXED['invoice.py']}
            command = {'tool':'run', 'argv':[sys.executable, '-m', 'unittest', 'discover']}
            actions = [{'plan':['Repair the two arithmetic expressions']},
                       {'tool':'read', 'path':'invoice.py'},
                       {'tool':'read', 'path':'line_items.py'}, invoice, command,
                       invoice, {'tool':'read', 'path':'invoice.py'}, invoice,
                       {'tool':'write', 'path':'line_items.py', 'content':INVOICE_FIXED['line_items.py']},
                       command, {'done':'Both expressions verified with original tests'}]
            events = []
            agent = Agent(root, Model(actions), {}, events.append, lambda argv:approve_invoice(root, argv))
            self.assertEqual(agent.run('Repair invoice and line totals; preserve README, tests and validation'), 'COMPLETED')
            self.assertEqual(agent.tools.revision, 2)
            self.assertEqual(sum(e['kind']=='recovery' for e in events), 1)
            self.assertTrue(approve_invoice(root, command['argv']))
            for name in ('README.md', 'test_invoice.py', 'validation.py'):
                self.assertEqual((root/name).read_text(encoding='utf-8'), INVOICE_FILES[name])

    def test_unchanged_write_keeps_verification_and_clears_old_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            case = self
            class Model(ScriptedModel):
                def generate(inner, messages, config):
                    action = super(Model, inner).generate(messages, config)
                    if 'done' in action:
                        import json
                        observation = json.loads(messages[-1]['content'].split(': ', 1)[1])
                        case.assertIsNone(observation['last_failing_command'])
                        case.assertIn('Tests passed', observation['controller_instruction'])
                        case.assertTrue(any('done' in s['properties'] for s in config['response_schema']['anyOf']))
                    return action
            actions = [{'plan':['Repair and verify value']},
                       {'tool':'write', 'path':'app.py', 'content':'value=1'},
                       {'tool':'run', 'argv':[sys.executable, '-c', 'from app import value; assert value==2'], 'verify':True},
                       {'tool':'write', 'path':'app.py', 'content':'value=2'},
                       {'tool':'run', 'argv':[sys.executable, '-c', 'from app import value; assert value==2'], 'verify':True},
                       {'tool':'write', 'path':'app.py', 'content':'value=2'},
                       {'done':'Verified value'}]
            agent = Agent(root, Model(actions), {}, approve=lambda argv:True)
            self.assertEqual(agent.run('Set value to two'), 'COMPLETED')
            self.assertEqual(agent.tools.revision, agent.tools.verified_revision)

    def test_repeated_unchanged_write_stops_without_approval_or_verification(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'app.py').write_text('value=1', encoding='utf-8')
            actions = [{'plan':['Repair value']}]+[{'tool':'write', 'path':'app.py', 'content':'value=1'}]*3
            approvals = []
            agent = Agent(root, ScriptedModel(actions), {'max_steps':4}, approve=lambda argv:approvals.append(argv))
            self.assertEqual(agent.run('Set value to two'), 'FAILED')
            self.assertEqual(agent.tools.revision, 0)
            self.assertEqual(agent.tools.verified_revision, -1)
            self.assertEqual(approvals, [])
            self.assertEqual((root/'app.py').read_text(), 'value=1')

    def test_budget_reconsideration_leaves_read_and_test_schema_available(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'app.py').write_text('value=1', encoding='utf-8')
            case = self
            class Model(ScriptedModel):
                def generate(inner, messages, config):
                    action = super(Model, inner).generate(messages, config)
                    if action.get('tool') == 'read':
                        shapes = config['response_schema']['anyOf']
                        for tool in ('read', 'search', 'list', 'run'):
                            shape = next(s for s in shapes if s['properties'].get('tool', {}).get('enum') == [tool])
                            case.assertNotIn('simplicity', shape['required'])
                        write = next(s for s in shapes if s['properties'].get('tool', {}).get('enum') == ['write'])
                        case.assertIn('simplicity', write['required'])
                    return action
            actions = [{'plan':['Check value'], 'change_budget':{'files':0, 'new_files':0, 'dependencies':0, 'complexity':'verify only'}},
                       {'tool':'write', 'path':'extra.py', 'content':'value=1'},
                       {'tool':'read', 'path':'app.py'},
                       {'tool':'run', 'argv':[sys.executable, '-c', 'from app import value; assert value==1'], 'verify':True},
                       {'done':'Existing value verified'}]
            approvals = []
            def approve(argv):
                approvals.append(argv)
                return True
            agent = Agent(root, Model(actions), {}, approve=approve)
            self.assertEqual(agent.run('Ensure value is one; avoid unnecessary files'), 'COMPLETED')
            self.assertFalse((root/'extra.py').exists())
            self.assertEqual(len(approvals), 1)
            self.assertEqual(agent.tools.diff(), '')
