"""Setup Jupyter Notebook environment."""

import tempfile
from pathlib import Path
import shutil
import atexit
from IPython import get_ipython
import uuid


# Clean ALL previous temp dirs from this notebook system
def clean_all_geoips_tutorial_tempdirs(tmp_root, ignore_dirs):
    """Clean all GeoIPS tutorial temporary directories."""
    print("Cleaning all previous tutorial temp dirs...")
    for dir_path in tmp_root.glob("geoips_tutorial_tmp_*"):
        if dir_path.is_dir() and Path(dir_path).name not in ignore_dirs:
            try:
                shutil.rmtree(dir_path, ignore_errors=True)
                print(f"Removed old temp dir: {dir_path}")
            except Exception as e:
                print(f"Failed to remove temporary directory {dir_path}: {e}")
        else:
            print(f"Skipping {dir_path}")


def setup(tmp_root=tempfile.gettempdir(), ignore_dirs=[]):
    """Set up the environment for Jupyter Notebooks."""
    # Define a global temporary root directory for the tutorial
    tmp_root = Path(tmp_root)

    print(f"Tutorial Temporary Storage Dir: {tmp_root}")

    # Clean previous temp dirs immediately
    clean_all_geoips_tutorial_tempdirs(tmp_root, ignore_dirs)

    # Create a new temp dir for this session
    _temp_uuid = uuid.uuid4().hex
    temp_dir = tmp_root / f"geoips_tutorial_tmp_{_temp_uuid}"

    # Register cleanup at shutdown
    print("Setting up cleanup hook for current session temp dir...")

    @atexit.register
    def _cleanup_session_temp_dir():
        """Clean up session temporary directory."""
        print(f"Cleaning up current session temp dir: {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        # Clean ALL previous temp dirs again to ensure no leftovers
        clean_all_geoips_tutorial_tempdirs(tmp_root, ignore_dirs)

    # Make available globally for all cells
    print("Making `temp_dir` variable available globally...")
    get_ipython().user_ns["temp_dir"] = temp_dir
    print(f"Session Temporary Directory: {temp_dir}")
