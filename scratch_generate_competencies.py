import os
import json
from datetime import datetime

base_dir = r"d:\du an\educore\lms\lms\doctype"

def create_doctype(name, is_child, fields, title_field=None):
    folder_name = name.lower().replace(" ", "_")
    doctype_dir = os.path.join(base_dir, folder_name)
    os.makedirs(doctype_dir, exist_ok=True)
    
    with open(os.path.join(doctype_dir, "__init__.py"), "w") as f: pass
    
    with open(os.path.join(doctype_dir, f"{folder_name}.py"), "w") as f:
        f.write(f"""import frappe\nfrom frappe.model.document import Document\n\nclass {name.replace(' ', '')}(Document):\n\tpass\n""")
        
    json_data = {
        "actions": [],
        "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "doctype": "DocType",
        "engine": "InnoDB",
        "field_order": [f.get("fieldname") for f in fields],
        "fields": fields,
        "istable": 1 if is_child else 0,
        "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "modified_by": "Administrator",
        "module": "LMS",
        "name": name,
        "owner": "Administrator",
        "permissions": [],
        "sort_field": "modified",
        "sort_order": "DESC",
        "track_changes": 1
    }
    
    if not is_child:
        json_data["autoname"] = f"field:{fields[0]['fieldname']}"
        json_data["permissions"] = [{
            "create": 1, "delete": 1, "email": 1, "export": 1, 
            "print": 1, "read": 1, "report": 1, "role": "System Manager", 
            "share": 1, "write": 1
        }, {
            "read": 1, "role": "LMS Student"
        }]
    
    with open(os.path.join(doctype_dir, f"{folder_name}.json"), "w") as f:
        json.dump(json_data, f, indent=1)


# 1. LMS Competency
create_doctype("LMS Competency", False, [
    {"fieldname": "competency_name", "fieldtype": "Data", "label": "Competency Name", "reqd": 1, "unique": 1},
    {"fieldname": "description", "fieldtype": "Text", "label": "Description"}
])

# 2. LMS Skill
create_doctype("LMS Skill", False, [
    {"fieldname": "skill_name", "fieldtype": "Data", "label": "Skill Name", "reqd": 1, "unique": 1},
    {"fieldname": "competency", "fieldtype": "Link", "label": "Competency", "options": "LMS Competency", "reqd": 1},
    {"fieldname": "description", "fieldtype": "Text", "label": "Description"}
])

# 3. LMS Skill Requirement (Child Table)
create_doctype("LMS Skill Requirement", True, [
    {"fieldname": "skill", "fieldtype": "Link", "label": "Skill", "options": "LMS Skill", "in_list_view": 1, "reqd": 1},
    {"fieldname": "required_level", "fieldtype": "Int", "label": "Required Level", "in_list_view": 1, "reqd": 1, "description": "e.g. 1-5"}
])

# 4. LMS Role Profile
create_doctype("LMS Role Profile", False, [
    {"fieldname": "position", "fieldtype": "Data", "label": "Position Name", "reqd": 1, "unique": 1},
    {"fieldname": "skills", "fieldtype": "Table", "label": "Required Skills", "options": "LMS Skill Requirement"}
])

# 5. LMS Course Skill (Child Table)
create_doctype("LMS Course Skill", True, [
    {"fieldname": "skill", "fieldtype": "Link", "label": "Skill", "options": "LMS Skill", "in_list_view": 1, "reqd": 1},
    {"fieldname": "level_awarded", "fieldtype": "Int", "label": "Level Awarded", "in_list_view": 1, "reqd": 1}
])

# 6. LMS Member Skill
create_doctype("LMS Member Skill", False, [
    {"fieldname": "member_skill_id", "fieldtype": "Data", "label": "ID", "hidden": 1},
    {"fieldname": "member", "fieldtype": "Link", "label": "Member", "options": "User", "reqd": 1, "in_list_view": 1},
    {"fieldname": "skill", "fieldtype": "Link", "label": "Skill", "options": "LMS Skill", "reqd": 1, "in_list_view": 1},
    {"fieldname": "achieved_level", "fieldtype": "Int", "label": "Achieved Level", "reqd": 1, "in_list_view": 1},
    {"fieldname": "source", "fieldtype": "Data", "label": "Source (e.g. Course Name)"}
])
# Update Member Skill autoname to format instead of field
ms_path = os.path.join(base_dir, "lms_member_skill", "lms_member_skill.json")
with open(ms_path, "r") as f: ms_data = json.load(f)
ms_data["autoname"] = "format:{member}-{skill}"
ms_data["field_order"].remove("member_skill_id")
ms_data["fields"] = [f for f in ms_data["fields"] if f["fieldname"] != "member_skill_id"]
with open(ms_path, "w") as f: json.dump(ms_data, f, indent=1)


# 7. Patch LMS Course to include LMS Course Skill
course_path = os.path.join(base_dir, "lms_course", "lms_course.json")
with open(course_path, "r") as f:
    course_data = json.load(f)

if "skills" not in course_data["field_order"]:
    course_data["field_order"].append("skills")
    course_data["fields"].append({
        "fieldname": "skills",
        "fieldtype": "Table",
        "label": "Skills Awarded on Completion",
        "options": "LMS Course Skill"
    })
    with open(course_path, "w") as f:
        json.dump(course_data, f, indent=1)

print("Competency DocTypes generated successfully!")
