"""Small deterministic checks; semantic correctness remains a test/review concern."""
import json
from pathlib import Path
import re
import tomllib

from .tools import redact

POLICY = '''Minimum necessary change, not minimum quality. Before implementation inspect the supplied repository evidence and search/read relevant code and callers. Prefer: no change when already satisfied; delete only proven unnecessary code; reuse project code; use the standard library, native framework/platform or an existing dependency; modify an existing file; then create the smallest maintainable implementation. Never weaken requested functionality, security, validation, accessibility, error handling, data integrity, compatibility or meaningful tests to reduce size. Do not add speculative managers, factories, wrappers or interfaces. Include a change_budget in the plan (files, new_files, dependencies: nonnegative counts; complexity: brief description). A flagged action needs a simplicity string explaining why the smaller/reused/native alternatives do not meet the current requirement. A larger justified task is allowed. Fix root causes, not layers of symptom patches. After verification review the supplied task diff: extra files, duplicate behavior, dependencies, abstractions, safe removals and an equally correct simpler option. Repair if needed and retest. A small diff is not proof of correctness. Review internally; do not create review/log/report files unless requested. The controller owns PROJECT_LOG.txt. After tests pass and the diff is reviewed, return a done JSON summary.'''

CHECKLIST = ['Are all changes needed for the request?', 'Could existing code or native capabilities replace any addition?',
             'Are new dependencies and abstractions justified now?', 'Can anything safely disappear?',
             'Are correctness, safety, tests and compatibility preserved?']


def dependency_file(name):
    p = Path(name)
    return p.name in ('package.json','pyproject.toml') or (p.name.startswith('requirements') and p.suffix == '.txt')


def dependencies(name, content):
    """Declared dependency names only; never import or execute project metadata."""
    if not content:
        return set()
    text = content.decode('utf-8') if isinstance(content, bytes) else content
    if Path(name).name == 'package.json':
        data = json.loads(text)
        return {key for group in ('dependencies','devDependencies','optionalDependencies','peerDependencies') for key in data.get(group,{})}
    if Path(name).name == 'pyproject.toml':
        data = tomllib.loads(text)
        project = data.get('project',{})
        entries = list(project.get('dependencies',[])) + data.get('build-system',{}).get('requires',[])
        entries += [item for group in project.get('optional-dependencies',{}).values() for item in group]
    else:
        entries = [line.strip() for line in text.splitlines() if line.strip() and not line.lstrip().startswith('#')]
    return {re.split(r'[\s\[<>=!~;@]', item, maxsplit=1)[0].lower().replace('_','-') for item in entries}


def installation(argv):
    words = [str(word).lower() for word in argv]
    # Deliberately conservative: wrappers/shells still need normal command approval.
    return any(word in ('install','add','i') for word in words[1:]) and any(
        Path(word).stem in ('pip','pip3','npm','pnpm','yarn','uv','poetry','bun') for word in words)


