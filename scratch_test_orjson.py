import json
import glob
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
pattern = os.path.join(base_dir, "lms", "lms", "doctype", "*", "*.json")

for f in glob.glob(pattern):
    try:
        with open(f, "r", encoding="utf-8") as file:
            json.load(file)
    except Exception as e:
        print(f"Error in {f}: {e}")

