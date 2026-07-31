// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Program Progress Report"] = {
	filters: [
            { "fieldname": "program", "label": __("Program"), "fieldtype": "Link", "options": "LMS Program" },
            { "fieldname": "department", "label": __("Department"), "fieldtype": "Data" },
            { "fieldname": "status", "label": __("Status"), "fieldtype": "Select", "options": "\nNot Started\nIn Progress\nCompleted\nOverdue" }
        ]
};
