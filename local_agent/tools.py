import difflib
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time


EXCLUDED = {'.agent', '.git', 'node_modules', '__pycache__', '.venv', 'venv'}


def sensitive(path):
    return any(p in EXCLUDED or p.startswith('.env') or p.lower() in ('credentials', 'id_rsa', 'id_ed25519') or p.lower().endswith(('.pem', '.key', '.pfx')) for p in Path(path).parts)


def redact(text):
    return re.sub(r'(?i)((?:api[_-]?key|password|token|secret)\s*[=:]\s*)[^\s,;]+', r'\1[REDACTED]', str(text))


def private_folder(root):
    folder = Path(root) / '.agent'
    if folder.is_symlink() or (hasattr(folder,'is_junction') and folder.is_junction()):
        raise PermissionError('Project metadata folder cannot be a link.')
    if folder.exists():
        for directory, dirs, files in os.walk(folder,followlinks=False):
            for name in dirs+files:
                p = Path(directory)/name
                if p.is_symlink() or (hasattr(p,'is_junction') and p.is_junction()):
                    raise PermissionError('Project metadata contains a linked path.')
    folder.mkdir(exist_ok=True)
    return folder


class Tools:
    def __init__(self, root, cancel, approve=lambda args: False):
        self.root = Path(root).resolve()
        self.cancel, self.approve = cancel, approve
        self.backups = {}
        self.revision = 0
        self.verified_revision = -1
        self.checkpoint = private_folder(self.root) / 'checkpoints' / str(time.time_ns())
        self.checkpoint.mkdir(parents=True)

    def path(self, name):
        p = Path(name)
        if p.is_absolute() or '..' in p.parts or sensitive(p) or ':' in name:
            raise PermissionError('Path is outside the permitted project files.')
        target = self.root / p
        for part in [target, *target.parents]:
            if part == self.root:
                break
            if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
                raise PermissionError('Linked paths are not allowed.')
        target.resolve().relative_to(self.root)
        return target

    def files(self):
        found = []
        patterns = []
        ignore = self.root/'.gitignore'
        if ignore.is_file() and not ignore.is_symlink():
            patterns = [line.strip().rstrip('/') for line in ignore.read_text(encoding='utf-8',errors='replace').splitlines() if line.strip() and not line.startswith(('#','!'))]
        def ignored(rel):
            return any(fnmatch.fnmatch(rel.as_posix(),p) or any(fnmatch.fnmatch(part,p) for part in rel.parts) for p in patterns)
        for directory, dirs, files in os.walk(self.root, followlinks=False):
            dirs[:] = [d for d in dirs if not sensitive(Path(directory).relative_to(self.root) / d) and not ignored(Path(directory).relative_to(self.root)/d) and not (Path(directory)/d).is_symlink() and not (hasattr(Path(directory)/d,'is_junction') and (Path(directory)/d).is_junction())]
            for name in files:
                rel = str((Path(directory)/name).relative_to(self.root))
                if not sensitive(rel) and not ignored(Path(rel)):
                    try:
                        self.path(rel)
                        found.append(rel)
                    except (ValueError, PermissionError):
                        continue
                if len(found) >= 2000:
                    return found
        return sorted(found)

    def snapshot(self, name):
        p = self.path(name)
        if name not in self.backups:
            if p.exists() and p.stat().st_size > 2_000_000:
                raise ValueError('File is too large for a V0 checkpoint.')
            content = p.read_bytes() if p.exists() else None
            self.backups[name] = content
            key = hashlib.sha256(name.encode()).hexdigest()
            if content is not None:
                (self.checkpoint/key).write_bytes(content)
            self.save_manifest()

    def save_manifest(self):
        tmp = self.checkpoint/'manifest.tmp'
        tmp.write_text(json.dumps({n:hashlib.sha256(n.encode()).hexdigest() if b is not None else None for n,b in self.backups.items()}),encoding='utf-8')
        os.replace(tmp,self.checkpoint/'manifest.json')

    def load_checkpoint(self, folder):
        folder = Path(folder).resolve()
        folder.relative_to((self.root/'.agent'/'checkpoints').resolve())
        entries = json.loads((folder/'manifest.json').read_text(encoding='utf-8'))
        restored = {}
        for name,key in entries.items():
            self.path(name)
            if key is not None and key != hashlib.sha256(name.encode()).hexdigest():
                raise ValueError('Invalid checkpoint manifest.')
            restored[name] = (folder/key).read_bytes() if key else None
        self.backups = restored
        self.checkpoint = folder

    def diff(self):
        changes = []
        for name, before in self.backups.items():
            p = self.path(name)
            after = p.read_bytes() if p.exists() else b''
            changes.extend(difflib.unified_diff((before or b'').decode('utf-8',errors='replace').splitlines(True), after.decode('utf-8',errors='replace').splitlines(True), fromfile='before/'+name,tofile='after/'+name))
        return ''.join(changes)

    def rollback(self):
        for name, before in self.backups.items():
            p = self.path(name)
            if before is None:
                p.unlink(missing_ok=True)
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(before)
        self.revision += 1

    def execute(self, action):
        if self.cancel.is_set():
            raise InterruptedError('Stopped by user.')
        tool = action.get('tool')
        if tool == 'list':
            return {'files': self.files()}
        if tool == 'read':
            p = self.path(action['path'])
            if p.stat().st_size > 200_000:
                raise ValueError('Read a smaller file (limit 200 KB).')
            return {'content': redact(p.read_text(encoding='utf-8'))}
        if tool == 'search':
            query = str(action['query'])
            matches = []
            for name in self.files():
                p = self.path(name)
                if p.stat().st_size > 200_000:
                    continue
                try:
                    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
                        if query.lower() in line.lower():
                            matches.append({'path':name,'line':i,'text':redact(line[:300])})
                            if len(matches) >= 50:
                                return {'matches':matches}
                except UnicodeError:
                    pass
            return {'matches':matches}
        if tool in ('write','patch','delete','move'):
            name = action['path']
            p = self.path(name)
            if p == self.root/'PROJECT_LOG.txt' or (tool == 'move' and self.path(action['destination']) == self.root/'PROJECT_LOG.txt'):
                raise PermissionError('The controller owns PROJECT_LOG.txt.')
            self.snapshot(name)
            if tool == 'delete':
                p.unlink()
            elif tool == 'move':
                dest = self.path(action['destination'])
                if dest.exists():
                    raise ValueError('Destination already exists.')
                self.snapshot(action['destination'])
                dest.parent.mkdir(parents=True,exist_ok=True)
                p.rename(dest)
            else:
                content = action.get('content','')
                if tool == 'patch':
                    original = p.read_text(encoding='utf-8')
                    if not action.get('old') or original.count(action['old']) != 1:
                        raise ValueError('Patch must match exactly one location.')
                    content = original.replace(action['old'],action['new'],1)
                if not isinstance(content,str) or len(content.encode()) > 200_000:
                    raise ValueError('Content must be text up to 200 KB.')
                p.parent.mkdir(parents=True,exist_ok=True)
                with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:
                    f.write(content.encode())
                os.replace(f.name,p)
            self.revision += 1
            return {'changed':name}
        if tool == 'run':
            argv = action.get('argv')
            if not isinstance(argv,list) or not argv or len(argv)>64 or not all(isinstance(x,str) and '\x00' not in x for x in argv):
                raise ValueError('Command requires a list of arguments.')
            if not self.approve(argv):
                raise PermissionError('Command was not approved. Do not retry the same command.')
            self.verified_revision = -1
            # Preserve ordinary project files before approved code can change them.
            for name in self.files():
                if name != 'PROJECT_LOG.txt':
                    self.snapshot(name)
            timeout = min(120,max(1,int(action.get('timeout',60))))
            env = {k:v for k,v in os.environ.items() if k.upper() in ('PATH','SYSTEMROOT','WINDIR','TEMP','TMP','COMSPEC','PATHEXT','LANG')}
            env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
            with tempfile.TemporaryFile() as output:
                proc = subprocess.Popen(argv,cwd=self.root,env=env,stdout=output,stderr=subprocess.STDOUT,shell=False,creationflags=0x08000000 if os.name=='nt' else 0,start_new_session=os.name!='nt')
                start = time.monotonic()
                reason = ''
                while proc.poll() is None:
                    if self.cancel.is_set() or time.monotonic()-start > timeout or output.tell()>2_000_000:
                        reason = 'Cancelled' if self.cancel.is_set() else 'Time or output limit reached'
                        if os.name == 'nt':
                            subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True,creationflags=0x08000000)
                            if proc.poll() is None:
                                proc.kill()
                        else:
                            import signal
                            os.killpg(proc.pid,signal.SIGKILL)
                        proc.wait(timeout=5)
                        break
                    time.sleep(.05)
                output.seek(0)
                text = redact(output.read(16000).decode('utf-8',errors='replace'))
            for name in self.files():
                if name not in self.backups and name != 'PROJECT_LOG.txt':
                    self.backups[name] = None
            self.save_manifest()
            if action.get('verify') is True and proc.returncode == 0 and not reason:
                self.verified_revision = self.revision
            return {'exit_code':proc.returncode,'output':text,'error':reason,'verification': action.get('verify') is True}
        raise ValueError('Unknown tool: '+str(tool))
