import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def setup():
    frappe.flags.in_patch = True
    if not frappe.db.exists("DocType", "LMS Department"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "LMS Department",
            "module": "LMS",
            "custom": 1,
            "fields": [
                {"fieldname": "department_name", "fieldtype": "Data", "label": "Department Name", "reqd": 1, "in_list_view": 1},
                {"fieldname": "parent_department", "fieldtype": "Link", "options": "LMS Department", "label": "Parent Department", "in_list_view": 1},
                {"fieldname": "manager", "fieldtype": "Link", "options": "User", "label": "Department Manager", "in_list_view": 1}
            ],
            "autoname": "field:department_name"
        })
        doc.insert(ignore_permissions=True)

    custom_fields = {
        "User": [
            {"fieldname": "lms_department", "fieldtype": "Link", "options": "LMS Department", "label": "Department", "insert_after": "role_profile_name"},
            {"fieldname": "employee_code", "fieldtype": "Data", "label": "Employee Code", "insert_after": "lms_department"},
            {"fieldname": "job_position", "fieldtype": "Data", "label": "Job Position", "insert_after": "employee_code"},
            {"fieldname": "rank_level", "fieldtype": "Data", "label": "Rank/Level", "insert_after": "job_position"},
            {"fieldname": "lms_manager", "fieldtype": "Link", "options": "User", "label": "LMS Manager", "insert_after": "rank_level"}
        ]
    }
    create_custom_fields(custom_fields)
    frappe.db.commit()
    print("Manager setup completed successfully.")
