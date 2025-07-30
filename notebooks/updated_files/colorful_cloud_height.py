"""Module containing colormap for colorful cloud height product."""

import logging

LOG = logging.getLogger(__name__)

interface = "colormappers"
family = "matplotlib"
name = "colorful_cloud_height"


def call(data_range=[0, 20]):
    """Colorful cloud height colormap.

    Parameters
    ----------
    data_range : list of float, default=[0.0, 20]
        Min and max value for colormap.
        Ensure the data range matches the range of the algorithm specified
        for use with this colormap

    Returns
    -------
    mpl_colors_info : dict
        Dictionary of matplotlib plotting parameters, to ensure consistent image output
    """
    min_val = data_range[0]
    max_val = data_range[1]

    if min_val >= 1 or max_val <= 10:
        raise ("cloud height_base range MUST include 1 and 10")

    from geoips.image_utils.colormap_utils import create_linear_segmented_colormap

    transition_vals = [
        (min_val, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 6),
        (6, 8),
        (8, 10),
        (10, 15),
        (15, max_val),
    ]
    transition_colors = [
        ("pink", "red"),
        ("paleturquoise", "teal"),
        ("plum", "rebeccapurple"),
        ("yellow", "chartreuse"),
        ("limegreen", "darkgreen"),
        ("wheat", "darkorange"),
        ("darkgray", "black"),
        ("lightgray", "silver"),
        ("lightskyblue", "deepskyblue"),
    ]

    # ticks = [xx[0] for xx in transition_vals]

    # special selection of label

    ticks = [0, 1, 2, 3, 4, 6, 8, 10, 15, 20]

    # selection of min and max values for colormap if needed
    min_val = transition_vals[0][0]
    max_val = transition_vals[-1][1]

    LOG.info("Setting cmap")
    mpl_cmap = create_linear_segmented_colormap(
        "cmap_cldHeight", min_val, max_val, transition_vals, transition_colors
    )

    LOG.info("Setting norm")
    from matplotlib.colors import Normalize

    mpl_norm = Normalize(vmin=min_val, vmax=max_val)

    cbar_label = "Cloud Height (km)"

    # Must be uniform or proportional, None not valid for Python 3
    cbar_spacing = "proportional"
    mpl_tick_labels = None
    mpl_boundaries = None

    # from geoips.image_utils.mpl_utils import create_colorbar
    # only create colorbar for final imagery
    # cbar = create_colorbar(fig, mpl_cmap, mpl_norm, ticks, cbar_label=cbar_label)
    mpl_colors_info = {
        "cmap": mpl_cmap,
        "norm": mpl_norm,
        "cbar_ticks": ticks,
        "cbar_tick_labels": mpl_tick_labels,
        "cbar_label": cbar_label,
        "boundaries": mpl_boundaries,
        "cbar_spacing": cbar_spacing,
        "colorbar": True,
        "cbar_full_width": True,
    }

    return mpl_colors_info
