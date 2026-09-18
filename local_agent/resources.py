import ctypes
import os
import shutil
import subprocess


def detect(root):
    ram = available = None
    if os.name == 'nt':
        class Memory(ctypes.Structure):
            _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in ('total','available','page','freepage','virtual','freevirtual','extended')]
        m = Memory()
        m.length = ctypes.sizeof(m)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            ram, available = m.total, m.available
    else:
        try:
            ram = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
            available = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_AVPHYS_PAGES')
        except (ValueError, OSError, AttributeError):
            pass
    gpu = ''
    try:
        gpu = subprocess.check_output(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader'], timeout=5, text=True, creationflags=0x08000000 if os.name == 'nt' else 0).strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return dict(threads=os.cpu_count() or 1, ram=ram, available=available, gpu=gpu, disk_free=shutil.disk_usage(root).free)


def profile(hardware, power='Balanced', cpu=None, context=None):
    fraction, window, steps = {'Eco': (.25, 4096, 24), 'Balanced': (.5, 8192, 40), 'High': (.75, 16384, 60)}[power]
    if hardware.get('available') and hardware['available'] < 2 * 1024**3:
        window = min(window, 4096)
    return dict(num_thread=max(1, min(cpu or hardware['threads'], int(hardware['threads'] * fraction) or 1)), num_ctx=min(context or window, window), max_steps=steps, workers=1)
