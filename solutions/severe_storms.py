"""Severe Storms WMO RGB recipe."""

from geoips.interfaces.class_based.algorithms import BaseAlgorithmPlugin

import logging

LOG = logging.getLogger(__name__)


class SevereStormsAlgorithmPlugin(BaseAlgorithmPlugin):
    """Severe Storms WMO RGB recipe."""

    interface = "algorithms"
    family = "xarray_to_numpy"
    name = "severe_storms"

    def call(self, xobj, red, green, blue):
        """Apply WMO's Severe Storms RGB recipe.

        Parameters
        ----------
        xobj : xarray.Dataset
            The dataset containing variables needed for the severe storms rgb recipe.
        red : dict
            A dictionary containing {'range', 'units', 'gamma'} key value pairs which
            define the parameters to the red gun of a RGB recipe.
        green : dict
            A dictionary containing {'range', 'units', 'gamma'} key value pairs which
            define the parameters to the green gun of a RGB recipe.
        blue : dict
            A dictionary containing {'range', 'units', 'gamma'} key value pairs which
            define the parameters to the blue gun of a RGB recipe.

        Returns
        -------
        numpy.ndarray
            numpy.ndarray or numpy.MaskedArray of qualitative RGBA image output
        """
        rparams = red
        gparams = green
        bparams = blue

        red = xobj["B08BT"].to_masked_array() - xobj["B10BT"].to_masked_array()
        grn = xobj["B07BT"].to_masked_array() - xobj["B13BT"].to_masked_array()
        blu = xobj["B05Ref"].to_masked_array() - xobj["B02Ref"].to_masked_array()

        # Ensure red and green guns are in Kelvin units
        from geoips.data_manipulations.conversions import unit_conversion

        red = unit_conversion(red, input_units="Kelvin", output_units=rparams["units"])
        grn = unit_conversion(grn, input_units="Kelvin", output_units=gparams["units"])
        # No unit conversion needed to be applied to blue gun

        from geoips.data_manipulations.corrections import apply_data_range, apply_gamma

        data_range = rparams["range"]
        gamma = rparams["gamma"]
        red = apply_data_range(
            red,
            min_val=data_range[0],
            max_val=data_range[1],
            min_outbounds="crop",
            max_outbounds="crop",
            norm=True,
            inverse=False,
        )
        red = apply_gamma(red, gamma)

        data_range = gparams["range"]
        gamma = gparams["gamma"]
        grn = apply_data_range(
            grn,
            min_val=data_range[0],
            max_val=data_range[1],
            min_outbounds="crop",
            max_outbounds="crop",
            norm=True,
            inverse=False,
        )
        grn = apply_gamma(grn, gamma)

        data_range = bparams["range"]
        gamma = bparams["gamma"]
        blu = apply_data_range(
            blu,
            min_val=data_range[0],
            max_val=data_range[1],
            min_outbounds="crop",
            max_outbounds="crop",
            norm=True,
            inverse=False,
        )
        blu = apply_gamma(blu, gamma)

        from geoips.image_utils.mpl_utils import (
            alpha_from_masked_arrays,
            rgba_from_arrays,
        )

        alp = alpha_from_masked_arrays([red, grn, blu])
        rgba = rgba_from_arrays(red, grn, blu, alp)

        return rgba


# Tells pluginify (plugin registry package) what object is the actual plugin we want to
# add to the registry
PLUGIN_CLASS = SevereStormsAlgorithmPlugin
