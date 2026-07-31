import os
import glob
import json

base_dir = r"d:\du an\educore\lms\lms\doctype"
for f in glob.glob(os.path.join(base_dir, "*", "*.json")):
    with open(f, "rb") as fp:
        content = fp.read()
    try:
        json.loads(content)
    except Exception as e:
        print(f"Error in {f}: {e}")
