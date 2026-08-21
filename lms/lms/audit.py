import frappe

def log_business_event(action: str, details: str, reference_doctype: str, reference_name: str, user: str = None):
    """Write a structured entry to Frappe's Activity Log for business events."""
    user = user or frappe.session.user
    full_name = frappe.db.get_value("User", user, "full_name") or user
    
    frappe.get_doc({
        "doctype": "Activity Log",
        "user": user,
        "subject": f"[LMS Audit] {action}",
        "full_name": full_name,
        "content": details,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "ip_address": frappe.local.request_ip if hasattr(frappe.local, "request_ip") else "",
    }).insert(ignore_permissions=True, ignore_links=True)

def on_enrollment_change(doc, method):
    """Audit hook for LMS Enrollment"""
    if method == "after_insert":
        log_business_event(
            "Enrollment Created",
            f"User {doc.member} enrolled in course {doc.course}.",
            "LMS Enrollment",
            doc.name,
            doc.member
        )
    elif method == "on_update":
        # Check if progress reached 100
        if doc.has_value_changed("progress") and doc.progress == 100:
            log_business_event(
                "Course Completed",
                f"User {doc.member} completed course {doc.course}.",
                "LMS Enrollment",
                doc.name,
                doc.member
            )

def on_batch_enrollment_change(doc, method):
    """Audit hook for LMS Batch Enrollment"""
    if method == "after_insert":
        log_business_event(
            "Batch Enrollment Created",
            f"User {doc.member} enrolled in batch {doc.batch}.",
            "LMS Batch Enrollment",
            doc.name,
            doc.member
        )

def on_certificate_issued(doc, method):
    """Audit hook for LMS Certificate"""
    if method == "after_insert":
        log_business_event(
            "Certificate Issued",
            f"Certificate {doc.name} issued to {doc.member} for course {doc.course}.",
            "LMS Certificate",
            doc.name,
            doc.member
        )
