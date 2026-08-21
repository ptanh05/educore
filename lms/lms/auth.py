import re

import frappe
from frappe import _
from frappe.auth import LoginManager
from frappe.rate_limiter import rate_limit
from frappe.utils import get_url, random_string


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


# ---------------------------------------------------------------------------
# Audit trail helper — logs auth & business events to Activity Log.
# ---------------------------------------------------------------------------
def log_audit_event(action: str, details: str = "", reference_doctype: str = "", reference_name: str = ""):
    """Write a structured entry to Frappe's Activity Log for compliance."""
    frappe.get_doc({
        "doctype": "Activity Log",
        "user": frappe.session.user,
        "subject": f"[LMS Audit] {action}",
        "full_name": frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user,
        "content": details,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "ip_address": frappe.local.request_ip if hasattr(frappe.local, "request_ip") else "",
    }).insert(ignore_permissions=True, ignore_links=True)


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=20, seconds=60 * 60)
def admin_login(api_key: str) -> dict:
    valid_key = frappe.conf.get("admin_api_key")

    if not valid_key:
        frappe.throw("Admin key is not configured on the server (add 'admin_api_key' to site_config.json).")

    if not api_key or api_key != valid_key:
        log_audit_event("Admin Login Failed", "Invalid API key attempt")
        frappe.throw("Invalid Admin API Key", frappe.AuthenticationError)

    login_manager = LoginManager()
    login_manager.login_as("Administrator")
    log_audit_event("Admin Login Success", "Administrator logged in via API key")

    return {"message": "Logged in as Administrator successfully"}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60 * 60)
def sign_up(email: str, full_name: str, password: str) -> dict:
    if not email or not full_name or not password:
        frappe.throw(_("Email, Full Name, and Password are required."))

    validate_password_strength(password)

    if frappe.db.exists("User", email):
        frappe.throw(_("Email is already registered."))

    # Create user as disabled — will be enabled after email verification.
    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "send_welcome_email": 0,
        "enabled": 0,
    })
    user.flags.ignore_permissions = True
    user.insert(ignore_permissions=True)

    from frappe.utils.password import update_password
    update_password(email, password)

    # Generate verification token and send email
    _send_verification_email(user)

    log_audit_event(
        "Account Created (Pending Verification)",
        f"New account created for {email}, awaiting email verification",
        "User", email,
    )

    return {"message": "Account created! Please check your email to verify your account before signing in."}


def _send_verification_email(user) -> None:
    """Generate a verification token and send a verification link via email."""
    token = random_string(32)
    # Store token in the user's reset_password_key field (Frappe built-in)
    frappe.db.set_value("User", user.name, "reset_password_key", token)
    frappe.db.commit()

    verify_url = f"{get_url()}/api/method/lms.lms.auth.verify_email?token={token}&email={user.name}"

    frappe.sendmail(
        recipients=[user.name],
        subject=_("Verify Your Viettel Academy Account"),
        template="verification",
        args={
            "full_name": user.first_name or user.name,
            "verify_url": verify_url,
            "site_name": "Viettel Academy",
        },
        header=[_("Email Verification"), "green"],
        retry=3,
        now=True,
    )


@frappe.whitelist(allow_guest=True)
def verify_email(token: str, email: str) -> None:
    """Verify the email address and enable the user account."""
    if not token or not email:
        frappe.throw(_("Invalid verification link."))

    stored_key = frappe.db.get_value("User", email, "reset_password_key")
    if not stored_key or stored_key != token:
        frappe.throw(_("Invalid or expired verification link. Please request a new one."))

    # Enable the user
    frappe.db.set_value("User", email, {
        "enabled": 1,
        "reset_password_key": "",
    })
    frappe.db.commit()

    log_audit_event("Email Verified", f"Account {email} verified and enabled", "User", email)

    # Redirect to the login page with a success message
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = f"/{_get_lms_path()}/auth?verified=1"


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=3, seconds=60 * 60)
def resend_verification(email: str) -> dict:
    """Resend the verification email for an unverified account."""
    if not email:
        frappe.throw(_("Email is required."))

    user = frappe.db.get_value("User", email, ["name", "enabled", "first_name"], as_dict=True)
    if not user:
        # Don't reveal whether the email exists
        return {"message": _("If the email is registered, a verification link has been sent.")}

    if user.enabled:
        return {"message": _("This account is already verified. You can sign in.")}

    _send_verification_email(frappe._dict({"name": email, "first_name": user.first_name}))
    return {"message": _("Verification email sent. Please check your inbox.")}


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=3, seconds=60 * 60)
def forgot_password(email: str) -> dict:
    """Send a password reset link to the given email address."""
    if not email:
        frappe.throw(_("Email is required."))

    if not frappe.db.exists("User", email):
        # Don't reveal whether the email exists (security best practice)
        return {"message": _("If the email is registered, a password reset link has been sent.")}

    try:
        from frappe.core.doctype.user.user import reset_password
        reset_password(email)
    except Exception:
        pass

    log_audit_event("Password Reset Requested", f"Reset requested for {email}", "User", email)
    return {"message": _("If the email is registered, a password reset link has been sent.")}


@frappe.whitelist(allow_guest=True)
def get_google_login_url() -> str:
    try:
        provider_name = frappe.db.get_value("Social Login Key", {"provider_name": "Google", "enable_social_login": 1}, "name")
        if not provider_name:
            provider_name = "Google"  # fallback

        from frappe.utils.oauth import get_oauth2_authorize_url
        url = get_oauth2_authorize_url(provider_name, "/lms/courses")
        return url
    except Exception as e:
        frappe.throw(f"Google Login error: {str(e)}")


def _get_lms_path() -> str:
    return frappe.conf.get("lms_path", "lms").strip("/")
