import os


# Directory structure
dirs = [
    "src/runtime",
    "src/control_plane",
    "src/modules",
    "tests",
    "notebooks",
    "data"
]

# Files to create
files = [
    "README.md",
    "setup.py",
    "src/__init__.py",
    "src/runtime/__init__.py",
    "src/runtime/launch.py",
    "src/runtime/resources.py",
    "src/control_plane/__init__.py",
    "src/control_plane/main.py",
    "src/control_plane/scheduler.py",
    "src/modules/__init__.py",
    "src/modules/logging.py",
    "src/modules/monitoring.py",
    "src/modules/networking.py",
    "src/modules/metrics.py",
    "src/modules/utils.py"
    "tests/__init__.py",
    "tests/test_runtime.py",
    "tests/test_scheduler.py",
    "notebooks/example.ipynb",
    "data/sample_config.yaml"
]

# Create directories
for d in dirs:
    path = os.path.join(os.getcwd(), d)
    os.makedirs(path, exist_ok=True)
    print(f"Created directory: {path}")

# Create empty files
for f in files:
    path = os.path.join(os.getcwd(), f)
    with open(path, "w") as file:
        pass
    print(f"Created file: {path}")

print("PyRune project skeleton setup complete.")

