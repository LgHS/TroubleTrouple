import json

import os.path
from pathlib import Path

script_path = Path(__file__).parent.absolute()
dict_path = os.path.join(script_path, "dic.txt")
setup_path = os.path.join(script_path, "setup.json")