import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from .tools import private_folder


class Store:
    def __init__(self, root, recover=True):
        folder = private_folder(root)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(folder / 'state.sqlite', check_same_thread=False)
        self.db.executescript('''PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, goal TEXT, state TEXT);
        CREATE TABLE IF NOT EXISTS events(task TEXT, time REAL, kind TEXT, data TEXT);
        CREATE TABLE IF NOT EXISTS memory(key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS repository_index(path TEXT PRIMARY KEY, digest TEXT, data TEXT);
        CREATE TABLE IF NOT EXISTS memories_v1(id TEXT PRIMARY KEY, kind TEXT, value TEXT, task TEXT, evidence TEXT, created REAL);
        ''')
        if recover:
            self.db.execute("UPDATE tasks SET state='INTERRUPTED' WHERE state NOT IN ('COMPLETED','FAILED','CANCELLED','INTERRUPTED')")
        self.db.commit()

    def task(self, goal):
        task = uuid.uuid4().hex
        with self.lock, self.db:
            self.db.execute('INSERT INTO tasks VALUES(?,?,?)', (task, goal, 'QUEUED'))
        return task

    def event(self, task, kind, data):
        with self.lock, self.db:
            self.db.execute('INSERT INTO events VALUES(?,?,?,?)', (task, time.time(), kind, json.dumps(data)))
            if kind == 'state':
                self.db.execute('UPDATE tasks SET state=? WHERE id=?', (data, task))

    def remember(self, key, value):
        with self.lock, self.db:
            self.db.execute('INSERT OR REPLACE INTO memory VALUES(?,?)', (key, value))

    def memories(self):
        return dict(self.db.execute('SELECT key,value FROM memory'))

    def forget(self, key):
        with self.lock, self.db:
            self.db.execute('DELETE FROM memory WHERE key=?', (key,))

    def index_rows(self):
        with self.lock:
            return {p: (digest, json.loads(data)) for p, digest, data in self.db.execute('SELECT path,digest,data FROM repository_index')}

    def save_index(self, rows):
        with self.lock, self.db:
            self.db.execute('DELETE FROM repository_index')
            self.db.executemany('INSERT INTO repository_index VALUES(?,?,?)', [(p, d, json.dumps(data)) for p, (d, data) in rows.items()])

    def add_memory(self, kind, value, task='', evidence=None):
        from .tools import redact
        if kind not in ('note', 'verified_task') or not value.strip():
            raise ValueError('Provide a project note or a verified task.')
        with self.lock, self.db:
            self.db.execute('INSERT INTO memories_v1 VALUES(?,?,?,?,?,?)',
                            (uuid.uuid4().hex, kind, redact(value[:4000]), task, json.dumps(evidence or {}), time.time()))
            self.db.execute('DELETE FROM memories_v1 WHERE id NOT IN (SELECT id FROM memories_v1 ORDER BY created DESC LIMIT 100)')

    def memory_records(self):
        with self.lock:
            return [dict(id=i, kind=k, value=v, task=t, evidence=json.loads(e), created=c)
                    for i,k,v,t,e,c in self.db.execute('SELECT * FROM memories_v1 ORDER BY created DESC')]

    def delete_memory(self, identifier):
        with self.lock, self.db:
            self.db.execute('DELETE FROM memories_v1 WHERE id=?', (identifier,))

    def history(self):
        with self.lock:
            return [dict(id=i, goal=g, state=s) for i,g,s in self.db.execute('SELECT id,goal,state FROM tasks ORDER BY rowid DESC LIMIT 30')]

    def close(self):
        with self.lock:
            self.db.close()
