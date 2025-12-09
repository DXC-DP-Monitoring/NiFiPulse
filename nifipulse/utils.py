import os
from datetime import datetime

def abs_ff_path(relpath):
    abspath = os.path.abspath(relpath)
    return abspath

def path_tofile(file):
    abspath = abs_ff_path(file)
    # debug point print("Checking file:", abspath)
    return os.path.isfile(abspath)

def path_tofolder(folder):
    abspath = abs_ff_path(folder)
    return os.path.isdir(abspath)

def _csv_has_rows(path):
    try:
        with open(path, "r", newline="") as f:
            next(f, None)  # skip header
            return any(True for _ in f)
    except FileNotFoundError:
        return False