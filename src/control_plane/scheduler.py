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
    """
    Enhanced scheduler: GPU-aware + NUMA-aware
    """

    def __init__(self, nodes):
        self.nodes = nodes  # List[Node]

    def schedule_job(self, job_request):
        """
        Schedule a job with resource preferences:
        job_request: dict with keys 'cpus', 'mem', 'gpus', 'preferred_numa' (optional)
        """
        # Sort nodes by available GPUs first (GPU-aware)
        sorted_nodes = sorted(self.nodes, key=lambda n: n.available_gpus, reverse=True)

        for node in sorted_nodes:
            numa = job_request.get("preferred_numa")
            if node.can_allocate(job_request["cpus"], job_request["mem"], job_request["gpus"], numa):
                node.allocate(job_request["cpus"], job_request["mem"], job_request["gpus"], numa)
                log_info(f"Scheduled job on {node.name} (NUMA: {numa})")
                return node.name
        log_error("No available node found for job")
        return None


# Example Usage
if __name__ == "__main__":
    # # Two nodes, each with 2 GPUs, 16 cores, 64GB RAM, and simple NUMA split
    # nodes = [
    #     Node("node1", total_cpus=16, total_mem=64, total_gpus=2, numa_topology={0: 8, 1: 8}),
    #     Node("node2", total_cpus=32, total_mem=128, total_gpus=4, numa_topology={0: 16, 1: 16})
    # ]
    # scheduler = Scheduler(nodes)
    #
    # job1 = {"cpus": 4, "mem": 8, "gpus": 1, "preferred_numa": 0}
    # job2 = {"cpus": 16, "mem": 32, "gpus": 2}  # No NUMA preference
    #
    # assigned_node1 = scheduler.schedule_job(job1)
    # assigned_node2 = scheduler.schedule_job(job2)
    #
    # print(f"Job1 assigned to: {assigned_node1}")
    # print(f"Job2 assigned to: {assigned_node2}")
