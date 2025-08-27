# src/modules/metrics.py
from src.modules.monitoring import get_cpu_usage, get_memory_usage, get_gpu_usage

def get_system_metrics():
    return {
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "gpu": get_gpu_usage()
    }