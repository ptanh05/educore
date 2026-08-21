import frappe

def create_demo_user(email, first_name, password, roles):
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
        
        from frappe.utils.password import update_password
        update_password(email, password)
        
        for role in roles:
            if role != "LMS Student": # LMS Student is auto-added
                doc = frappe.get_doc({
                    "doctype": "Has Role",
                    "parent": user.name,
                    "parenttype": "User",
                    "parentfield": "roles",
                    "role": role
                })
                doc.flags.ignore_permissions = True
                doc.insert(ignore_permissions=True)
        print(f"Created {email}")
    else:
        # Just update password and enable
        frappe.db.set_value("User", email, "enabled", 1)
        from frappe.utils.password import update_password
        update_password(email, password)
        print(f"Updated {email}")

def setup():
    # 1. Student Demo
    create_demo_user("demo_student@viettel.com.vn", "Học viên Demo", "Viettel@123", ["LMS Student"])
    
    # 2. Manager/Admin Demo
    create_demo_user("demo_admin@viettel.com.vn", "Quản lý Demo", "Viettel@123", ["System Manager", "Course Creator"])
