"""
This is the entrypoint of the control-plane.
Initialize the control plane.

Register nodes

Start the scheduler.

Accept job/container requests (CLI, config file, or API).

Forward the jobs to the scheduler, then optionally call the runtime module to launch containers.
"""

from src.control_plane.scheduler import Scheduler
from src.control_plane.node_dynamic import Node
from src.modules.logging import log_info, log_error

import yaml

def discover_nodes_from_config(file_path="nodes.yaml"):
    with open(file_path) as f:
        data = yaml.safe_load(f)
    nodes = [Node(n['name']) for n in data['nodes']]
    return nodes

def main():
    # Discover nodes
    nodes = discover_nodes_from_config()

    # Initialize Scheduler
    scheduler = Scheduler(nodes)
    log_info("Scheduler initialized.")

    # Example: submit some job requests
    job_requests = [
        {"cpus": 4, "mem": 8, "gpus": 1, "preferred_numa": 0},
        {"cpus": 8, "mem": 16, "gpus": 2}
    ]

    for job in job_requests:
        assigned_node = scheduler.schedule_job(job)
        if assigned_node:
            log_info(f"Job scheduled on node {assigned_node}")
            # Optionally, call runtime.launch here to start the container
            # from src.runtime.launch import launch_container
            # launch_container(job, assigned_node)
        else:
            log_error("Job could not be scheduled")

if __name__ == "__main__":
    main()