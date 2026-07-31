# Copyright (c) 2024, Viettel Academy
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document

class HREmployeeProfile(Document):
	def on_update(self):
		self.sync_with_user()
		self.assign_learning_paths()
		
	def sync_with_user(self):
		if not self.email:
			return
			
		user_exists = frappe.db.exists("User", self.email)
		if not user_exists:
			user = frappe.new_doc("User")
			user.email = self.email
			user.first_name = self.full_name
			user.send_welcome_email = 0
			user.insert(ignore_permissions=True)
		else:
			user = frappe.get_doc("User", self.email)
			
		# Sync details
		if self.full_name != user.full_name or (self.status == "Inactive" and user.enabled) or (self.status == "Active" and not user.enabled):
			user.first_name = self.full_name
			user.enabled = 1 if self.status == "Active" else 0
			user.save(ignore_permissions=True)
			
		# Map to our user field
		if self.user != self.email:
			self.db_set("user", self.email)
			
		# Assign default role if Active
		if self.status == "Active":
			if not frappe.db.exists("Has Role", {"parent": self.email, "role": "LMS Student"}):
				user.append("roles", {"role": "LMS Student"})
				user.save(ignore_permissions=True)
				
		# Optional: Set department/designation on User if fields exist in schema
		try:
			if hasattr(user, "department"):
				frappe.db.set_value("User", self.email, "department", self.department)
		except Exception:
			pass

	def assign_learning_paths(self):
		if self.status != "Active":
			return
			
		# Find matching programs based on department or position
		programs = frappe.get_all("LMS Program", filters={"published": 1}, fields=["name", "department", "position"])
		
		for p in programs:
			match = False
			if p.department and self.department and p.department.lower() == self.department.lower():
				match = True
			if p.position and self.position and p.position.lower() == self.position.lower():
				match = True
				
			if match:
				# Enroll
				if not frappe.db.exists("LMS Program Member", {"parent": p.name, "member": self.email}):
					program = frappe.get_doc("LMS Program", p.name)
					program.append("members", {
						"member": self.email,
						"status": "Not Started",
						"assignment_source": "HR Sync"
					})
					program.save(ignore_permissions=True)

