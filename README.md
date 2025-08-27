# PyRune

PyRune is a **Python-based container runtime and control plane**, designed for managing containerized workloads with advanced scheduling and resource isolation. It is optimized for AI/ML and HPC workloads, supporting features such as GPU isolation, NUMA-aware scheduling, and RDMA networking.

## Project Structure

- `src/runtime/` – Core runtime engine for container lifecycle management
- `src/control_plane/` – Orchestration and scheduling control plane
- `src/modules/` – Reusable modules for logging, monitoring, networking
- `tests/` – Unit and integration tests
- `notebooks/` – Jupyter notebooks for demos and experimentation
- `data/` – Sample configurations or datasets

## Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
