// Copyright (c) 2024, Viettel Academy
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Department Training Report"] = {
	filters: [
            { "fieldname": "department", "label": __("Department"), "fieldtype": "Data" },
            { "fieldname": "from_date", "label": __("From Date"), "fieldtype": "Date" },
            { "fieldname": "to_date", "label": __("To Date"), "fieldtype": "Date" }
        ]
};
