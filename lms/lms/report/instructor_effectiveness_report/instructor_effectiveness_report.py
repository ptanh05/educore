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
			"fieldname": "course",
			"fieldtype": "Link",
			"label": _("Course"),
			"options": "LMS Course",
			"width": 160,
		},
		{
			"fieldname": "course_title",
			"fieldtype": "Data",
			"label": _("Course Title"),
			"width": 200,
		},
		{
			"fieldname": "instructor",
			"fieldtype": "Data",
			"label": _("Instructor"),
			"width": 160,
		},
		{
			"fieldname": "rating",
			"fieldtype": "Float",
			"label": _("Rating (1-5)"),
			"width": 110,
		},
		{
			"fieldname": "review",
			"fieldtype": "Small Text",
			"label": _("Review / Feedback"),
			"width": 250,
		},
		{
			"fieldname": "owner",
			"fieldtype": "Link",
			"label": _("Reviewer"),
			"options": "User",
			"width": 150,
		},
		{
			"fieldname": "creation",
			"fieldtype": "Date",
			"label": _("Date"),
			"width": 120,
		},
	]

def get_data(filters=None):
	query_filter = {}
	if filters:
		if filters.get("course"):
			query_filter["course"] = filters.get("course")
		if filters.get("instructor"):
			courses = frappe.get_all("Course Instructor", filters={"instructor": filters.get("instructor")}, pluck="parent")
			if courses:
				query_filter["course"] = ["in", courses]
			else:
				return []
	
	reviews = frappe.get_all(
		"LMS Course Review",
		fields=["name", "course", "course_title", "rating", "review", "owner", "creation"],
		filters=query_filter,
		order_by="creation desc"
	)
	
	data = []
	for r in reviews:
		instructors = frappe.get_all("Course Instructor", filters={"parent": r.course, "parenttype": "LMS Course"}, pluck="instructor")
		instructor_str = ", ".join(instructors) if instructors else ""
		data.append({
			"course": r.course,
			"course_title": r.course_title,
			"instructor": instructor_str,
			"rating": r.rating,
			"review": r.review,
			"owner": r.owner,
			"creation": r.creation.strftime("%Y-%m-%d") if r.creation else ""
		})
	return data

