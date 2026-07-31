"""Reusable Python editor widget for GeoIPS workshop notebooks."""

import ast
from pathlib import Path

import ipywidgets as widgets
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


def python_editor(
    path: str | Path,
    default_python: str = "",
    *,
    height: str = "300px",
) -> widgets.VBox:
    """Return a widget for editing, validating, and saving a Python file."""
    python_path = Path(path).expanduser()
    python_path.parent.mkdir(parents=True, exist_ok=True)

    if python_path.exists():
        initial_python = python_path.read_text(encoding="utf-8")
    else:
        initial_python = default_python

    textarea = widgets.Textarea(
        value=initial_python,
        description="Python:",
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
            PythonLexer(),
            formatter,
        )

    textarea.observe(update_preview, names="value")
    update_preview()

    def save_python(_):
        with status:
            status.clear_output(wait=True)

            try:
                ast.parse(textarea.value, filename=str(python_path))
            except SyntaxError as error:
                save_button.button_style = "danger"
                print(f"Syntax error on line {error.lineno}:")
                print(error.msg)
                return

            temporary_path = python_path.with_name(f".{python_path.name}.tmp")
            temporary_path.write_text(
                textarea.value,
                encoding="utf-8",
            )
            temporary_path.replace(python_path)

            save_button.button_style = "success"
            print(f"Saved valid Python to {python_path}")

    save_button.on_click(save_python)

    return widgets.VBox(
        [
            textarea,
            widgets.HTML("<strong>Syntax-highlighted preview</strong>"),
            preview,
            save_button,
            status,
        ]
    )
