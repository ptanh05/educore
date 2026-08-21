import re

import frappe
from frappe.auth import LoginManager
from frappe.rate_limiter import rate_limit


# ---------------------------------------------------------------------------
# Password policy — enforced server-side so no client bypass is possible.
# ---------------------------------------------------------------------------
MIN_PASSWORD_LENGTH = 8
PASSWORD_RULES = [
    (r"[A-Z]", "at least one uppercase letter"),
    (r"[0-9]", "at least one digit"),
]


def validate_password_strength(password: str) -> None:
    """Raise if *password* does not meet the enterprise password policy."""
    errors: list[str] = []
    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append(f"at least {MIN_PASSWORD_LENGTH} characters")
    for pattern, description in PASSWORD_RULES:
        if not re.search(pattern, password):
            errors.append(description)
    if errors:
        frappe.throw(
            f"Password is too weak. It must contain: {', '.join(errors)}.",
            title="Weak Password",
        )


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60 * 60)
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
@rate_limit(limit=5, seconds=60 * 60)
def sign_up(email: str, full_name: str, password: str) -> dict:
    if not email or not full_name or not password:
        frappe.throw("Email, Full Name, and Password are required.")

    validate_password_strength(password)
        
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
        provider_name = frappe.db.get_value("Social Login Key", {"provider_name": "Google", "enable_social_login": 1}, "name")
        if not provider_name:
            provider_name = "Google" # fallback
            
        from frappe.utils.oauth import get_oauth2_authorize_url
        url = get_oauth2_authorize_url(provider_name, "/lms/courses")
        return url
    except Exception as e:
        frappe.throw(f"Google Login error: {str(e)}")
