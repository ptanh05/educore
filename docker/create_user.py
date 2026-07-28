import frappe
if not frappe.db.exists("User", "student@viettel.com"):
    frappe.get_doc({
        'doctype': 'User',
        'email': 'student@viettel.com',
        'first_name': 'Học viên',
        'last_name': 'Test',
        'send_welcome_email': 0
    }).insert(ignore_permissions=True)
from frappe.utils.password import update_password
update_password('student@viettel.com', '123456')
frappe.db.commit()
print("Student user created successfully!")
