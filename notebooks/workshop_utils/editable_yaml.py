"""Reusable widgets for GeoIPS workshop notebooks."""

from pathlib import Path

import ipywidgets as widgets
import yaml


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

    def save_yaml(_):
        with status:
            status.clear_output(wait=True)

            try:
                yaml.safe_load(textarea.value)
            except yaml.YAMLError as error:
                save_button.button_style = "danger"
                print("Invalid YAML:")
                print(error)
                return

            # Write to a temporary file first, then atomically replace the
            # destination so an interrupted write cannot corrupt the file.
            temporary_path = config_path.with_name(
                f".{config_path.name}.tmp"
            )
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
            save_button,
            status,
        ]
    )