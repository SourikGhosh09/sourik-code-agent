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
        window.title(f'Sourik Code Agent - V{__version__} preview')
        window.geometry('1000x760')
        window.minsize(780,600)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.',font=('Segoe UI',11))
        frame = ttk.Frame(window,padding=24)
        frame.pack(fill='both',expand=True)
        ttk.Label(frame,text='Build something. Make it work.',font=('Segoe UI',23,'bold')).pack(anchor='w')
        ttk.Label(frame,text='Your local coding workspace · Files stay on your computer').pack(anchor='w',pady=(4,18))
        row = ttk.Frame(frame)
        row.pack(fill='x')
        self.project = tk.StringVar()
        self.project_picker = ttk.Combobox(row,textvariable=self.project)
        self.project_picker.pack(side='left',fill='x',expand=True)
        self.project_picker.bind('<<ComboboxSelected>>',lambda event:self.refresh_project())
        ttk.Button(row,text='Open / create project…',command=self.choose).pack(side='left',padx=8)
        ttk.Label(frame,text='What do you want to build or change?').pack(anchor='w',pady=(18,6))
        self.goal = scrolledtext.ScrolledText(frame,height=4,font=('Segoe UI',12),wrap='word')
        self.goal.pack(fill='x')
        controls = ttk.Frame(frame)
        controls.pack(fill='x',pady=12)
        ttk.Label(controls,text='AI power').pack(side='left')
        self.power = tk.StringVar(value='Auto')
        ttk.Combobox(controls,textvariable=self.power,values=['Auto','Eco','Balanced','High'],state='readonly',width=12).pack(side='left',padx=8)
        self.preference = tk.StringVar(value='Quality')
        ttk.Combobox(controls,textvariable=self.preference,values=['Quality','Speed'],state='readonly',width=9).pack(side='left')
        self.run_button = ttk.Button(controls,text='Run task',command=self.run)
        self.run_button.pack(side='right')
        ttk.Button(controls,text='Stop',command=self.stop).pack(side='right',padx=8)
        advanced_shell = ttk.Frame(frame)
        advanced_shell.pack(fill='x')
        advanced = ttk.LabelFrame(advanced_shell,text='Local model settings',padding=10)
        def toggle_settings():
            if advanced.winfo_manager():
                advanced.pack_forget()
            else:
                advanced.pack(fill='x',pady=6)
        ttk.Button(advanced_shell,text='Model settings',command=toggle_settings).pack(anchor='w')
        self.automodel = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced,text='Auto model',variable=self.automodel).pack(side='left')
        self.model = tk.StringVar(value='qwen2.5-coder:3b')
        self.endpoint = tk.StringVar(value='http://127.0.0.1:11434')
        self.backend = tk.StringVar(value='ollama')
        for label,var in [('Model',self.model),('Server',self.endpoint)]:
            ttk.Label(advanced,text=label).pack(side='left',padx=4)
            ttk.Entry(advanced,textvariable=var,width=25).pack(side='left')
        ttk.Combobox(advanced,textvariable=self.backend,values=['ollama','openai-compatible'],width=19,state='readonly').pack(side='left',padx=8)
        self.cpu_target = tk.StringVar(value='')
        self.context_target = tk.StringVar(value='')
        # Targets stay inside the collapsed settings group.
        targets = ttk.LabelFrame(advanced_shell,text='Resource targets (optional)',padding=6)
        def toggle_resources():
            if targets.winfo_manager(): targets.pack_forget()
            else: targets.pack(fill='x')
        ttk.Button(advanced_shell,text='Resource settings',command=toggle_resources).pack(anchor='w')
        ttk.Label(targets,text='CPU threads').pack(side='left')
        ttk.Entry(targets,textvariable=self.cpu_target,width=6).pack(side='left',padx=5)
        ttk.Label(targets,text='Context tokens').pack(side='left')
        ttk.Entry(targets,textvariable=self.context_target,width=8).pack(side='left',padx=5)
        ttk.Label(targets,text='Blank = Auto. Runtime targets, not hard memory caps.').pack(side='left')
        self.status = tk.StringVar(value='Ready · Choose a project to begin')
        ttk.Label(frame,textvariable=self.status,font=('Segoe UI',12,'bold')).pack(anchor='w',pady=12)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill='both',expand=True)
        self.views = {}
        for name in ('Progress','Changes','What changed?','Technical details'):
            view = scrolledtext.ScrolledText(notebook,wrap='word',font=('Consolas',10),state='disabled')
            notebook.add(view,text=name)
            self.views[name] = view
        memory_frame = ttk.Frame(notebook,padding=8)
        notebook.add(memory_frame,text='Project memory')
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
        notebook.add(history_frame,text='Task history')
        self.history_list = tk.Listbox(history_frame,exportselection=False)
        self.history_list.pack(fill='both',expand=True)
        ttk.Button(history_frame,text='Use selected task as a new request',command=self.reuse_goal).pack(anchor='w')
        self.memory_rows = []
        self.history_rows = []
        self.recent_projects = []
        self.memory_root = None
        ttk.Button(frame,text='Undo this task’s tracked changes',command=self.rollback).pack(anchor='e',pady=(10,0))
        ttk.Button(frame,text='Restore a saved checkpoint…',command=self.restore_saved).pack(anchor='e',pady=4)
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
        window.after(200,self.refresh_project)
        window.protocol('WM_DELETE_WINDOW',self.close)
        window.after(100,self.poll)

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
        if self.worker and self.worker.is_alive():
            return
        root = Path(self.project.get())
        goal = self.goal.get('1.0','end').strip()
        if not self.project.get() or not goal:
            messagebox.showinfo('Start a task','Choose a project folder and describe what you want to build.')
            return
        try:
            root.mkdir(parents=True,exist_ok=True)
            model = LocalModel(self.model.get(),self.endpoint.get(),self.backend.get())
            hardware = detect(root)
            config = preference_profile(hardware,self.power.get(),self.preference.get(),int(self.cpu_target.get()) if self.cpu_target.get().strip() else None,int(self.context_target.get()) if self.context_target.get().strip() else None)
            if self.automodel.get() and self.backend.get() == 'ollama':
                model.model = choose_model(hardware,model.installed_models(),'Eco' if self.preference.get()=='Speed' else self.power.get())
                self.model.set(model.model)
            self.append('Progress','Using local model: '+self.model.get())
            self.agent = Agent(root,model,config,self.events.put,self.approve)
            self.settings.parent.mkdir(exist_ok=True)
            self.recent_projects = [str(root)]+[p for p in self.recent_projects if p != str(root)][:9]
            self.project_picker.configure(values=self.recent_projects)
            self.settings.write_text(json.dumps({**{name:getattr(self,name).get() for name in ('project','power','model','endpoint','backend','automodel','preference','cpu_target','context_target')},'recent_projects':self.recent_projects}))
            self.append('Progress',f'Using {config["num_thread"]} model CPU threads; {config["num_ctx"]} context budget. These are runtime targets, not hard OS memory limits.')
            self.run_button.configure(state='disabled')
            self.worker = threading.Thread(target=self.agent.run,args=(goal,),daemon=True)
            self.worker.start()
        except Exception as exc:
            messagebox.showerror('Could not start',str(exc))

    def stop(self):
        if self.agent:
            self.agent.cancel.set()
            self.status.set('Stopping · A model request may take up to 120 seconds to return')

    def rollback(self):
        if not self.agent or (self.worker and self.worker.is_alive()):
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
        if self.worker and self.worker.is_alive():
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
        if self.worker and self.worker.is_alive():
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
        if self.worker and self.worker.is_alive(): return
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
        if self.worker and self.worker.is_alive(): return
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
        if self.worker and self.worker.is_alive(): return
        selected = self.history_list.curselection()
        if selected:
            self.goal.delete('1.0','end')
            self.goal.insert('1.0',self.history_rows[selected[0]]['goal'])
            self.status.set('Request loaded · Run starts a fresh inspection and checkpoint')

    def poll(self):
        try:
            while True:
                event = self.events.get_nowait()
                kind,data = event['kind'],event['data']
                if kind == 'approval':
                    argv,ready,result = data
                    result.append(False if self.agent.cancel.is_set() else messagebox.askyesno('Approve project command', 'The agent wants to run:\n\n'+repr(argv)+'\n\nIn: '+str(self.agent.root)+'\n\nThis executes code with your Windows permissions and may access files or the network. Allow this command?'))
                    ready.set()
                elif kind == 'state':
                    self.status.set(data.replace('_',' ').title())
                    if data in ('COMPLETED','FAILED','CANCELLED'):
                        self.run_button.configure(state='normal')
                        self.window.after(100,self.refresh_project)
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
        self.window.after(100,self.poll)

    def close(self):
        if self.worker and self.worker.is_alive():
            self.stop()
            messagebox.showinfo('Stopping task','Please wait for the task to stop, then close the window again.')
        else:
            self.window.destroy()


def main():
    window = tk.Tk()
    App(window)
    window.mainloop()
