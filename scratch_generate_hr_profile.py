import os
import json
from datetime import datetime

doctype_name = "HR Employee Profile"
folder_name = doctype_name.lower().replace(" ", "_")
base_dir = r"d:\du an\educore\lms\lms\doctype"
doctype_dir = os.path.join(base_dir, folder_name)
os.makedirs(doctype_dir, exist_ok=True)

# __init__.py
with open(os.path.join(doctype_dir, "__init__.py"), "w") as f:
    pass

# JSON
json_data = {
    "actions": [],
    "autoname": "field:external_user_id",
    "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "doctype": "DocType",
    "engine": "InnoDB",
    "field_order": [
        "external_user_id",
        "employee_code",
        "user",
        "email",
        "full_name",
        "column_break_1",
        "department",
        "position",
        "manager",
        "status"
    ],
    "fields": [
        {
            "fieldname": "external_user_id",
            "fieldtype": "Data",
            "label": "External User ID",
            "reqd": 1,
            "unique": 1
        },
        {
            "fieldname": "employee_code",
            "fieldtype": "Data",
            "label": "Employee Code"
        },
        {
            "fieldname": "email",
            "fieldtype": "Data",
            "label": "Email",
            "options": "Email",
            "reqd": 1
        },
        {
            "fieldname": "user",
            "fieldtype": "Link",
            "label": "Linked User",
            "options": "User",
            "read_only": 1
        },
        {
            "fieldname": "full_name",
            "fieldtype": "Data",
            "label": "Full Name",
            "reqd": 1
        },
        {
            "fieldname": "column_break_1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "department",
            "fieldtype": "Data",
            "label": "Department"
        },
        {
            "fieldname": "position",
            "fieldtype": "Data",
            "label": "Position"
        },
        {
            "fieldname": "manager",
            "fieldtype": "Data",
            "label": "Manager (Email)"
        },
        {
            "default": "Active",
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "Status",
            "options": "Active\\nInactive"
        }
    ],
    "index_web_pages_for_search": 1,
    "links": [],
    "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    "modified_by": "Administrator",
    "module": "LMS",
    "name": doctype_name,
    "owner": "Administrator",
    "permissions": [
        {
            "create": 1,
            "delete": 1,
            "email": 1,
            "export": 1,
            "print": 1,
            "read": 1,
            "report": 1,
            "role": "System Manager",
            "share": 1,
            "write": 1
        }
    ],
    "sort_field": "modified",
    "sort_order": "DESC",
    "track_changes": 1
}

with open(os.path.join(doctype_dir, f"{folder_name}.json"), "w") as f:
    json.dump(json_data, f, indent=1)

# JS
js_content = f'''// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt

frappe.ui.form.on("{doctype_name}", {{
	refresh(frm) {{
	}}
}});
'''
with open(os.path.join(doctype_dir, f"{folder_name}.js"), "w") as f:
    f.write(js_content)

# PY
py_content = f'''# Copyright (c) 2024, Viettel Academy
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document

class HREmployeeProfile(Document):
	def on_update(self):
		self.sync_with_user()
		self.assign_learning_paths()
		
	def sync_with_user(self):
		if not self.email:
			return
			
		user_exists = frappe.db.exists("User", self.email)
		if not user_exists:
			user = frappe.new_doc("User")
			user.email = self.email
			user.first_name = self.full_name
			user.send_welcome_email = 0
			user.insert(ignore_permissions=True)
		else:
			user = frappe.get_doc("User", self.email)
			
		# Sync details
		if self.full_name != user.full_name or (self.status == "Inactive" and user.enabled) or (self.status == "Active" and not user.enabled):
			user.first_name = self.full_name
			user.enabled = 1 if self.status == "Active" else 0
			user.save(ignore_permissions=True)
			
		# Map to our user field
		if self.user != self.email:
			self.db_set("user", self.email)
			
		# Assign default role if Active
		if self.status == "Active":
			if not frappe.db.exists("Has Role", {{"parent": self.email, "role": "LMS Student"}}):
				user.append("roles", {{"role": "LMS Student"}})
				user.save(ignore_permissions=True)
				
		# Optional: Set department/designation on User if fields exist in schema
		try:
			if hasattr(user, "department"):
				frappe.db.set_value("User", self.email, "department", self.department)
		except Exception:
			pass

	def assign_learning_paths(self):
		if self.status != "Active":
			return
			
		# Find matching programs based on department or position
		programs = frappe.get_all("LMS Program", filters={{"published": 1}}, fields=["name", "department", "position"])
		
		for p in programs:
			match = False
			if p.department and self.department and p.department.lower() == self.department.lower():
				match = True
			if p.position and self.position and p.position.lower() == self.position.lower():
				match = True
				
			if match:
				# Enroll
				if not frappe.db.exists("LMS Program Member", {{"parent": p.name, "member": self.email}}):
					program = frappe.get_doc("LMS Program", p.name)
					program.append("members", {{
						"member": self.email,
						"status": "Not Started",
						"assignment_source": "HR Sync"
					}})
					program.save(ignore_permissions=True)

'''
with open(os.path.join(doctype_dir, f"{folder_name}.py"), "w") as f:
    f.write(py_content)
