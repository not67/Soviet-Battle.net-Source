from gc import get_stats
import os
from helpers.hash import md5
from helpers.ostype import OSType, get_os
ACCOUNT_GENERATION_BASEURL = "https://account.battle.net/creation/flow/creation-full"

# Retrieve TMP folder based on os

TMP_FOLDER = "/tmp/" if get_os() == OSType.LINUX else r"C:\\Temp\\"

# Create TMP_FOLDER if it does not exist
if not os.path.exists(TMP_FOLDER):
    os.makedirs(TMP_FOLDER)


def get_ini():
    config = {}
    # Parse config from config.ini
    with open("config.ini", "r") as f:
        for line in f.readlines():
            first_char = line[0]
            # Verify that the first char is a letter
            if first_char.isalpha():
                # Remove the newline char
                line = line.replace("\n", "")
                # Split the line into a list
                line = line.split("=", 1)
                # Get the key and value
                key = line[0].strip()
                value = line[1].split("#")[0].strip()
                # Add the key and value to the config dict
                if value == "true":
                    config[key] = True
                elif value == "false":
                    config[key] = False
                elif value.isnumeric():
                    config[key] = int(value)
                else:
                    config[key] = value
    return config


INI_CONFIG = get_ini()
