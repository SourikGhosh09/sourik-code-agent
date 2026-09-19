from pathlib import Path
import tempfile
import time
import tkinter as tk
import unittest
from unittest.mock import patch
from local_agent.ui import App
from tests.test_agent import ScriptedModel

class Desktop(unittest.TestCase):
    def test_task_failure_display(self):
        with tempfile.TemporaryDirectory() as d:
            window=tk.Tk()
            window.withdraw()
            app=App(window)
            app.settings=Path(d)/'settings.json'
            app.project.set(d)
            app.goal.insert('1.0','An intentionally incomplete task')
            model=ScriptedModel([{'done':'Not verified'}]*24)
            app.power.set('Eco')
            app.automodel.set(False)
            with patch('local_agent.ui.LocalModel',return_value=model),patch('local_agent.ui.detect',return_value={'threads':4,'available':4*1024**3}):
                app.run()
            deadline=time.monotonic()+5
            while app.worker.is_alive() and time.monotonic()<deadline:
                window.update()
                time.sleep(.01)
            self.assertFalse(app.worker.is_alive())
            app.poll()
            self.assertEqual(app.status.get(),'Failed')
            self.assertIn('Completion was not verified',app.views['What changed?'].get('1.0','end'))
            window.destroy()
