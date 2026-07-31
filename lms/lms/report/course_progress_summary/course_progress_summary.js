// Copyright (c) 2016, FOSS United and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Course Progress Summary"] = {
	filters: [
		{
			fieldname: "course",
			label: __("Course"),
			fieldtype: "Link",
			options: "LMS Course",
			reqd: 0,
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Data",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname: "batch",
			label: __("Batch"),
			fieldtype: "Link",
			options: "LMS Batch",
		},
	],
};
