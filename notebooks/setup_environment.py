"""Set up very simple environment variables for the beginner tutorial."""

with open("./.env", "w") as env_file:
    env_file.writelines(
        [
            f"GEOIPS_TESTDATA_DIR=~/test_data\n",
            f"GEOIPS_OUTDIRS=~/outdirs",
        ],
    )
