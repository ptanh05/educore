// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Learner Detail Report"] = {
	filters: [
            { "fieldname": "member", "label": __("Learner"), "fieldtype": "Link", "options": "User" }
        ]
};
