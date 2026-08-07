import frappe

def run():
    frappe.init("lms.localhost")
    frappe.connect()

    if frappe.db.exists("User", "instructor@educore.vn"):
        user = frappe.get_doc("User", "instructor@educore.vn")
        user.first_name = "Gi\u1ea3ng vi\u00ean"
        user.last_name = "Viettel"
        user.save(ignore_permissions=True)
        frappe.db.commit()
        print("Success! Full name:", user.full_name)

if __name__ == "__main__":
    run()
