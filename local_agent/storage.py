import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from .tools import private_folder


class Store:
    def __init__(self, root):
        folder = private_folder(root)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(folder / 'state.sqlite', check_same_thread=False)
        self.db.executescript('''PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, goal TEXT, state TEXT);
        CREATE TABLE IF NOT EXISTS events(task TEXT, time REAL, kind TEXT, data TEXT);
        CREATE TABLE IF NOT EXISTS memory(key TEXT PRIMARY KEY, value TEXT);
        ''')
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

    def close(self):
        with self.lock:
            self.db.close()
