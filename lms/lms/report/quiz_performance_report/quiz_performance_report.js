// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quiz Performance Report"] = {
	filters: [
            { "fieldname": "quiz", "label": __("Quiz"), "fieldtype": "Link", "options": "LMS Quiz" },
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" }
        ]
};
