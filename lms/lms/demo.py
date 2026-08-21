import frappe
from frappe.utils.password import update_password

def create_user(email, first_name, roles):
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "enabled": 1,
            "send_welcome_email": 0
        })
        user.flags.ignore_permissions = True
        user.flags.ignore_password_policy = True
        user.insert(ignore_permissions=True)
        
        for role in roles:
            if role == "LMS Student": continue
            doc = frappe.get_doc({
                "doctype": "Has Role",
                "parent": user.name,
                "parenttype": "User",
                "parentfield": "roles",
                "role": role
            })
            doc.flags.ignore_permissions = True
            doc.insert(ignore_permissions=True)

    frappe.db.set_value("User", email, "enabled", 1)
    update_password(email, "Viettel@123")
    print(f"Created/Updated: {email}")

def setup():
    # Giảng viên
    create_user("demo_giangvien@viettel.com.vn", "Giảng viên Demo", ["Moderator", "Course Creator"])
    # Học viên
    create_user("demo_hocvien@viettel.com.vn", "Học viên Demo", ["LMS Student"])
    
    frappe.db.commit()
