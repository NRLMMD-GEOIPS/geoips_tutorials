"""Pass."""

import nbformat


def merge_notebooks_clean(nb1_path, nb2_path, output_path):
    """Pass."""
    # Load both notebooks
    nb1 = nbformat.read(nb1_path, as_version=4)
    nb2 = nbformat.read(nb2_path, as_version=4)

    # Append cells from nb2 to nb1
    nb1.cells.extend(nb2.cells)

    # Strip outputs and reset execution counts
    for cell in nb1.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None

    # Save as clean merged notebook
    nbformat.write(nb1, output_path)


merge_notebooks_clean(
    "Beginner_Tutorial_Part_1.ipynb",
    "Beginner_Tutorial_Part_2.ipynb",
    "combined_beginner_tutorial.ipynb",
)
