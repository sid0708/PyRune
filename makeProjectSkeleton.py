import os

# Base project directory
base_dir = "PyRune"

# Directory structure
dirs = [
    "src",
    "src/modules",
    "tests",
    "docs",
    "data",
    "notebooks"
]

# Files to create
files = [
    "README.md",
    "setup.py",
    "src/__init__.py",
    "tests/__init__.py"
]

# Create directories
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"Created directory: {d}")

# Create empty files
for f in files:
    with open(f, "w") as file:
        pass
    print(f"Created file: {f}")

print("PyRune directory structure setup complete.")

