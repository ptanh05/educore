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
			"width": 150,
		},
		{
			"fieldname": "department",
			"fieldtype": "Data",
			"label": _("Department"),
			"width": 120,
		},
		{
			"fieldname": "program",
			"fieldtype": "Link",
			"label": _("Program"),
			"options": "LMS Program",
			"width": 150,
		},
		{
			"fieldname": "status",
			"fieldtype": "Data",
			"label": _("Status"),
			"width": 120,
		},
		{
			"fieldname": "progress",
			"fieldtype": "Data",
			"label": _("Progress (%)"),
			"width": 100,
		}
	]

def get_data(filters=None):
	query_filter = {}
	if filters:
		if filters.get("program"):
			query_filter["parent"] = filters.get("program")
		if filters.get("status"):
			query_filter["status"] = filters.get("status")

	if filters and filters.get("department"):
		try:
			members = frappe.get_all("User", filters={"department": filters.get("department")}, pluck="name")
			if members:
				query_filter["member"] = ["in", members]
			else:
				return []
		except Exception:
			pass

	records = frappe.get_all(
		"LMS Program Member",
		fields=["member", "full_name as member_name", "parent as program", "status", "progress"],
		filters=query_filter
	)
	
	for r in records:
		r.department = frappe.db.get_value("User", r.member, "department", ignore=True) or ""
	
	return records
