"""Reusable widgets for GeoIPS workshop notebooks."""

import os
from pathlib import Path

import ipywidgets as widgets
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import YamlLexer
import yaml


def env_constructor(loader, node):
    """YAML constructor for the ``!ENV`` tag that expands environment variables.

    This function allows YAML files to include environment variables using
    the ``!ENV`` tag. The scalar value associated with the tag is read and
    any environment variables within the string (e.g. ``${VAR_NAME}``) are
    expanded using :func:`os.path.expandvars`.

    Parameters
    ----------
    loader : yaml.Loader
        The YAML loader instance currently parsing the document.
    node : yaml.Node
        The YAML node containing the scalar value associated with the ``!ENV`` tag.

    Returns
    -------
    str
        The scalar value with any environment variables expanded using the
        current process environment.
    """
    value = loader.construct_scalar(node)
    return os.path.expandvars(value)


yaml.SafeLoader.add_constructor("!ENV", env_constructor)


def yaml_editor(
    path: str | Path,
    default_yaml: str = "",
    *,
    height: str = "300px",
) -> widgets.VBox:
    """Return a widget for editing, validating, and saving a YAML file."""

    config_path = Path(path).expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        initial_yaml = config_path.read_text(encoding="utf-8")
    else:
        initial_yaml = default_yaml

    textarea = widgets.Textarea(
        value=initial_yaml,
        description="YAML:",
        layout=widgets.Layout(
            width="100%",
            height=height,
        ),
    )

    save_button = widgets.Button(
        description="Validate and save",
        button_style="primary",
        icon="save",
    )

    status = widgets.Output()

    formatter = HtmlFormatter(
        style="friendly",
        noclasses=True,
    )
    preview = widgets.HTML(
        layout=widgets.Layout(
            width="100%",
            max_height=height,
            overflow="auto",
        )
    )

    def update_preview(_=None):
        preview.value = highlight(
            textarea.value,
            YamlLexer(),
            formatter,
        )

    textarea.observe(update_preview, names="value")
    update_preview()

    def save_yaml(_):
        with status:
            status.clear_output(wait=True)

            try:
                yaml.safe_load(textarea.value)
            except Exception as error:
                save_button.button_style = "danger"
                print("Invalid YAML:")
                print(error)
                return

            # Write to a temporary file first, then atomically replace the
            # destination so an interrupted write cannot corrupt the file.
            temporary_path = config_path.with_name(f".{config_path.name}.tmp")
            temporary_path.write_text(
                textarea.value,
                encoding="utf-8",
            )
            temporary_path.replace(config_path)

            save_button.button_style = "success"
            print(f"Saved valid YAML to {config_path}")

    save_button.on_click(save_yaml)

    return widgets.VBox(
        [
            textarea,
            widgets.HTML("<strong>Syntax-highlighted preview</strong>"),
            preview,
            save_button,
            status,
        ]
    )
