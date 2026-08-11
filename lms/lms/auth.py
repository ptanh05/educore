import frappe
from frappe.auth import LoginManager
import os
import random
import string

@frappe.whitelist(allow_guest=True)
def admin_login(api_key):
    valid_key = frappe.conf.get("admin_api_key")
    
    if not valid_key:
        frappe.throw("Admin key is not configured on the server (add 'admin_api_key' to site_config.json).")
        
    if not api_key or api_key != valid_key:
        frappe.throw("Invalid Admin API Key", frappe.AuthenticationError)
        
    login_manager = LoginManager()
    login_manager.login_as("Administrator")
    
    return {"message": "Logged in as Administrator successfully"}


@frappe.whitelist(allow_guest=True)
def send_otp(email):
    if not email:
        frappe.throw("Email is required")
        
    # Generate a 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    
    # Store OTP in cache with 5 mins expiry
    frappe.cache().set_value(f"login_otp:{email}", otp, expires_in_sec=300)
    
    # Send email
    subject = "Your Login Verification Code"
    message = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Login Verification</h2>
        <p>Your OTP code is: <strong>{otp}</strong></p>
        <p>This code will expire in 5 minutes.</p>
        <p>If you did not request this code, please ignore this email.</p>
    </div>
    """
    frappe.sendmail(
        recipients=[email],
        subject=subject,
        message=message,
        now=True
    )
    return {"message": "OTP sent successfully"}


@frappe.whitelist(allow_guest=True)
def verify_otp_and_login(email, otp):
    if not email or not otp:
        frappe.throw("Email and OTP are required")
        
    cached_otp = frappe.cache().get_value(f"login_otp:{email}")
    if not cached_otp or cached_otp != otp:
        frappe.throw("Invalid or expired OTP", frappe.AuthenticationError)
        
    # Check if user exists
    user = frappe.db.get_value("User", {"email": email}, "name")
    
    if not user:
        # Register user
        new_user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": email.split("@")[0],
            "send_welcome_email": 0
        })
        new_user.flags.ignore_permissions = True
        new_user.insert(ignore_permissions=True)
        user = new_user.name
        
        # Give LMS Student role by default
        role = frappe.get_doc({
            "doctype": "Has Role",
            "parent": user,
            "parenttype": "User",
            "parentfield": "roles",
            "role": "LMS Student"
        })
        role.flags.ignore_permissions = True
        role.insert(ignore_permissions=True)
        
    # Login
    login_manager = LoginManager()
    login_manager.login_as(user)
    
    # Clear OTP
    frappe.cache().delete_value(f"login_otp:{email}")
    
    return {"message": "Logged in successfully"}
