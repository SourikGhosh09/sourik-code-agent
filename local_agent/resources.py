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
    if power == 'Custom':
        threads = cpu if cpu is not None else max(1, hardware['threads'] // 2)
        window = context if context is not None else 8192
        if hardware.get('available') and hardware['available'] < 2 * 1024**3:
            window = min(window, 4096)
        return dict(num_thread=max(1, min(threads, hardware['threads'])), num_ctx=window, max_steps=40, workers=1)
    fraction, window, steps = {'Auto': (.5, 8192, 40), 'Eco': (.25, 4096, 24), 'Balanced': (.5, 8192, 40), 'High': (.75, 16384, 60)}[power]
    if hardware.get('available') and hardware['available'] < 2 * 1024**3:
        window = min(window, 4096)
    return dict(num_thread=max(1, min(cpu or hardware['threads'], int(hardware['threads'] * fraction) or 1)), num_ctx=min(context or window, window), max_steps=steps, workers=1)


def choose_model(hardware, models, power='Auto'):
    """Select only installed models, reserving room for runtime and context.

    Model file size is a placement estimate, not a hard memory guarantee.
    """
    free_gpu=total_gpu=0
    try:
        gpu_parts=hardware.get('gpu','').splitlines()[0].split(',')
        free_gpu=float(gpu_parts[-1].strip().split()[0])*1024**2
        total_gpu=float(gpu_parts[-2].strip().split()[0])*1024**2
    except (ValueError,IndexError):
        pass
    reclaimable=sum(max(0,m.get('loaded_vram',0)) for m in models)
    free_gpu=min(total_gpu,free_gpu+reclaimable)
    budget=max(free_gpu*.65,(hardware.get('available') or 0)*.45)
    candidates=[m for m in models if isinstance(m.get('size'),(int,float)) and 0<m['size']<=budget and m.get('name')]
    if not candidates:
        raise ValueError('No installed local model fits the estimated available memory. Close other applications or choose a smaller installed model in Model settings.')
    candidates.sort(key=lambda m:m['size'])
    return candidates[0 if power=='Eco' else -1]['name']


def preference_profile(hardware, power='Auto', preference='Quality', cpu=None, context=None):
    if power not in ('Auto', 'Eco', 'Balanced', 'High', 'Custom'):
        raise ValueError('Choose Auto, Eco, Balanced, High or Custom power.')
    if preference not in ('Quality', 'Speed'):
        raise ValueError('Choose Quality or Speed.')
    if cpu is not None and (type(cpu) is not int or not 1 <= cpu <= hardware['threads']):
        raise ValueError('CPU thread target must fit this computer.')
    if context is not None and (type(context) is not int or not 2048 <= context <= 16384):
        raise ValueError('Context target must be between 2048 and 16384.')
    config = profile(hardware, power, cpu=cpu, context=context)
    if preference == 'Speed':
        config['num_ctx'] = min(config['num_ctx'], 4096)
    config['monitor_resources'] = True
    return config


def pressure_adjust(config, hardware):
    """Only reduce runtime targets; never silently exceed the user's envelope."""
    adjusted = dict(config)
    available = hardware.get('available')
    if available is not None and available < 2 * 1024**3:
        adjusted['num_ctx'] = min(adjusted.get('num_ctx',8192), 2048)
        adjusted['num_thread'] = min(adjusted.get('num_thread',1), 2)
    return adjusted
