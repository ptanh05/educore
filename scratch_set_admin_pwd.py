import frappe
from frappe.utils.password import update_password

def run():
    frappe.init("lms.localhost")
    frappe.connect()
    update_password("Administrator", "admin")
    frappe.db.commit()
    print("Administrator password set to 'admin'")

if __name__ == "__main__":
    run()
