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
                self.assertIn('simplicity', shape['required'])
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