class SimplicityEngine:
    def __init__(self, tools, rows, context_limit=6000):
        self.tools, self.rows = tools, rows
        self.context_limit = max(256,context_limit)
        self.budget = {}
        self.inspected = set()

    def inspect(self, goal=""):
        """Reuse the ranked map and guarded reader; don't build a second index."""
        evidence = []
        remaining = min(4500,self.context_limit)
        for row in self.rows[:4]:
            name = row['path']
            try:
                observation = self.tools.execute({'tool':'read','path':name})
                content = observation['content'][:min(1500,remaining)]
                evidence.append({'path':name,'content':content,'excerpt':True})
                self.inspected.add(self.tools.path(name))
                remaining -= len(content)
                if remaining <= 0:
                    break
            except (OSError,ValueError,UnicodeError):
                continue
        term = next((symbol for row in self.rows for symbol in row.get('symbols',[]) if symbol.lower() in goal.lower()), '')
        if term:
            matches = self.tools.execute({'tool':'search','query':term})['matches'][:8]
            evidence.append({'query':term,'matches':matches})
        return evidence

    def plan(self, response):
        budget = response.get('change_budget',{})
        if not isinstance(budget,dict) or any(type(budget.get(k)) is not int or budget[k] < 0 for k in ('files','new_files','dependencies') if k in budget):
            raise ValueError('Change budget counts must be nonnegative integers.')
        self.budget = budget
        return {'phase':'plan','budget':budget,'note':'Estimates trigger reconsideration, not automatic scope reduction.'}

    def changes(self):
        changes = []
        for name,before in self.tools.backups.items():
            path = self.tools.path(name)
            after = path.read_bytes() if path.is_file() else None
            if before != after:
                changes.append((name,before,after))
        return changes

    def before(self, action):
        tool = action.get('tool')
        if tool not in ('write','patch','move','delete','run'):
            return None
        flags = []
        changes = self.changes()
        touched = {self.tools.path(n) for n,_,_ in changes}
        new = {self.tools.path(n) for n,b,a in changes if b is None and a is not None}
        if tool == 'run':
            if installation(action.get('argv',[])):
                flags.append('Dependency installation: check project code, standard library, platform and existing dependencies first.')
            else:
                return None  # Never hold verification hostage to a file-count estimate.
        else:
            name = action['path']
            path = self.tools.path(name)
            if path == self.tools.root/'PROJECT_LOG.txt':
                return None  # Delegate protected-history enforcement to Tools.
            if path.exists() and path not in self.inspected:
                read = self.tools.execute({'tool':'read','path':name})
                self.inspected.add(path)
                return {'phase':'inspect','reconsider':True,'evidence':{**read,'content':read['content'][:self.context_limit]},'note':'Read this current file before retrying the change; inspect callers with search when relevant.'}
            touched.add(path)
            if tool == 'move':
                destination = self.tools.path(action['destination'])
                touched.add(destination)
                new.add(destination)
            elif not path.exists() and tool == 'write':
                new.add(path)
            text = action.get('content',action.get('new',''))
            if tool in ('write','patch') and isinstance(text,str):
                symbols = re.findall(r'\b(?:def|function|class|interface)\s+(\w+)',text)
                matches = [r['path'] for r in self.rows if self.tools.path(r['path']) != path and set(symbols) & set(r.get('symbols',[]))]
                if matches:
                    flags.append('Possible existing implementation: '+', '.join(matches[:5])+'. Matching names are hints, not proof of duplication.')
                if (not path.exists() and re.search(r'manager|factory|wrapper|adapter|service|interface|helper',path.stem,re.I)) or re.search(r'\bclass\s+\w*(?:Manager|Factory|Wrapper|Adapter|Service|Interface)\b',text):
                    flags.append('New abstraction: explain the current problem it solves; avoid hypothetical future layers.')
                if dependency_file(name):
                    before = path.read_bytes() if path.exists() else None
                    proposed = text if tool == 'write' else (before or b'').decode('utf-8').replace(action.get('old',''),text,1)
                    try:
                        added = dependencies(name,proposed)-dependencies(name,before)
                        if added:
                            flags.append('New declared dependencies: '+', '.join(sorted(added))+'. Explain why reuse/stdlib/native/existing packages are insufficient.')
                    except (ValueError,TypeError,AttributeError):
                        flags.append('Dependency manifest could not be understood; inspect it before proceeding.')
        for key,count in (('files',len(touched)),('new_files',len(new))):
            if key in self.budget and count > self.budget[key]:
                flags.append(f'Planned {key}: {self.budget[key]}; proposed: {count}. Reconsider scope or explain the justified growth.')
        if not flags:
            return None
        explanation = action.get('simplicity','')
        allowed = isinstance(explanation,str) and bool(explanation.strip())
        return {'phase':'before','reconsider':not allowed,'findings':flags,
                'explanation':explanation if allowed else '',
                'note':'Retry with a concrete simplicity explanation or choose a smaller correct action. This never grants command permission.'}

    def review(self):
        changes = self.changes()
        added = []
        for name,before,after in changes:
            if dependency_file(name):
                try:
                    added += sorted(dependencies(name,after)-dependencies(name,before))
                except (ValueError,TypeError,AttributeError):
                    added.append(name+': unparsed manifest')
        files = len(changes)
        new_files = sum(before is None and after is not None for _,before,after in changes)
        counts = {'files':files,'new_files':new_files,'dependencies':len(added)}
        exceeded = [key for key,count in counts.items() if key in self.budget and count > self.budget[key]]
        diff = redact(self.tools.diff())
        return {'phase':'review','counts':counts,'budget_exceeded':exceeded,'added_dependencies':added[:20],
                'files':[name for name,_,_ in changes][:50], 'diff':diff[:self.context_limit], 'diff_truncated':len(diff)>self.context_limit,
                'source':'task checkpoint diff (includes new files; excludes pre-task edits)',
                'checklist':CHECKLIST,'note':'Review this evidence before completion. Keep every required behavior and protection. No automatic deletion or quality score.'}
