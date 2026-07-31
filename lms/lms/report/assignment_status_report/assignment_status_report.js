// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Assignment Status Report"] = {
	filters: [
            { "fieldname": "assignment", "label": __("Assignment"), "fieldtype": "Link", "options": "LMS Assignment" },
            { "fieldname": "status", "label": __("Status"), "fieldtype": "Select", "options": "\nPending\nEvaluated" }
        ]
};
