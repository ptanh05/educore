# Copyright (c) 2024, Viettel Academy
# License: MIT. See LICENSE

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "name",
			"fieldtype": "Link",
			"label": _("Certificate ID"),
			"options": "LMS Certificate",
			"width": 160,
		},
		{
			"fieldname": "member",
			"fieldtype": "Link",
			"label": _("Learner"),
			"options": "User",
			"width": 150,
		},
		{
			"fieldname": "member_name",
			"fieldtype": "Data",
			"label": _("Learner Name"),
			"width": 160,
		},
		{
			"fieldname": "course",
			"fieldtype": "Link",
			"label": _("Course"),
			"options": "LMS Course",
			"width": 150,
		},
		{
			"fieldname": "course_title",
			"fieldtype": "Data",
			"label": _("Course Title"),
			"width": 200,
		},
		{
			"fieldname": "issue_date",
			"fieldtype": "Date",
			"label": _("Issue Date"),
			"width": 120,
		},
		{
			"fieldname": "expiry_date",
			"fieldtype": "Date",
			"label": _("Expiry Date"),
			"width": 120,
		},
		{
			"fieldname": "template",
			"fieldtype": "Data",
			"label": _("Template"),
			"width": 140,
		},
	]

def get_data(filters=None):
	query_filter = {}
	if filters:
		if filters.get("course"):
			query_filter["course"] = filters.get("course")
		if filters.get("member"):
			query_filter["member"] = filters.get("member")
		if filters.get("from_date"):
			query_filter["issue_date"] = [">=", filters.get("from_date")]
		if filters.get("to_date"):
			if "issue_date" in query_filter:
				query_filter["issue_date"] = ["between", (filters.get("from_date"), filters.get("to_date"))]
			else:
				query_filter["issue_date"] = ["<=", filters.get("to_date")]
	
	records = frappe.get_all(
		"LMS Certificate",
		fields=["name", "member", "member_name", "course", "course_title", "issue_date", "expiry_date", "template"],
		filters=query_filter,
		order_by="issue_date desc"
	)
	
	return records

