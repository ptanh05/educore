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
			"label": _("ID"),
			"options": "LMS Quiz Submission",
			"width": 200,
		}
	]

def get_data(filters=None):
	conditions = ""
	# TODO: Add dynamic filters based on filters dict
	
	records = frappe.get_all(
		"LMS Quiz Submission",
		fields=["name"],
		filters=filters
	)
	
	return records
