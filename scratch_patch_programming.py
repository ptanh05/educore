import os
import json

base_dir = r"d:\du an\educore\lms\lms\doctype"

# 1. LMS Programming Exercise
exercise_path = os.path.join(base_dir, "lms_programming_exercise", "lms_programming_exercise.json")
with open(exercise_path, "r") as f:
    ex_data = json.load(f)

# Change options for language
for field in ex_data["fields"]:
    if field["fieldname"] == "language":
        field["options"] = "Python\nJavaScript\nJava\nC++\nGo\nRust"

# Add timeout and memory_limit
new_fields = [
    {
        "fieldname": "timeout",
        "fieldtype": "Int",
        "label": "Timeout (seconds)",
        "default": "5"
    },
    {
        "fieldname": "memory_limit",
        "fieldtype": "Int",
        "label": "Memory Limit (MB)",
        "default": "128"
    }
]
if "timeout" not in ex_data["field_order"]:
    ex_data["field_order"].extend(["timeout", "memory_limit"])
    ex_data["fields"].extend(new_fields)

with open(exercise_path, "w") as f:
    json.dump(ex_data, f, indent=1)

# 2. LMS Test Case
test_case_path = os.path.join(base_dir, "lms_test_case", "lms_test_case.json")
with open(test_case_path, "r") as f:
    tc_data = json.load(f)

if "is_hidden" not in tc_data["field_order"]:
    tc_data["field_order"].append("is_hidden")
    tc_data["fields"].append({
        "fieldname": "is_hidden",
        "fieldtype": "Check",
        "label": "Hidden Test Case (Blind Test)",
        "default": "0"
    })
    
with open(test_case_path, "w") as f:
    json.dump(tc_data, f, indent=1)

# 3. LMS Programming Exercise Submission
sub_path = os.path.join(base_dir, "lms_programming_exercise_submission", "lms_programming_exercise_submission.json")
with open(sub_path, "r") as f:
    sub_data = json.load(f)

for field in sub_data["fields"]:
    if field["fieldname"] == "status":
        field["options"] = "Pending\nPassed\nFailed\nError\nTimeout"

new_sub_fields = [
    {
        "fieldname": "score",
        "fieldtype": "Int",
        "label": "Score",
        "read_only": 1
    },
    {
        "fieldname": "error_message",
        "fieldtype": "Code",
        "label": "Compile/Runtime Error",
        "read_only": 1
    }
]

if "score" not in sub_data["field_order"]:
    sub_data["field_order"].insert(sub_data["field_order"].index("status") + 1, "score")
    sub_data["field_order"].insert(sub_data["field_order"].index("score") + 1, "error_message")
    sub_data["fields"].extend(new_sub_fields)

with open(sub_path, "w") as f:
    json.dump(sub_data, f, indent=1)

print("Programming Exercise DocTypes patched successfully!")
