# notebooks/notebook_setup.py
"""Setup script for Jupyter notebooks in the project."""

# Setup project path
import sys
from pathlib import Path
project_root = Path.cwd().parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))