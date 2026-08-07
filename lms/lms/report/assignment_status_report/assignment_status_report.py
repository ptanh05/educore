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
			"label": _("Submission ID"),
			"options": "LMS Assignment Submission",
			"width": 160,
		},
		{
			"fieldname": "assignment",
			"fieldtype": "Link",
			"label": _("Assignment"),
			"options": "LMS Assignment",
			"width": 180,
		},
		{
			"fieldname": "assignment_title",
			"fieldtype": "Data",
			"label": _("Assignment Title"),
			"width": 200,
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
			"fieldname": "status",
			"fieldtype": "Data",
			"label": _("Status"),
			"width": 120,
		},
		{
			"fieldname": "score",
			"fieldtype": "Int",
			"label": _("Score"),
			"width": 90,
		},
		{
			"fieldname": "creation",
			"fieldtype": "Datetime",
			"label": _("Submitted On"),
			"width": 160,
		},
	]

def get_data(filters=None):
	query_filter = {}
	if filters:
		if filters.get("assignment"):
			query_filter["assignment"] = filters.get("assignment")
		if filters.get("status"):
			query_filter["status"] = filters.get("status")
	
	records = frappe.get_all(
		"LMS Assignment Submission",
		fields=["name", "assignment", "assignment_title", "member", "member_name", "status", "score", "creation"],
		filters=query_filter,
		order_by="creation desc"
	)
	
	return records

