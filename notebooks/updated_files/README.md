    # # # This source code is subject to the license referenced at
    # # # https://github.com/NRLMMD-GEOIPS.

Basic GeoIPS Plugin Template
=============================

This template repository contains everything necessary to create a fully
compatible GeoIPS Plugin Package.  Each file within this repository contains
appropriate modification instructions.

To create your own functional plugin for GeoIPS, follow the
[step by step instructions](./docs/source/userguide/template_instructions.rst) for
modifying the template files within this repo.

@ Once this repository has been set up properly, you can remove this "Basic
GeoIPS Plugin Template" section in the README.md, leaving the appropriate
content for your package's README file.


cool_plugins GeoIPS Plugin
==========================

The cool_plugins package is a GeoIPS-compatible plugin, intended to be used within
the GeoIPS ecosystem.  Please see the
[GeoIPS Documentation](https://github.com/NRLMMD-GEOIPS/geoips#readme) for
more information on the GeoIPS plugin architecture and base infrastructure.

Package Overview
-----------------

The cool_plugins plugin provides the capability for

@ Please include a brief description of what capability this package provides.

@ This section should be no more than 1-2 paragraphs, if you have additional
@ information to include, please include in a "docs" subdirectory.

@ Example overview:

@ The template_basic_plugin package provides template files which can be used to create
@ a fully compatible GeoIPS plugin.  This template repository is focused on basic functionality -
@ ie, simple readers, products, output formats, etc.  Additional template repositories will be
@ created for more sophisticated and complicated use cases.

System Requirements
---------------------

* geoips >= 1.14.2
* Test data repos contained in $GEOIPS_TESTDATA_DIR for tests to pass.
* @ Add any additional system requirements, such as gfortran, etc

IF REQUIRED: Install base geoips package
------------------------------------------------------------
SKIP IF YOU HAVE ALREADY INSTALLED BASE GEOIPS ENVIRONMENT

If GeoIPS Base is not yet installed, follow the
[installation instructions](https://github.com/NRLMMD-GEOIPS/geoips#installation)
within the geoips source repo documentation:

Install cool_plugins package
----------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # Clone and install cool_plugins
    git clone https://github.com/NRLMMD-GEOIPS/cool_plugins $GEOIPS_PACKAGES_DIR/cool_plugins
    pip install -e $GEOIPS_PACKAGES_DIR/cool_plugins

    # Add any additional clone/install/setup steps here
```

Test cool_plugins installation
-----------------------------
```bash

    # Ensure GeoIPS Python environment is enabled.

    # This script will run ALL tests within this package
    $GEOIPS_PACKAGES_DIR/cool_plugins/tests/test_all.sh

    # Individual direct test calls, for reference
    $GEOIPS_PACKAGES_DIR/cool_plugins/tests/scripts/<test_script_name>.sh
```
