import orjson
import glob
for f in glob.glob('/home/frappe/frappe-bench/apps/lms/lms/lms/doctype/*/*.json'):
    try:
        orjson.loads(open(f, 'rb').read())
    except Exception as e:
        print(f"Error in {f}: {e}")
