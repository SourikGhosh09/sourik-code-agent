from . import __version__
import json
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
from .agent import Agent
from .models import LocalModel
from .resources import detect, preference_profile, choose_model
from .storage import Store
from .tools import Tools


class App:
    def __init__(self, window):
        self.window = window
        self.agent = None
        self.worker = None
        self.events = queue.Queue()
        self.preparing = False
        self.startup_cancel = threading.Event()
        self.closed = False
        window.title(f'Sourik Code Agent - V{__version__} preview')
        window.geometry('1000x760')
        window.minsize(780,600)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.',font=('Segoe UI',10),background='#f3f5f7',foreground='#172b3a')
        style.configure('TButton',padding=(10,4))
        style.map('TButton',background=[('active','#e1e8ee')])
        style.configure('Run.TButton',background='#175d9c',foreground='#ffffff')
        style.map('Run.TButton',background=[('disabled','#dbe2e8'),('active','#124d82')],foreground=[('disabled','#526372')])
        style.configure('TNotebook.Tab',padding=(9,6))
        style.map('TNotebook.Tab',background=[('selected','#ffffff')])
        window.configure(background='#f3f5f7')
        frame = ttk.Frame(window,padding=12)
        frame.pack(fill='both',expand=True)
        ttk.Label(frame,text='Sourik Code Agent',font=('Segoe UI',16,'bold')).pack(anchor='w')
        # Keep room for results and recovery at the minimum window size.
        ttk.Label(frame,text='Project folder · choose a folder or a recent project').pack(anchor='w',pady=(0,4))
        row = ttk.Frame(frame)
        row.pack(fill='x')
        self.project = tk.StringVar()
        self.project_picker = ttk.Combobox(row,textvariable=self.project)
        self.project_picker.pack(side='left',fill='x',expand=True)
        self.project_picker.bind('<<ComboboxSelected>>',lambda event:self.refresh_project())
        ttk.Button(row,text='Open / create project…',command=self.choose).pack(side='left',padx=8)
        ttk.Label(frame,text='What do you want to build or change?').pack(anchor='w',pady=(10,4))
        self.goal = scrolledtext.ScrolledText(frame,height=2,font=('Segoe UI',11),wrap='word',background='#ffffff',foreground='#172b3a',insertbackground='#175d9c')
        self.goal.pack(fill='x')
        self.goal.bind('<Tab>', lambda event:self.move_focus(event))
        self.goal.bind('<Shift-Tab>', lambda event:self.move_focus(event, backward=True))
        self.goal.bind('<ISO_Left_Tab>', lambda event:self.move_focus(event, backward=True))
        controls = ttk.Frame(frame)
        controls.pack(fill='x',pady=8)
        ttk.Label(controls,text='AI power').pack(side='left')
        self.power = tk.StringVar(value='Auto')
        self.power_picker = ttk.Combobox(controls,textvariable=self.power,values=['Auto','Eco','Balanced','High','Custom'],state='readonly',width=10)
        self.power_picker.pack(side='left',padx=8)
        ttk.Label(controls,text='Priority').pack(side='left',padx=(4,5))
        self.preference = tk.StringVar(value='Quality')
        ttk.Combobox(controls,textvariable=self.preference,values=['Quality','Speed'],state='readonly',width=8).pack(side='left')
        self.run_button = ttk.Button(controls,text='Run task (Ctrl+Enter)',command=self.run,style='Run.TButton')
        self.run_button.pack(side='right')
        ttk.Button(controls,text='Stop (Esc)',command=self.stop).pack(side='right',padx=8)
        advanced_shell = ttk.Frame(frame)
        advanced_shell.pack(fill='x')
        self.settings_window = tk.Toplevel(window)
        self.settings_window.title('Settings · Sourik Code Agent')
        self.settings_window.geometry('660x590')
        self.settings_window.minsize(660,590)
        self.settings_window.withdraw()
        self.settings_window.protocol('WM_DELETE_WINDOW',self.settings_window.withdraw)
        self.settings_window.bind('<Escape>',lambda event:self.shortcut(self.settings_window.withdraw))
        settings_frame = ttk.Frame(self.settings_window,padding=16)
        settings_frame.pack(fill='both',expand=True)
        ttk.Label(settings_frame,text='Local model & PC power',font=('Segoe UI',15,'bold')).pack(anchor='w')
        ttk.Label(settings_frame,text='Changes apply to the next task. Close this window to return to your task.').pack(anchor='w',pady=(4,10))
        advanced = ttk.LabelFrame(settings_frame,text='Local model settings',padding=10)
        advanced.pack(fill='x')
        def toggle_settings():
            self.settings_window.deiconify()
            self.settings_window.lift()
        ttk.Button(advanced_shell,text='Model settings',command=toggle_settings).pack(side='left')
        self.automodel = tk.BooleanVar(value=True)
        advanced.columnconfigure(1,weight=1)
        ttk.Checkbutton(advanced,text='Auto model',variable=self.automodel).grid(row=0,column=0,sticky='w')
        self.model = tk.StringVar(value='qwen2.5-coder:3b')
        self.endpoint = tk.StringVar(value='http://127.0.0.1:11434')
        self.backend = tk.StringVar(value='ollama')
        for row_index,(label,var) in enumerate([('Model',self.model),('Server',self.endpoint)], start=1):
            ttk.Label(advanced,text=label).grid(row=row_index,column=0,sticky='w',padx=(0,8),pady=3)
            ttk.Entry(advanced,textvariable=var,width=25).grid(row=row_index,column=1,columnspan=2,sticky='ew',pady=3)
        ttk.Label(advanced,text='Backend').grid(row=0,column=1,sticky='e',padx=(8,12))
        ttk.Combobox(advanced,textvariable=self.backend,values=['ollama','openai-compatible'],width=19,state='readonly').grid(row=0,column=2,sticky='w',pady=3)
        advanced.columnconfigure(2,weight=1)
        self.cpu_target = tk.StringVar(value='')
        self.context_target = tk.StringVar(value='')
        targets = ttk.LabelFrame(settings_frame,text='Resource targets (optional)',padding=10)
        targets.pack(fill='x',pady=(10,0))
        def toggle_resources():
            toggle_settings()
            self.settings_window.after_idle(cpu_entry.focus_set)
        ttk.Button(advanced_shell,text='Resource settings',command=toggle_resources).pack(side='left',padx=8)
        ttk.Label(targets,text='CPU threads').grid(row=0,column=0,sticky='w')
        cpu_entry = ttk.Entry(targets,textvariable=self.cpu_target,width=6)
        cpu_entry.grid(row=0,column=1,sticky='w',padx=5)
        ttk.Label(targets,text='Context tokens (2048–16384)').grid(row=1,column=0,sticky='w')
        ttk.Entry(targets,textvariable=self.context_target,width=8).grid(row=1,column=1,sticky='w',padx=5)
        ttk.Label(targets,text='Custom uses your targets; blanks use Balanced defaults. Other modes cap targets.\nSpeed and low memory may reduce targets. Ollama only; no hard CPU/RAM/GPU limits.',wraplength=560).grid(row=2,column=0,columnspan=2,sticky='w',pady=4)
        def show_custom(event=None):
            if self.power.get() == 'Custom':
                if event is not None:
                    toggle_resources()
        self.power_picker.bind('<<ComboboxSelected>>',show_custom)
        self.status = tk.StringVar(value='Ready · Choose a project to begin')
        ttk.Label(frame,textvariable=self.status,font=('Segoe UI',10,'bold'),wraplength=720).pack(anchor='w',pady=6)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill='both',expand=True)
        notebook.enable_traversal()
        self.views = {}
        for name in ('Progress','Changes','What changed?','Technical details'):
            view = scrolledtext.ScrolledText(notebook,wrap='word',font=('Consolas',10) if name in ('Changes','Technical details') else ('Segoe UI',10),state='disabled',background='#ffffff',foreground='#172b3a')
            notebook.add(view,text={'What changed?':'Summary','Technical details':'Details'}.get(name,name))
            for sequence,step in (('<Control-Tab>',1),('<Control-Shift-Tab>',-1)):
                view.bind(sequence,lambda event, step=step:self.shortcut(
                    lambda:notebook.select((notebook.index('current')+step)%len(notebook.tabs()))))
            self.views[name] = view
        memory_frame = ttk.Frame(notebook,padding=8)
        notebook.add(memory_frame,text='Memory')
        self.memory_list = tk.Listbox(memory_frame,height=5,exportselection=False)
        self.memory_list.pack(fill='both',expand=True)
        self.memory_list.bind('<<ListboxSelect>>',self.show_memory)
        self.memory_detail = tk.StringVar(value='Notes and verified results stay on this computer. Current files take precedence.')
        ttk.Label(memory_frame,textvariable=self.memory_detail,wraplength=800).pack(anchor='w',pady=4)
        memory_buttons = ttk.Frame(memory_frame)
        memory_buttons.pack(fill='x')
        ttk.Button(memory_buttons,text='Add note',command=self.add_note).pack(side='left')
        ttk.Button(memory_buttons,text='Forget selected',command=self.forget_memory).pack(side='left',padx=8)
        ttk.Button(memory_buttons,text='Refresh',command=self.refresh_project).pack(side='left')
        history_frame = ttk.Frame(notebook,padding=8)
        notebook.add(history_frame,text='History')
        self.history_list = tk.Listbox(history_frame,exportselection=False)
        self.history_list.pack(fill='both',expand=True)
        ttk.Button(history_frame,text='Use selected task as a new request',command=self.reuse_goal).pack(anchor='w')
        self.memory_rows = []
        self.history_rows = []
        self.recent_projects = []
        self.memory_root = None
        self.append('Progress','Choose a project folder and describe one change.\nYour plan, checks and any action needed will appear here when the task starts.')
        self.append('What changed?','A verified task result and its project log will appear here after work begins.')
        recovery = ttk.Frame(frame)
        recovery.pack(fill='x',pady=(8,0),before=notebook)
        ttk.Button(recovery,text='Undo task changes',command=self.rollback).pack(side='left')
        ttk.Button(recovery,text='Restore checkpoint…',command=self.restore_saved).pack(side='left',padx=8)
        ttk.Button(settings_frame,text='Back to task',command=self.settings_window.withdraw).pack(anchor='e',pady=(10,0))
        self.settings = Path(__file__).resolve().parent.parent/'.agent'/'preferences.json'
        if self.settings.exists():
            try:
                saved = json.loads(self.settings.read_text())
                for name in ('project','power','model','endpoint','backend','automodel','preference','cpu_target','context_target'):
                    getattr(self,name).set(saved.get(name,getattr(self,name).get()))
                self.recent_projects = saved.get('recent_projects',[])[:10]
                self.project_picker.configure(values=self.recent_projects)
            except (ValueError,OSError):
                pass
        show_custom()
        self.refresh_timer = window.after(200,self.refresh_project)
        window.protocol('WM_DELETE_WINDOW',self.close)
        self.poll_timer = window.after(100,self.poll)
        window.bind('<Control-l>',lambda event:self.shortcut(self.project_picker.focus_set))
        window.bind('<Control-Return>',lambda event:self.shortcut(self.run))
        self.goal.bind('<Control-Return>',lambda event:self.shortcut(self.run))
        window.bind('<Escape>',lambda event:self.shortcut(self.stop))

    def move_focus(self, event, backward=False):
        target = event.widget.tk_focusPrev() if backward else event.widget.tk_focusNext()
        target.focus_set()
        return 'break'

    def shortcut(self, action):
        action()
        return 'break'

    def choose(self):
        folder = filedialog.askdirectory(mustexist=False,title='Choose or create your project folder')
        if folder:
            self.project.set(folder)
            self.refresh_project()

    def append(self,name,text):
        view = self.views[name]
        view.configure(state='normal')
        view.insert('end',text+'\n')
        view.see('end')
        view.configure(state='disabled')

    def approve(self,argv):
        event = threading.Event()
        result = []
        self.events.put({'kind':'approval','data':(argv,event,result)})
        while not event.wait(.1):
            if self.agent.cancel.is_set():
                return False
        return bool(result and result[0])

    def run(self):
        if self.closed or self.preparing or (self.worker and self.worker.is_alive()):
            return
        goal = self.goal.get('1.0','end').strip()
        if not self.project.get().strip() or not goal:
            messagebox.showinfo('Start a task','Choose a project folder and describe what you want to build.')
            return
        try:
            # Tk values are captured on the UI thread. Later edits apply to the next run.
            options = {name:getattr(self,name).get() for name in
                       ('project','power','model','endpoint','backend','automodel','preference','cpu_target','context_target')}
            root = Path(options['project']).expanduser().resolve()
            cpu = int(options['cpu_target']) if options['cpu_target'].strip() else None
            context = int(options['context_target']) if options['context_target'].strip() else None
            model = LocalModel(options['model'],options['endpoint'],options['backend'])
            self.startup_cancel = threading.Event()
            self.preparing = True
            self.run_button.configure(state='disabled')
            self.status.set('Preparing · Checking hardware and local models')
            self.append('Progress','Checking this computer and your local model settings. You can stop or close during this check.')
            self.worker = threading.Thread(target=self.discover,
                args=(root,goal,options,model,cpu,context,self.startup_cancel),daemon=True)
            self.worker.start()
        except Exception as exc:
            self.preparing = False
            self.run_button.configure(state='normal')
            self.status.set('Could not start · Check your settings and try again')
            messagebox.showerror('Could not start',str(exc))

    def discover(self, root, goal, options, model, cpu, context, cancel):
        """Only blocking discovery and queue writes here; never access Tk from a worker."""
        result = {'root':root,'goal':goal,'options':options,'model':model}
        try:
            if cancel.is_set():
                return
            root.mkdir(parents=True,exist_ok=True)
            hardware = detect(root)
            if cancel.is_set():
                return
            result['config'] = preference_profile(hardware,options['power'],options['preference'],cpu,context)
            if options['automodel'] and options['backend'] == 'ollama':
                model.model = choose_model(hardware,model.installed_models(),
                                           'Eco' if options['preference']=='Speed' else options['power'])
        except Exception as exc:
            result['error'] = str(exc)
        finally:
            self.events.put({'kind':'startup','data':result})

    def finish_startup(self, result):
        if self.closed or not self.preparing:
            return
        self.preparing = False
        if self.startup_cancel.is_set():
            self.run_button.configure(state='normal')
            self.status.set('Cancelled · No task started')
            self.append('Progress','Startup cancelled. No agent task or command was started.')
            return
        if 'error' in result:
            self.run_button.configure(state='normal')
            self.status.set('Could not start · Check your settings and try again')
            self.append('Progress','Could not prepare the local model: '+result['error'])
            messagebox.showerror('Could not start',result['error'])
            return
        root,goal,options,model,config = (result[key] for key in ('root','goal','options','model','config'))
        previous_agent = self.agent
        agent = None
        try:
            agent = Agent(root,model,config,self.events.put,self.approve)
            self.settings.parent.mkdir(parents=True,exist_ok=True)
            self.recent_projects = [str(root)]+[p for p in self.recent_projects if p != str(root)][:9]
            self.project_picker.configure(values=self.recent_projects)
            saved = {**options,'project':str(root),'model':model.model,'recent_projects':self.recent_projects}
            self.settings.write_text(json.dumps(saved),encoding='utf-8')
            # Don't overwrite settings the user changed while discovery was running.
            if all(getattr(self,name).get() == options[name] for name in
                   ('model','endpoint','backend','automodel','power','preference')):
                self.model.set(model.model)
            self.append('Progress','Using local model: '+model.model)
            self.append('Progress',f'Using {config["num_thread"]} model CPU threads; {config["num_ctx"]} context budget. These are runtime targets, not hard OS memory limits.')
            self.agent = agent
            self.worker = threading.Thread(target=agent.run,args=(goal,),daemon=True)
            self.worker.start()
        except Exception as exc:
            if agent:
                agent.store.close()
            self.agent = previous_agent
            self.run_button.configure(state='normal')
            self.status.set('Could not start · Check your settings and try again')
            messagebox.showerror('Could not start',str(exc))

    def stop(self):
        if self.preparing:
            self.startup_cancel.set()
            self.status.set('Stopping startup · Waiting for the current check to return')
        elif self.agent and self.worker and self.worker.is_alive():
            self.agent.cancel.set()
            self.status.set('Stopping · A model request may take up to 120 seconds to return')

    def rollback(self):
        if not self.agent or self.preparing or (self.worker and self.worker.is_alive()):
            return
        if messagebox.askyesno('Restore checkpoint','Restore tracked files to their contents before this task? Later edits to those files will be replaced.'):
            try:
                if not self.confirm_restore(self.agent.tools): return
                self.agent.tools.rollback(force=True)
                self.agent.log('What changed: Restored tracked files from the task checkpoint.\nResult: Recovery completed.\nRemaining: Review restored files.\nUser action: None.')
                self.status.set('Checkpoint restored')
            except Exception as exc:
                messagebox.showerror('Recovery failed',str(exc))

    def restore_saved(self):
        if self.preparing or (self.worker and self.worker.is_alive()):
            return
        root=Path(self.project.get())
        if not root.is_dir():
            return
        folder=filedialog.askdirectory(initialdir=root/'.agent'/'checkpoints',title='Select a saved checkpoint folder')
        if folder and messagebox.askyesno('Restore saved files','Replace tracked files with their saved versions? Later edits will be overwritten.'):
            try:
                tools=Tools(root,threading.Event())
                tools.load_checkpoint(folder)
                if not self.confirm_restore(tools): return
                tools.rollback(force=True)
                self.status.set('Saved checkpoint restored')
            except Exception as exc:
                messagebox.showerror('Recovery failed',str(exc))

    def confirm_restore(self, tools):
        conflicts = tools.rollback_conflicts()
        return not conflicts or messagebox.askyesno('Later edits detected',
            'These files changed after the task, or belong to an older checkpoint:\n\n'+
            '\n'.join(conflicts[:15])+'\n\nOverwrite these later edits with the saved versions?')

    def refresh_project(self):
        if self.preparing or (self.worker and self.worker.is_alive()):
            return
        root = Path(self.project.get())
        if not self.project.get() or not root.is_dir():
            return
        store = None
        try:
            store = Store(root,recover=False)
            self.memory_root = str(root.resolve())
            self.memory_rows = store.memory_records()
            self.history_rows = store.history()
            self.memory_list.delete(0,'end')
            self.history_list.delete(0,'end')
            for item in self.memory_rows:
                self.memory_list.insert('end',item['kind'].replace('_',' ').title()+': '+item['value'][:120].replace('\n',' '))
            for item in self.history_rows:
                self.history_list.insert('end',item['state']+' · '+item['goal'][:140])
            self.memory_detail.set('Select a memory to inspect its source. Verified results are only reused while their file evidence still matches.')
        except (OSError,ValueError) as exc:
            messagebox.showerror('Could not open project history',str(exc))
        finally:
            if store: store.close()

    def show_memory(self, event=None):
        selected = self.memory_list.curselection()
        if selected:
            item = self.memory_rows[selected[0]]
            self.memory_detail.set(item['value'][:1800]+'\nSource: '+(item['task'] or 'Your project note')+' · Evidence files: '+str(len(item['evidence'])))

    def add_note(self):
        if self.preparing or (self.worker and self.worker.is_alive()): return
        if not self.project.get() or not Path(self.project.get()).is_dir(): return
        value = simpledialog.askstring('Project note','What should the agent remember about this project?',parent=self.window)
        if value and value.strip():
            store = Store(self.project.get(),recover=False)
            try: store.add_memory('note',value)
            finally: store.close()
            self.refresh_project()

    def forget_memory(self):
        if self.memory_root != str(Path(self.project.get()).resolve()):
            self.refresh_project()
            return
        if self.preparing or (self.worker and self.worker.is_alive()): return
        selected = self.memory_list.curselection()
        if selected:
            store = Store(self.project.get(),recover=False)
            try: store.delete_memory(self.memory_rows[selected[0]]['id'])
            finally: store.close()
            self.refresh_project()

    def reuse_goal(self):
        if self.memory_root != str(Path(self.project.get()).resolve()):
            self.refresh_project()
            return
        if self.preparing or (self.worker and self.worker.is_alive()): return
        selected = self.history_list.curselection()
        if selected:
            self.goal.delete('1.0','end')
            self.goal.insert('1.0',self.history_rows[selected[0]]['goal'])
            self.status.set('Request loaded · Run starts a fresh inspection and checkpoint')

    def poll(self):
        if self.closed:
            return
        try:
            while True:
                event = self.events.get_nowait()
                kind,data = event['kind'],event['data']
                if kind == 'startup':
                    self.finish_startup(data)
                elif kind == 'approval':
                    argv,ready,result = data
                    result.append(False if self.agent.cancel.is_set() else messagebox.askyesno('Approve project command', 'The agent wants to run:\n\n'+repr(argv)+'\n\nIn: '+str(self.agent.root)+'\n\nThis executes code with your Windows permissions and may access files or the network. Allow this command?'))
                    ready.set()
                elif kind == 'state':
                    self.status.set(data.replace('_',' ').title())
                    if data in ('COMPLETED','FAILED','CANCELLED'):
                        self.run_button.configure(state='normal')
                        self.refresh_timer = self.window.after(100,self.refresh_project)
                        try:
                            self.append('What changed?',self.agent.tools.path('PROJECT_LOG.txt').read_text(encoding='utf-8'))
                            self.append('Changes',self.agent.tools.diff())
                        except (OSError,ValueError) as exc:
                            self.append('Progress','Could not display project history: '+str(exc))
                elif kind == 'simplicity':
                    self.append('Technical details',json.dumps(data,indent=2))
                    if data.get('reconsider'):
                        self.append('Progress','Checking whether a smaller or reused solution meets the task before making this change.')
                    elif data.get('phase') == 'review':
                        counts = data['counts']
                        self.append('Progress',f'Change review: {counts["files"]} files changed, {counts["new_files"]} new files, {counts["dependencies"]} added dependencies. Tests and safety still come first.')
                elif kind == 'resources':
                    available = data.get('available_ram')
                    self.append('Technical details',f'Resource targets: {data["threads"]} threads, {data["context"]} context tokens; available RAM: '+(f'{available/1024**3:.1f} GB' if available is not None else 'unknown'))
                elif kind == 'diff':
                    pass
                elif kind == 'plan':
                    self.append('Progress','Plan\n'+'\n'.join(f'{i+1}. {s}' for i,s in enumerate(data if isinstance(data,list) else [data])))
                elif kind in ('action','model_response'):
                    self.append('Technical details',json.dumps(data,indent=2))
                elif kind == 'observation':
                    self.append('Technical details',json.dumps(data,indent=2))
                    if 'changed' in data:
                        self.append('Progress','Updated '+data['changed'])
                    elif 'exit_code' in data:
                        self.append('Progress','Check passed.' if data['exit_code']==0 and not data.get('error') else 'The command failed. The agent is examining the problem.')
                    elif 'error' in data:
                        self.append('Progress','Action could not finish: '+data['error'])
                else:
                    self.append('Progress',data if isinstance(data,str) else json.dumps(data,indent=2))
        except queue.Empty:
            pass
        self.poll_timer = self.window.after(100,self.poll)

    def close(self):
        if self.closed:
            return
        if self.preparing:
            # Discovery cannot create an Agent or touch Tk; discard its queued result.
            self.startup_cancel.set()
        elif self.worker and self.worker.is_alive():
            self.stop()
            messagebox.showinfo('Stopping task','Please wait for the task to stop, then close the window again.')
            return
        self.closed = True
        for timer in (self.poll_timer,self.refresh_timer):
            self.window.after_cancel(timer)
        self.window.destroy()


def main():
    window = tk.Tk()
    App(window)
    window.mainloop()
