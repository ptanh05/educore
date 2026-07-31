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
			"fieldname": "course",
			"fieldtype": "Link",
			"label": _("Course"),
			"options": "LMS Course",
			"width": 150,
		},
		{
			"fieldname": "progress",
			"fieldtype": "Data",
			"label": _("Progress (%)"),
			"width": 100,
		},
		{
			"fieldname": "enrollment_date",
			"fieldtype": "Date",
			"label": _("Enrollment Date"),
			"width": 120,
		}
	]

def get_data(filters=None):
	query_filter = {}
	if filters:
		if filters.get("from_date"):
			query_filter["creation"] = [">=", filters.get("from_date")]
		if filters.get("to_date"):
			if "creation" in query_filter:
				query_filter["creation"] = ["between", (filters.get("from_date"), filters.get("to_date"))]
			else:
				query_filter["creation"] = ["<=", filters.get("to_date")]

	if filters and filters.get("department"):
		try:
			members = frappe.get_all("User", filters={"department": filters.get("department")}, pluck="name")
			if members:
				query_filter["member"] = ["in", members]
			else:
				return []
		except Exception:
			pass

	enrollments = frappe.get_all(
		"LMS Enrollment",
		fields=["name", "member", "member_name", "course", "progress", "creation"],
		filters=query_filter
	)
	
	data = []
	for e in enrollments:
		department = frappe.db.get_value("User", e.member, "department", ignore=True) or ""
		data.append({
			"member": e.member,
			"member_name": e.member_name,
			"department": department,
			"course": e.course,
			"progress": e.progress or 0,
			"enrollment_date": e.creation.strftime("%Y-%m-%d") if e.creation else ""
		})
	return data
