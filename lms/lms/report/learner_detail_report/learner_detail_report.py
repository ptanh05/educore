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
			"width": 160,
		},
		{
			"fieldname": "department",
			"fieldtype": "Data",
			"label": _("Department"),
			"width": 140,
		},
		{
			"fieldname": "course",
			"fieldtype": "Link",
			"label": _("Course"),
			"options": "LMS Course",
			"width": 160,
		},
		{
			"fieldname": "progress",
			"fieldtype": "Percent",
			"label": _("Progress (%)"),
			"width": 110,
		},
		{
			"fieldname": "current_lesson",
			"fieldtype": "Link",
			"label": _("Current Lesson"),
			"options": "Course Lesson",
			"width": 160,
		},
		{
			"fieldname": "creation",
			"fieldtype": "Date",
			"label": _("Enrollment Date"),
			"width": 130,
		},
	]

def get_data(filters=None):
	query_filter = {}
	if filters and filters.get("member"):
		query_filter["member"] = filters.get("member")
	
	records = frappe.get_all(
		"LMS Enrollment",
		fields=["name", "member", "member_name", "course", "progress", "current_lesson", "creation"],
		filters=query_filter,
		order_by="creation desc"
	)
	
	data = []
	for r in records:
		dept = frappe.db.get_value("User", r.member, "department", ignore=True) or ""
		data.append({
			"member": r.member,
			"member_name": r.member_name,
			"department": dept,
			"course": r.course,
			"progress": r.progress or 0,
			"current_lesson": r.current_lesson or "",
			"creation": r.creation.strftime("%Y-%m-%d") if r.creation else ""
		})
	return data

