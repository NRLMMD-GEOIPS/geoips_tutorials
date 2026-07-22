"""Bootstrap or verify the cool_plugins workshop package.

Mirrors the setup from the first half of the `2026-Intro-and-algorithms`
tutorial so a late-joining attendee can get a working `cool_plugins` package
(plus the `workshop_infrared` workflow) from a single notebook cell:

    from solutions.setup_cool_plugins import ensure_cool_plugins
    ensure_cool_plugins()

The function is idempotent. If the package is already installed and the
workflow file is already in place, it just rebuilds the plugin registries and
reports that everything is ready.
"""

import importlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

# `workshop_infrared.yaml` is expected to live next to this script in solutions/.
SOLUTIONS_DIR = Path(__file__).resolve().parent
WORKFLOW_FILENAME = "workshop_infrared.yaml"

# Defaults matching the workshop conventions; each is overridable via the env.
DEFAULT_PACKAGE_NAME = "cool_plugins"
DEFAULT_REPO_URL = "https://github.com/NRLMMD-GeoIPS"
TEMPLATE_NAME = "template_basic_plugin"
TEMPLATE_PACKAGE_DIR = "my_package"


def _run(command, cwd=None, allow_failure=False):
    """Run `command` (a list of arguments), streaming output to the notebook.

    Raises `subprocess.CalledProcessError` on a non-zero exit unless
    `allow_failure` is True, in which case the return code is ignored.
    """
    print(f"    $ {' '.join(str(part) for part in command)}")
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0 and not allow_failure:
        raise subprocess.CalledProcessError(result.returncode, command)
    return result.returncode


def _resolve_paths():
    """Return `(packages_dir, pkg_name, pkg_dir, repo_url)` from the environment."""
    packages_dir = Path(
        os.environ.get("GEOIPS_PACKAGES_DIR", Path.home() / "geoips")
    ).expanduser()
    pkg_name = os.environ.get("MY_PKG_NAME", DEFAULT_PACKAGE_NAME)
    pkg_dir = Path(
        os.environ.get("MY_PKG_DIR", packages_dir / pkg_name)
    ).expanduser()
    repo_url = os.environ.get("GEOIPS_REPO_URL", DEFAULT_REPO_URL)
    return packages_dir, pkg_name, pkg_dir, repo_url


def _package_installed(pkg_name):
    """Return True if `pkg_name` is already importable (already pip-installed)."""
    return importlib.util.find_spec(pkg_name) is not None


def _inner_package_dir(pkg_name, pkg_dir):
    """Return the inner import-package directory that holds `plugins/`.

    Prefers the installed location reported by the import system, falling back
    to `pkg_dir / pkg_name` when the package is not yet importable.
    """
    spec = importlib.util.find_spec(pkg_name)
    if spec is not None and spec.submodule_search_locations:
        return Path(list(spec.submodule_search_locations)[0])
    return pkg_dir / pkg_name


def _clone_and_rename_template(packages_dir, repo_url, pkg_name, pkg_dir):
    """Clone `template_basic_plugin` and rename it to `pkg_name` in place."""
    if pkg_dir.exists():
        print(f"    Package directory already exists: {pkg_dir}")
        return

    packages_dir.mkdir(parents=True, exist_ok=True)
    template_dir = packages_dir / TEMPLATE_NAME

    if not template_dir.exists():
        _run(
            [
                "git", "clone", "--no-tags", "--single-branch",
                f"{repo_url}/{TEMPLATE_NAME}.git",
            ],
            cwd=packages_dir,
        )

    # Rename the outer (repository) directory to the package name.
    shutil.move(str(template_dir), str(pkg_dir))

    # Detach from the upstream template repository (safe if already absent).
    _run(["git", "remote", "remove", "origin"], cwd=pkg_dir, allow_failure=True)

    # Rename the inner import package `my_package` -> `pkg_name`.
    inner_template = pkg_dir / TEMPLATE_PACKAGE_DIR
    inner_target = pkg_dir / pkg_name
    if inner_template.exists() and not inner_target.exists():
        shutil.move(str(inner_template), str(inner_target))


def _fixup_package_metadata(pkg_dir, pkg_name):
    """Replace template placeholders so the package installs as `pkg_name`.

    Mirrors the intro tutorial's find/replace:
        `pyproject.toml` : `my_package` -> `pkg_name`
        `README.md`      : `@package@`  -> `pkg_name`
    """
    replacements = [
        (pkg_dir / "pyproject.toml", TEMPLATE_PACKAGE_DIR),
        (pkg_dir / "README.md", "@package@"),
    ]
    for path, placeholder in replacements:
        if not path.exists():
            continue
        text = path.read_text()
        if placeholder in text:
            path.write_text(text.replace(placeholder, pkg_name))
            print(f"    Updated {path.name}")


def _pip_install_editable(pkg_dir):
    """Editable-install the package (equivalent to `pip install -e`)."""
    _run([sys.executable, "-m", "pip", "install", "-e", str(pkg_dir)])
    # Make the freshly installed package importable in this running kernel.
    importlib.invalidate_caches()


def _install_workshop_infrared(inner_dir):
    """Copy the finished `workshop_infrared.yaml` into the package workflows dir."""
    source = SOLUTIONS_DIR / WORKFLOW_FILENAME
    if not source.exists():
        raise FileNotFoundError(
            f"Expected {WORKFLOW_FILENAME} next to this script at {source}"
        )

    dest_dir = inner_dir / "plugins" / "yaml" / "workflows"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / WORKFLOW_FILENAME

    if dest.exists() and dest.read_bytes() == source.read_bytes():
        print(f"    Workflow already present: {dest}")
        return
    shutil.copyfile(source, dest)
    print(f"    Installed workflow: {dest}")


def _rebuild_registries():
    """Rebuild plugin registries (equivalent to `geoips config create-registries`)."""
    _run(["geoips", "config", "create-registries"])


def ensure_cool_plugins():
    """Set up the `cool_plugins` package and `workshop_infrared`, or verify them.

    Safe to run repeatedly. Returns the resolved inner package directory.
    """
    packages_dir, pkg_name, pkg_dir, repo_url = _resolve_paths()
    print(f"Ensuring '{pkg_name}' is set up under {packages_dir} ...")

    if _package_installed(pkg_name):
        print(f"    '{pkg_name}' is already installed.")
    else:
        print(f"    '{pkg_name}' not found; setting it up from {TEMPLATE_NAME} ...")
        _clone_and_rename_template(packages_dir, repo_url, pkg_name, pkg_dir)
        _fixup_package_metadata(pkg_dir, pkg_name)
        _pip_install_editable(pkg_dir)

    inner_dir = _inner_package_dir(pkg_name, pkg_dir)
    _install_workshop_infrared(inner_dir)
    _rebuild_registries()

    print(
        f"\nDone. '{pkg_name}' is ready and the 'workshop_infrared' workflow is "
        f"installed.\nVerify with: geoips list workflows -p {pkg_name}"
    )
    return inner_dir


if __name__ == "__main__":
    ensure_cool_plugins()