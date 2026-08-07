import frappe
from frappe.utils.password import update_password

def run():
    frappe.init("lms.localhost")
    frappe.connect()

    # Find existing instructors
    roles = frappe.get_all("Has Role", filters={"role": ["in", ["Course Creator", "Moderator", "Instructor"]]}, fields=["parent", "role"])
    print("Existing users with instructor roles:", roles)

    # Check if instructor@educore.vn exists, or create one
    instructor_email = "instructor@educore.vn"
    if not frappe.db.exists("User", instructor_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": instructor_email,
            "first_name": "Giảng Viên",
            "last_name": "Viettel",
            "enabled": 1,
            "send_welcome_email": 0,
            "roles": [
                {"role": "Course Creator"},
                {"role": "Moderator"},
                {"role": "LMS Student"},
                {"role": "Batch Evaluator"}
            ]
        })
        user.insert(ignore_permissions=True)
        print(f"Created user {instructor_email}")
    else:
        user = frappe.get_doc("User", instructor_email)
        user.enabled = 1
        user.add_roles("Course Creator", "Moderator", "LMS Student", "Batch Evaluator")
        print(f"Updated user {instructor_email}")

    # Set password to instructor123
    update_password(instructor_email, "instructor123")
    frappe.db.commit()
    print(f"Password for {instructor_email} set to instructor123")

if __name__ == "__main__":
    run()
