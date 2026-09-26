"""Representative ignore/import fixtures; no project imports or real model needed."""
import hashlib
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from local_agent.context import describe, repository_map
from local_agent.storage import Store
from local_agent.tools import Tools


class Indexing(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tools = Tools(self.root,threading.Event())
        self.store = Store(self.root)
        self.addCleanup(self.store.close)

    def write(self, name, content='value=1\n'):
        path = self.root/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding='utf-8')
        return path

    def files(self):
        return {Path(name).as_posix() for name in self.tools.files()}

    def test_root_anchor_nested_rules_and_directory_only_pattern(self):
        self.write('.gitignore','/generated/\ncache/\n')
        self.write('generated/noise.py')
        self.write('pkg/generated/keep.py')
        self.write('pkg/cache/omit.py')
        self.write('cache')  # Directory-only rule must keep an ordinary file.
        self.write('pkg/.gitignore','/scratch/\n*.tmp\n')
        self.write('pkg/scratch/omit.py')
        self.write('pkg/deeper/scratch/keep.py')
        self.write('pkg/deeper/omit.tmp')
        self.write('other/keep.tmp')
        files = self.files()
        self.assertTrue({'pkg/generated/keep.py','cache','pkg/deeper/scratch/keep.py','other/keep.tmp'} <= files)
        self.assertTrue({'generated/noise.py','pkg/cache/omit.py','pkg/scratch/omit.py','pkg/deeper/omit.tmp'}.isdisjoint(files))

    def test_component_globs_recursive_globs_and_ordered_negation(self):
        self.write('.gitignore','pkg/*.log\nassets/**/cache/\nbuild/**\n!build/keep.py\n*.tmp\n!keep.tmp\n')
        for name in ('pkg/omit.log','pkg/deep/keep.log','assets/cache/no.py','assets/deep/cache/no.py',
                     'assets/keep.py','build/keep.py','build/omit.py','keep.tmp','omit.tmp'):
            self.write(name)
        files = self.files()
        self.assertTrue({'pkg/deep/keep.log','assets/keep.py','build/keep.py','keep.tmp'} <= files)
        self.assertTrue({'pkg/omit.log','assets/cache/no.py','assets/deep/cache/no.py','build/omit.py','omit.tmp'}.isdisjoint(files))

    def test_nested_negation_and_pruned_parent_behavior(self):
        self.write('.gitignore','*.tmp\nexcluded/\n!excluded/keep.py\n')
        self.write('pkg/.gitignore','!keep.tmp\n')
        for name in ('pkg/keep.tmp','pkg/drop.tmp','other/keep.tmp','excluded/keep.py'):
            self.write(name)
        files = self.files()
        self.assertIn('pkg/keep.tmp',files)
        self.assertTrue({'pkg/drop.tmp','other/keep.tmp','excluded/keep.py'}.isdisjoint(files))

    def test_ignore_negation_never_includes_protected_names(self):
        self.write('.gitignore','*\n!*/\n!*\n!.env\n!.agent/\n!credentials\n')
        for name in ('.env','pkg/.ENV.local','pkg/credentials','pkg/private.key','node_modules/bad.py'):
            self.write(name,'secret=unavailable')
        self.write('pkg/keep.py')
        files = self.files()
        self.assertIn('pkg/keep.py',files)
        for name in ('.env','pkg/.ENV.local','pkg/credentials','pkg/private.key','node_modules/bad.py'):
            self.assertNotIn(name,files)
            with self.assertRaises(PermissionError): self.tools.path(name)

    def test_linked_ignore_and_linked_source_are_not_followed(self):
        outside = self.root.parent/(self.root.name+'-ignore')
        outside.write_text('*\n')
        self.addCleanup(outside.unlink)
        try:
            (self.root/'.gitignore').symlink_to(outside)
            (self.root/'linked.py').symlink_to(outside)
        except OSError:
            self.skipTest('OS does not permit symlink fixture')
        self.write('keep.py')
        self.assertIn('keep.py',self.files())
        self.assertNotIn('linked.py',self.files())
        self.assertNotIn('.gitignore',self.files())

    def test_relative_import_metadata_keeps_depth_and_imported_module(self):
        row = describe('pkg/feature/worker.py','from . import rules\nfrom ..core import validate\nfrom pkg import helpers\n')
        self.assertEqual(row['imports'],['.rules','..core','..core.validate','pkg','pkg.helpers'])

    def test_representative_repair_context_prefers_actual_relative_modules(self):
        self.write('.gitignore','/generated/\n')
        self.write('generated/checkout.py','def checkout(): pass\n')
        self.write('pkg/feature/checkout.py','from . import rules\nfrom ..core import validate\ndef checkout(): return rules.total()\n')
        self.write('pkg/feature/rules.py','def total(): return 1\n')
        self.write('pkg/core.py','def validate(): pass\n')
        self.write('aaa/rules.py','raise RuntimeError("must not be imported")\n')
        self.write('aaa/core.py','raise RuntimeError("must not be imported")\n')
        rows = repository_map(self.tools,limit=3,goal='Repair checkout',store=self.store)
        names = [Path(row['path']).as_posix() for row in rows]
        self.assertEqual(names[0],'pkg/feature/checkout.py')
        self.assertEqual(set(names[1:]),{'pkg/feature/rules.py','pkg/core.py'})
        self.assertNotIn('generated/checkout.py',{Path(n).as_posix() for n in self.store.index_rows()})

    def test_absolute_src_layout_package_and_nonexistent_imports(self):
        self.write('src/checkout.py','from billing import totals\nfrom external import missing\ndef checkout(): pass\n')
        self.write('src/billing/__init__.py')
        self.write('src/billing/totals.py')
        self.write('aaa/totals.py')
        names = {Path(row['path']).as_posix() for row in repository_map(self.tools,limit=3,goal='checkout')}
        self.assertEqual(names,{'src/checkout.py','src/billing/__init__.py','src/billing/totals.py'})

    def test_legacy_cache_reparsed_once_and_new_ignore_removes_cached_rows(self):
        content='from . import rules\n'
        path=self.write('pkg/worker.py',content)
        self.write('pkg/rules.py')
        name=str(path.relative_to(self.root))
        self.store.save_index({name:(hashlib.sha256(content.encode()).hexdigest(),
                                   {'path':name,'imports':[''],'symbols':[]})})
        rows=repository_map(self.tools,store=self.store)
        self.assertEqual(next(r for r in rows if r['path']==name)['imports'],['.rules'])
        with patch('local_agent.context.describe',side_effect=AssertionError('Unchanged file reparsed')):
            repository_map(self.tools,store=self.store)
        self.write('pkg/.gitignore','worker.py\n')
        repository_map(self.tools,store=self.store)
        self.assertNotIn(name,self.store.index_rows())

    def test_result_and_prompt_bounds_remain_in_place(self):
        # Large metadata rows exercise the map byte bound with a small fixture.
        for i in range(25):
            name=f'module_{i}.py'
            self.write(name, '\n'.join(f'def symbol_{n:02}_{"x"*110}(): pass' for n in range(40)))
        rows=repository_map(self.tools,limit=5)
        self.assertLessEqual(len(rows),5)
        import json
        self.assertLessEqual(sum(len(json.dumps(row)) for row in rows),12000)
