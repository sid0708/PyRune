# src/control_plane/node_dynamic.py
from .modules.monitoring import get_total_memory, get_cpu_count
from .modules.logging import log_info, log_error, log_debug
try:
    import pynvml
    pynvml.nvmlInit()
    NVML_AVAILABLE = True
except:
    NVML_AVAILABLE = False

class Node:
    def __init__(self, name):
        self.name = name
        # Dynamic detection
        self.total_cpus = get_cpu_count()
        self.total_mem = get_total_memory()  # GB
        self.available_cpus = self.total_cpus
        self.available_mem = self.total_mem
        self.total_gpus = self._detect_gpus()
        self.available_gpus = self.total_gpus
        # Track NUMA if on Linux (simplified example)
        self.numa_topology = self._detect_numa()

    def _detect_gpus(self):
        if NVML_AVAILABLE:
            return pynvml.nvmlDeviceGetCount()
        return 0

    def _detect_numa(self):
        # On Linux, could parse /sys/devices/system/node
        # Here we simplify to one NUMA node
        return {0: self.available_cpus}

    def can_allocate(self, cpus, mem, gpus, preferred_numa=None):
        if self.available_mem < mem or self.available_gpus < gpus:
            return False
        if preferred_numa is not None:
            return self.numa_topology.get(preferred_numa, 0) >= cpus
        return self.available_cpus >= cpus

    def allocate(self, cpus, mem, gpus, preferred_numa=None):
        if not self.can_allocate(cpus, mem, gpus, preferred_numa):
            return False
        self.available_mem -= mem
        self.available_gpus -= gpus
        if preferred_numa is not None:
            self.numa_topology[preferred_numa] -= cpus
        self.available_cpus -= cpus
        return True

    def release(self, cpus, mem, gpus, preferred_numa=None):
        self.available_mem += mem
        self.available_gpus += gpus
        if preferred_numa is not None:
            self.numa_topology[preferred_numa] += cpus
        self.available_cpus += cpus


class Scheduler:
    def __init__(self, nodes):
        self.nodes = nodes

    def schedule(self, job_func, *args, **kwargs):
        """
        Schedule a job defined with @pyrune_job decorator.
        """
        if not hasattr(job_func, "_pyrune_meta"):
            raise ValueError("Function must be decorated with @pyrune_job")

        job_request = job_func._pyrune_meta
        sorted_nodes = sorted(self.nodes, key=lambda n: n.available_gpus, reverse=True)

        for node in sorted_nodes:
            numa = job_request.get("preferred_numa")
            if node.can_allocate(job_request["cpus"], job_request["mem"], job_request["gpus"], numa):
                node.allocate(job_request["cpus"], job_request["mem"], job_request["gpus"], numa)
                log_info(f"Scheduled job {job_func.__name__} on {node.name} (NUMA: {numa})")

                # Execute the function
                try:
                    result = job_request["func"](*args, **kwargs)
                    log_info(f"Job {job_func.__name__} completed on {node.name} with result={result}")
                    return node.name, result
                except Exception as e:
                    log_error(f"Execution error on {node.name}: {e}")
                    return node.name, None

        log_error("No available node found for job")
        return None, None


# Example Usage
if __name__ == "__main__":

    nodes = [
        Node("node1"),
        Node("node2"),
        Node("node3"),
    ]

    scheduler = Scheduler(nodes)


    @pyrune_job(cpus=2, mem=4, gpus=1)
    def train_model(data, epochs):
        return f"Training model on {len(data)} samples for {epochs} epochs"

    @pyrune_job(cpus=1, mem=2)
    def preprocess_data(texts):
        return [t.lower() for t in texts]

    # Run jobs through scheduler
    jobs = [
        (preprocess_data, ["HELLO", "WORLD"]),
        (train_model, ["sample1", "sample2"], {"epochs": 10}),
    ]

    for func, args, kwargs in [(f, a, kw if isinstance(kw, dict) else {}) for f, a, *kw in jobs]:
        node, result = scheduler.schedule(func, *args, **kwargs)
        print(f"Job {func.__name__} ran on {node} → {result}")
