"""Set up very simple environment variables for the beginner tutorial."""

with open("./.env", "w") as env_file:
    env_file.writelines(
        [
            "GEOIPS_TESTDATA_DIR=~/test_data\n",
            "GEOIPS_OUTDIRS=~/outdirs",
        ],
    )
