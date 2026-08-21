import frappe

def get_last_error():
    log = frappe.get_all("Error Log", order_by="creation desc", limit=1, fields=["error"])
    if log:
        print(log[0].error)
    else:
        print("No errors found.")
