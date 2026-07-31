"""Channel mapping module for GeoIPS geostationary readers."""

GOES_ABI = {
    "LOW": [
        "B04Rad",
        "B04Ref",  # 1.37um Near-IR Cirrus
        "B06Rad",
        "B06Ref",  # 2.2um  Near-IR Cloud Particle Size
        "B07Rad",
        "B07BT",  # 3.9um  IR      Shortwave Window
        "B08Rad",
        "B08BT",  # 6.2um  IR      Upper-level tropospheric water vapor
        "B09Rad",
        "B09BT",  # 6.9um  IR      Mid-level water vapor
        "B10Rad",
        "B10BT",  # 7.3um  IR      Lower-level Water Vapor
        "B11Rad",
        "B11BT",  # 8.4um  IR      Cloud-top phase
        "B12Rad",
        "B12BT",  # 9.6um  IR      Ozone
        "B13Rad",
        "B13BT",  # 10.3um IR      Clean IR Longwave Window
        "B14Rad",
        "B14BT",  # 11.2um IR      IR Longwave window
        "B15Rad",
        "B15BT",  # 12.3um IR      Dirty Longwave Window
        "B16Rad",
        "B16BT",
    ],  # 13.3um IR      CO2 Longwave infrared
    "MED": [
        "B01Rad",
        "B01Ref",  # 0.47um Vis     Blue
        "B02Rad",
        "B02Ref",  # 0.64um Vis     Red
        "B05Rad",
        "B05Ref",
    ],  # 1.6um  Near-IR Snow/Ice
    "HIGH": ["B03Rad", "B03Ref"],  # 0.86um Near-IR Veggie
}

HIMAWARI_AHI = {
    "LOW": [
        "B05Rad",
        "B05Ref",  # 1.61um
        "B06Rad",
        "B06Ref",  # 2.267um
        "B07Rad",
        "B07BT",  # 3.8853um
        "B08Rad",
        "B08BT",  # 6.2429um
        "B09Rad",
        "B09BT",  # 6.9410um
        "B10Rad",
        "B10BT",  # 7.3467um
        "B11Rad",
        "B11BT",  # 8.5926um
        "B12Rad",
        "B12BT",  # 9.6372um
        "B13Rad",
        "B13BT",  # 10.4073um
        "B14Rad",
        "B14BT",  # 11.2395um
        "B15Rad",
        "B15BT",  # 12.3806um
        "B16Rad",
        "B16BT",
    ],  # 13.2807um
    "MED": [
        "B01Rad",
        "B01Ref",  # 0.47063um
        "B02Rad",
        "B02Ref",  # 0.51000um
        "B04Rad",
        "B04Ref",
    ],  # 0.85670um
    "HIGH": ["B03Rad", "B03Ref"],  # 0.63914um
}

METEOSAT_FCI = {
    "B01Ref": "vis_04",
    "B01Rad": "vis_04",
    "B02Ref": "vis_05",
    "B02Rad": "vis_05",
    "B03Ref": "vis_06",
    "B03Rad": "vis_06",
    "B04Ref": "vis_08",
    "B04Rad": "vis_08",
    "B05Ref": "vis_09",
    "B05Rad": "vis_09",
    "B06Ref": "nir_13",
    "B06Rad": "nir_13",
    "B07Ref": "nir_16",
    "B07Rad": "nir_16",
    "B08Ref": "nir_22",
    "B08Rad": "nir_22",
    "B09BT": "ir_38",
    "B09Rad": "ir_38",
    "B10BT": "wv_63",
    "B10Rad": "wv_63",
    "B11BT": "wv_73",
    "B11Rad": "wv_73",
    "B12BT": "ir_87",
    "B12Rad": "ir_87",
    "B13BT": "ir_97",
    "B13Rad": "ir_97",
    "B14BT": "ir_105",
    "B14Rad": "ir_105",
    "B15BT": "ir_123",
    "B15Rad": "ir_123",
    "B16BT": "ir_133",
    "B16Rad": "ir_133",
    "HRB03Ref": "vis_06_hr",
    "HRB03Rad": "vis_06_hr",
    "HRB09BT": "ir_38_hr",
    "HRB09Rad": "ir_38_hr",
    "HRB14BT": "ir_105_hr",
    "HRB14Rad": "ir_105_hr",
}

METEOSAT_SEVIRI = [
    "B01Rad",
    "B01Ref",  # VIS0.6 Cloud mapping
    "B02Rad",
    "B02Ref",  # VIS0.8 Vegetation index
    "B03Rad",
    "B03Ref",  # NIR1.6 Cloud / snow discrimination
    "B04Rad",
    "B04BT",  # IR3.9  Atmospheric window
    "B05Rad",
    "B05BT",  # IR6.2  Water vapour channel (Upper atmosphere)
    "B06Rad",
    "B06BT",  # IR7.3  Water vapour channel (Lower atmosphere)
    "B07Rad",
    "B07BT",  # IR8.7  Atmospheric window
    "B08Rad",
    "B08BT",  # IR9.7  Ozone channel
    "B09Rad",
    "B09BT",  # IR10.8 Atmospheric window
    "B10Rad",
    "B10BT",  # IR12.0 Atmospheric window
    "B11Rad",
    "B11BT",  # IR13.4 Carbon dioxide channel
]
