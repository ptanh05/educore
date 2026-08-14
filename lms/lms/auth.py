import frappe
from frappe.auth import LoginManager
import os

@frappe.whitelist(allow_guest=True)
def admin_login(api_key: str) -> dict:
    valid_key = frappe.conf.get("admin_api_key")
    
    if not valid_key:
        frappe.throw("Admin key is not configured on the server (add 'admin_api_key' to site_config.json).")
        
    if not api_key or api_key != valid_key:
        frappe.throw("Invalid Admin API Key", frappe.AuthenticationError)
        
    login_manager = LoginManager()
    login_manager.login_as("Administrator")
    
    return {"message": "Logged in as Administrator successfully"}


@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str, password: str) -> dict:
    if not email or not full_name or not password:
        frappe.throw("Email, Full Name, and Password are required.")
        
    if frappe.db.exists("User", email):
        frappe.throw("Email is already registered.")
        
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "send_welcome_email": 0
    })
    user.flags.ignore_permissions = True
    user.insert(ignore_permissions=True)
    
    from frappe.utils.password import update_password
    update_password(email, password)
    
    # Give LMS Student role by default
    role = frappe.get_doc({
        "doctype": "Has Role",
        "parent": user.name,
        "parenttype": "User",
        "parentfield": "roles",
        "role": "LMS Student"
    })
    role.flags.ignore_permissions = True
    role.insert(ignore_permissions=True)
    
    # Login immediately
    login_manager = LoginManager()
    login_manager.login_as(user.name)
    
    return {"message": "Account created successfully"}


@frappe.whitelist(allow_guest=True)
def get_google_login_url() -> str:
    try:
        from frappe.utils.oauth import get_oauth2_authorize_url
        url = get_oauth2_authorize_url("Google", "/lms/courses")
        return url
    except Exception:
        frappe.throw("Google Login is not properly configured on the server.")
