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
            model.model='scripted'
            app.power.set('Eco')
            app.automodel.set(False)
            with patch('local_agent.ui.LocalModel',return_value=model),patch('local_agent.ui.detect',return_value={'threads':4,'available':4*1024**3}):
                app.run()
                deadline=time.monotonic()+5
                while (app.preparing or app.worker.is_alive()) and time.monotonic()<deadline:
                    window.update()
                    time.sleep(.01)
            self.assertFalse(app.preparing)
            self.assertFalse(app.worker.is_alive())
            app.poll()
            self.assertEqual(app.status.get(),'Failed')
            self.assertIn('Completion was not verified',app.views['What changed?'].get('1.0','end'))
            window.destroy()


class Startup(unittest.TestCase):
    """Exercise real threads/queue with UI doubles that reject off-thread access."""
    def setUp(self):
        import queue
        import threading
        from unittest.mock import Mock
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ui_thread = threading.get_ident()
        self.release = threading.Event()
        self.entered = threading.Event()
        self.app = App.__new__(App)
        app = self.app
        app.agent = None
        app.worker = None
        app.events = queue.Queue()
        app.preparing = False
        app.startup_cancel = threading.Event()
        app.closed = False
        app.poll_timer, app.refresh_timer = 'poll', 'refresh'
        app.settings = self.root/'preferences.json'
        app.recent_projects = []
        def ui_call(*args, **kwargs):
            self.assertEqual(threading.get_ident(), self.ui_thread, 'Worker touched the UI')
        def value(initial):
            state = [initial]
            item = Mock()
            def get(*args):
                ui_call()
                return state[0]
            def set_value(new):
                ui_call()
                state[0] = new
            item.get.side_effect = get
            item.set.side_effect = set_value
            return item
        for name, initial in dict(project=str(self.root/'project'), power='Eco', preference='Quality',
                                  model='manual-model', endpoint='http://127.0.0.1:11434', backend='ollama',
                                  automodel=False, cpu_target='', context_target='', status='Ready',
                                  goal='Inspect the original project').items():
            setattr(app, name, value(initial))
        app.window = Mock()
        app.window.after.side_effect = lambda *args:(ui_call() or 'next-timer')
        app.window.after_cancel.side_effect = ui_call
        app.window.destroy.side_effect = ui_call
        app.run_button = Mock()
        app.run_button.configure.side_effect = ui_call
        app.project_picker = Mock()
        app.project_picker.configure.side_effect = ui_call
        app.append = Mock(side_effect=ui_call)
        self.errors = self.enterContext(patch('local_agent.ui.messagebox.showerror', side_effect=ui_call))
        self.info = self.enterContext(patch('local_agent.ui.messagebox.showinfo', side_effect=ui_call))
        self.detect = self.enterContext(patch('local_agent.ui.detect', return_value={'threads':4,'available':8*1024**3}))
        self.agent_type = self.enterContext(patch('local_agent.ui.Agent'))
        self.model_type = self.enterContext(patch('local_agent.ui.LocalModel'))
        self.model_type.return_value.model = 'manual-model'
        self.addCleanup(self.finish_workers)

    def finish_workers(self):
        self.app.startup_cancel.set()
        self.release.set()
        if self.app.worker:
            self.app.worker.join(3)
            self.assertFalse(self.app.worker.is_alive(), 'Worker did not finish')

    def slow_check(self, *args):
        import threading
        self.assertNotEqual(threading.get_ident(), self.ui_thread)
        self.entered.set()
        if not self.release.wait(3):
            raise TimeoutError('Test did not release discovery')
        return {'threads':4,'available':8*1024**3}

    def finish_discovery(self):
        self.release.set()
        self.app.worker.join(3)
        self.assertFalse(self.app.worker.is_alive())
        self.app.poll()
        if self.app.worker:
            self.app.worker.join(3)

    def test_slow_discovery_returns_to_ui_and_blocks_duplicate_run(self):
        self.detect.side_effect = self.slow_check
        self.app.run()
        self.assertTrue(self.entered.wait(1))
        self.assertTrue(self.app.preparing)
        self.assertIn('Preparing', self.app.status.get())
        self.app.poll()  # UI can process events while the hardware call is blocked.
        self.app.run()
        self.detect.assert_called_once()
        self.agent_type.assert_not_called()
        self.app.run_button.configure.assert_called_with(state='disabled')
        self.finish_discovery()
        self.agent_type.assert_called_once()
        self.agent_type.return_value.run.assert_called_once_with('Inspect the original project')
        self.assertFalse(self.app.preparing)
        self.errors.assert_not_called()

    def test_stop_discards_already_queued_result_without_starting_task(self):
        self.app.run()
        self.app.worker.join(3)
        self.assertFalse(self.app.events.empty())
        self.app.stop()
        self.app.run()  # A late result must be consumed before another startup.
        self.app.poll()
        self.agent_type.assert_not_called()
        self.assertEqual(self.app.status.get(), 'Cancelled · No task started')
        self.assertFalse(self.app.settings.exists())
        self.app.run_button.configure.assert_called_with(state='normal')

    def test_stop_during_hardware_skips_model_discovery(self):
        self.app.automodel.set(True)
        self.detect.side_effect = self.slow_check
        self.app.run()
        self.assertTrue(self.entered.wait(1))
        self.app.stop()
        self.finish_discovery()
        self.model_type.return_value.installed_models.assert_not_called()
        self.agent_type.assert_not_called()
        self.assertFalse(self.app.preparing)

    def test_close_during_model_discovery_ignores_late_result(self):
        self.app.automodel.set(True)
        def slow_models():
            self.slow_check()
            return [{'name':'small-model', 'size':1_000_000_000}]
        self.model_type.return_value.installed_models.side_effect = slow_models
        self.app.run()
        self.assertTrue(self.entered.wait(1))
        self.app.close()
        self.assertTrue(self.app.closed)
        self.assertTrue(self.app.startup_cancel.is_set())
        self.app.window.destroy.assert_called_once()
        self.assertEqual(self.app.window.after_cancel.call_count, 2)
        self.finish_discovery()
        self.agent_type.assert_not_called()
        self.errors.assert_not_called()
        self.info.assert_not_called()
        self.assertFalse(self.app.settings.exists())

    def test_discovery_error_is_visible_and_next_attempt_can_start(self):
        self.detect.side_effect = OSError('Hardware check failed')
        self.app.run()
        self.finish_discovery()
        self.errors.assert_called_once_with('Could not start', 'Hardware check failed')
        self.app.run_button.configure.assert_called_with(state='normal')
        self.agent_type.assert_not_called()
        self.detect.side_effect = None
        self.app.run()
        self.finish_discovery()
        self.agent_type.assert_called_once()

    def test_running_task_uses_snapshot_and_preserves_new_ui_settings(self):
        import json
        self.detect.side_effect = self.slow_check
        original = self.app.project.get()
        self.app.run()
        self.assertTrue(self.entered.wait(1))
        self.app.project.set(str(self.root/'different-project'))
        self.app.goal.set('A different task')
        self.app.model.set('next-model')
        self.app.cpu_target.set('not an integer')
        self.finish_discovery()
        self.assertEqual(self.agent_type.call_args.args[0], Path(original))
        self.agent_type.return_value.run.assert_called_once_with('Inspect the original project')
        self.assertEqual(self.app.model.get(), 'next-model')
        self.assertEqual(self.app.cpu_target.get(), 'not an integer')
        saved = json.loads(self.app.settings.read_text())
        self.assertEqual(saved['project'], original)
        self.assertEqual(saved['model'], 'manual-model')
        self.assertEqual(saved['cpu_target'], '')

    def test_invalid_numeric_setting_does_not_start_discovery(self):
        self.app.cpu_target.set('wrong')
        self.app.run()
        self.detect.assert_not_called()
        self.agent_type.assert_not_called()
        self.errors.assert_called_once()
        self.assertFalse(self.app.preparing)
        self.app.run_button.configure.assert_called_with(state='normal')

    def test_settings_failure_closes_unused_agent_and_allows_retry(self):
        self.app.settings = self.root/'occupied'/'preferences.json'
        self.app.settings.parent.write_text('This is a file')
        self.app.run()
        self.finish_discovery()
        self.agent_type.return_value.store.close.assert_called_once()
        self.agent_type.return_value.run.assert_not_called()
        self.assertIsNone(self.app.agent)
        self.assertFalse(self.app.preparing)
        self.errors.assert_called_once()

    def test_scripted_task_result_reaches_ui_after_background_discovery(self):
        from local_agent.agent import Agent
        self.agent_type.side_effect = Agent
        model = ScriptedModel([{'done':'Not verified'}]*24)
        model.model = 'scripted'
        self.model_type.return_value = model
        self.app.run()
        self.finish_discovery()
        self.app.poll()
        self.assertEqual(self.app.status.get(), 'Failed')
        self.assertTrue(any(name == 'What changed?' and 'Completion was not verified' in text
                            for (name,text), kwargs in self.app.append.call_args_list))
        self.app.run_button.configure.assert_called_with(state='normal')

    def test_auto_model_selection_reaches_saved_settings(self):
        import json
        self.app.automodel.set(True)
        self.model_type.return_value.installed_models.return_value = [{'name':'small-model', 'size':1_000_000_000}]
        self.app.run()
        self.finish_discovery()
        self.assertEqual(self.app.model.get(), 'small-model')
        self.assertEqual(json.loads(self.app.settings.read_text())['model'], 'small-model')
        self.assertEqual(self.agent_type.call_args.args[1].model, 'small-model')
        self.errors.assert_not_called()

    def test_tcl_event_loop_handles_callbacks_while_discovery_waits(self):
        # Tcl's timer/event loop runs without a display; native Tk widgets still need one.
        window = tk.Tcl()
        self.app.window = window
        self.app.poll_timer = window.after(0, self.app.poll)
        self.app.refresh_timer = window.after(60_000, lambda:None)
        self.detect.side_effect = self.slow_check
        self.app.run()
        self.assertTrue(self.entered.wait(1))
        heartbeats = []
        window.after(0, lambda:heartbeats.append('responsive'))
        try:
            window.update()
            self.assertEqual(heartbeats, ['responsive'])
            self.agent_type.assert_not_called()
            self.app.stop()
            self.finish_discovery()
        finally:
            window.after_cancel(self.app.poll_timer)
            window.after_cancel(self.app.refresh_timer)
