FOUND_RELMGR=True

APP_VERSION = 1.94
BETA = "1"  # leave blank to turn off beta
APP_VERSION_FULL = f"{APP_VERSION}"
if BETA:
    APP_VERSION_FULL += f"-{BETA}" 

dummy1 = 1.9
dummy2 = 20.98

import os
try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []
print("CWD", os.getcwd())
print("PYTHONPATH", user_paths)

try:
    from relmgr.relationship_manager import RelationshipManager
except ModuleNotFoundError:
    FOUND_RELMGR=False
else:
    FOUND_RELMGR = True

print("FOUND_RELMGR:", FOUND_RELMGR)

APP_ICON_PATH = "icons/xx.ico"
