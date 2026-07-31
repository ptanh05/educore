// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Instructor Effectiveness Report"] = {
	filters: [
            { "fieldname": "instructor", "label": __("Instructor"), "fieldtype": "Link", "options": "User" },
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" }
        ]
};
