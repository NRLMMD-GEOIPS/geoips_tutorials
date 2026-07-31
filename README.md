# GeoIPS Workshop Tutorials

Installation
------------
If you've not yet installed GeoIPS, please follow the following installation
instructions before continuing. GeoIPS does not need to be installed in editable mode
unless you plan to actively develop the core package.

Non-editable Instructions:

```bash
pip install geoips
```

Editable Instructions:

[Please visit this folder to find the correct installation instructions for your machine](https://github.com/NRLMMD-GEOIPS/geoips/tree/main/docs/source/contribute).

Once you've installed GeoIPS, go ahead and install this package as well. If you have
``$GEOIPS_PACKAGES_DIR`` set as an environment variable, you can run the following command:

```bash
pip install -e $GEOIPS_PACKAGES_DIR/geoips_tutorials
```

Otherwise, navigate to the location you cloned this package and run:
```bash
pip install -e .
```

Running the tutorials
---------------------

Most of our tutorials make use of Jupyter Notebooks. Make sure you follow the
instructions laid out below for interactive code cell blocks.

I would recommend beginning with the following tutorial. It builds nicely into the
tutorials which follow afterwards.

[Click Here to visit that tutorial](./notebooks/2026-Intro-and-algorithms.ipynb).


`output_formatter` Tutorial
---------------------------
Access the slides [here](https://docs.google.com/presentation/d/1wFbrP4RBdwf6Hx30adD9DN4jNZm1f0hVaHxV--encS0/edit?usp=sharing)

## Workshop file editors

The `workshop_utils` package provides notebook widgets for editing YAML and
Python files. Each editor loads an existing file without changing it. If the
file does not exist, the supplied default text is shown instead. Nothing is
written until **Validate and save** is selected.

Both widgets have the same layout:

```text
┌───────────────────────────────────────┐
│ Editable source text                  │
├───────────────────────────────────────┤
│ Live syntax-highlighted preview       │
├───────────────────────────────────────┤
│ [ Validate and save ]                 │
├───────────────────────────────────────┤
│ Validation or save status             │
└───────────────────────────────────────┘
```

### YAML editor

Run the following in a notebook cell:

```python
from workshop_utils import yaml_editor

yaml_editor(
    "~/workshop/config.yaml",
    default_yaml="""\
reader:
  name: abi_netcdf

output:
  format: png
""",
)
```

Edit the YAML, review the highlighted preview, and select **Validate and
save**. Invalid YAML is reported and the file is not overwritten.

Read the saved file in a later cell:

```python
from pathlib import Path

import yaml

config_path = Path("~/workshop/config.yaml").expanduser()
with config_path.open() as stream:
    config = yaml.safe_load(stream)
```

### Python editor

Run the following in a notebook cell:

```python
from workshop_utils import python_editor

python_editor(
    "~/workshop/example.py",
    default_python="""\
def greet(name):
    return f"Hello, {name}!"
""",
)
```

The Python editor uses `ast.parse` to check syntax before saving. It does not
execute the edited code. Syntax errors are reported and the existing file is
left unchanged.

After changing an imported Python file, restart the notebook kernel or reload
the module before using the updated code:

```python
import importlib
import example

importlib.reload(example)
```
