// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Certificate Report"] = {
	filters: [
            { "fieldname": "course", "label": __("Course"), "fieldtype": "Link", "options": "LMS Course" },
            { "fieldname": "member", "label": __("Learner"), "fieldtype": "Link", "options": "User" },
            { "fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date" },
            { "fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date" }
        ]
};
