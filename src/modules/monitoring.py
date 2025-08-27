# src/modules/monitoring.py
"""
Tracks container and system resources using psutil (CPU/memory) and nvidia-ml-py3 (GPU).
"""
import psutil

def isNVML():
    try:
        import pynvml
        pynvml.nvmlInit()
        NVML_AVAILABLE = True
    except:
        NVML_AVAILABLE = False
    return NVML_AVAILABLE


# monitoring resource usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def get_gpu_usage():
    if not isNVML():
        return None
    import pynvml
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
    return util.gpu  # GPU utilization percentage

# monitor resource availability
def get_total_memory():
    return psutil.virtual_memory().total / (1024 ** 3)

def get_cpu_count():
    return psutil.cpu_count(logical=True)

