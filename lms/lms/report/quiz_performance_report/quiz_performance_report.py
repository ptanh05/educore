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
			"options": "LMS Quiz Submission",
			"width": 160,
		},
		{
			"fieldname": "quiz",
			"fieldtype": "Link",
			"label": _("Quiz"),
			"options": "LMS Quiz",
			"width": 160,
		},
		{
			"fieldname": "quiz_title",
			"fieldtype": "Data",
			"label": _("Quiz Title"),
			"width": 200,
		},
		{
			"fieldname": "course",
			"fieldtype": "Link",
			"label": _("Course"),
			"options": "LMS Course",
			"width": 150,
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
			"fieldname": "score",
			"fieldtype": "Int",
			"label": _("Score"),
			"width": 90,
		},
		{
			"fieldname": "percentage",
			"fieldtype": "Percent",
			"label": _("Percentage"),
			"width": 110,
		},
		{
			"fieldname": "result",
			"fieldtype": "Data",
			"label": _("Result"),
			"width": 100,
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
		if filters.get("quiz"):
			query_filter["quiz"] = filters.get("quiz")
		if filters.get("course"):
			query_filter["course"] = filters.get("course")
	
	records = frappe.get_all(
		"LMS Quiz Submission",
		fields=["name", "quiz", "quiz_title", "course", "member", "member_name", "score", "percentage", "result", "creation"],
		filters=query_filter,
		order_by="creation desc"
	)
	
	return records

