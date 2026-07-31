import os
import json
from datetime import datetime

reports_to_create = [
    {
        "name": "Program Progress Report",
        "ref_doctype": "LMS Program Member",
        "columns": "[]",
        "filters": """[
            { "fieldname": "program", "label": __("Program"), "fieldtype": "Link", "options": "LMS Program" },
            { "fieldname": "department", "label": __("Department"), "fieldtype": "Data" },
            { "fieldname": "status", "label": __("Status"), "fieldtype": "Select", "options": "\\nNot Started\\nIn Progress\\nCompleted\\nOverdue" }
        ]"""
    },
    {
        "name": "Department Training Report",
        "ref_doctype": "LMS Enrollment",
        "columns": "[]",
        "filters": """[
            { "fieldname": "department", "label": __("Department"), "fieldtype": "Data" },
            { "fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date" },
            { "fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date" }
        ]"""
    },
    {
        "name": "Learner Detail Report",
        "ref_doctype": "LMS Enrollment",
        "columns": "[]",
        "filters": """[
            { "fieldname": "member", "label": __("Learner"), "fieldtype": "Link", "options": "User" }
        ]"""
    },
    {
        "name": "Certificate Report",
        "ref_doctype": "LMS Certificate",
        "columns": "[]",
        "filters": """[
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" },
            { "fieldname": "member", "label": __("Learner"), "fieldtype": "Link", "options": "User" },
            { "fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date" },
            { "fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date" }
        ]"""
    },
    {
        "name": "Quiz Performance Report",
        "ref_doctype": "LMS Quiz Submission",
        "columns": "[]",
        "filters": """[
            { "fieldname": "quiz", "label": __("Quiz"), "fieldtype": "Link", "options": "LMS Quiz" },
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" }
        ]"""
    },
    {
        "name": "Assignment Status Report",
        "ref_doctype": "LMS Assignment Submission",
        "columns": "[]",
        "filters": """[
            { "fieldname": "assignment", "label": __("Assignment"), "fieldtype": "Link", "options": "LMS Assignment" },
            { "fieldname": "status", "label": __("Status"), "fieldtype": "Select", "options": "\\nPending\\nEvaluated" }
        ]"""
    },
    {
        "name": "Instructor Effectiveness Report",
        "ref_doctype": "LMS Course Review",
        "columns": "[]",
        "filters": """[
            { "fieldname": "instructor", "label": __("Instructor"), "fieldtype": "Link", "options": "User" },
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" }
        ]"""
    }
]

base_dir = r"d:\du an\educore\lms\lms\report"

for rep in reports_to_create:
    folder_name = rep["name"].lower().replace(" ", "_")
    report_dir = os.path.join(base_dir, folder_name)
    os.makedirs(report_dir, exist_ok=True)
    
    # __init__.py
    with open(os.path.join(report_dir, "__init__.py"), "w") as f:
        pass
    
    # JSON
    json_data = {
        "add_total_row": 0,
        "columns": [],
        "creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "disable_prepared_report": 0,
        "disabled": 0,
        "docstatus": 0,
        "doctype": "Report",
        "filters": [],
        "idx": 0,
        "is_standard": "Yes",
        "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "modified_by": "Administrator",
        "module": "LMS",
        "name": rep["name"],
        "owner": "Administrator",
        "prepared_report": 0,
        "ref_doctype": rep["ref_doctype"],
        "report_name": rep["name"],
        "report_type": "Script Report",
        "roles": [{"role": "System Manager"}, {"role": "Moderator"}]
    }
    with open(os.path.join(report_dir, f"{folder_name}.json"), "w") as f:
        json.dump(json_data, f, indent=1)
        
    # JS
    js_content = f'''// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["{rep["name"]}"] = {{
	filters: {rep["filters"]}
}};
'''
    with open(os.path.join(report_dir, f"{folder_name}.js"), "w") as f:
        f.write(js_content)
        
    # PY
    py_content = f'''# Copyright (c) 2024, Viettel Academy
# License: MIT. See LICENSE

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": _("ID"),
			"options": "{rep["ref_doctype"]}",
			"width": 200,
		}}
	]

def get_data(filters=None):
	conditions = ""
	# TODO: Add dynamic filters based on filters dict
	
	records = frappe.get_all(
		"{rep["ref_doctype"]}",
		fields=["name"],
		filters=filters
	)
	
	return records
'''
    with open(os.path.join(report_dir, f"{folder_name}.py"), "w") as f:
        f.write(py_content)
