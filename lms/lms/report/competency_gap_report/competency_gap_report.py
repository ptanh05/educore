import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "member",
			"fieldtype": "Link",
			"label": _("Learner"),
			"options": "User",
			"width": 150,
		},
		{
			"fieldname": "department",
			"fieldtype": "Data",
			"label": _("Department"),
			"width": 120,
		},
		{
			"fieldname": "position",
			"fieldtype": "Data",
			"label": _("Position"),
			"width": 120,
		},
		{
			"fieldname": "skill",
			"fieldtype": "Link",
			"label": _("Skill"),
			"options": "LMS Skill",
			"width": 150,
		},
		{
			"fieldname": "required_level",
			"fieldtype": "Int",
			"label": _("Required"),
			"width": 100,
		},
		{
			"fieldname": "achieved_level",
			"fieldtype": "Int",
			"label": _("Achieved"),
			"width": 100,
		},
		{
			"fieldname": "gap",
			"fieldtype": "Int",
			"label": _("Gap"),
			"width": 100,
		},
		{
			"fieldname": "recommended_course",
			"fieldtype": "Link",
			"label": _("Recommendation"),
			"options": "LMS Course",
			"width": 200,
		}
	]

def get_data(filters=None):
	query_filter = {}
	if filters and filters.get("department"):
		query_filter["department"] = filters.get("department")
		
	# Lấy tất cả user active
	query_filter["enabled"] = 1
	users = frappe.get_all("User", filters=query_filter, fields=["name", "department", "name as member"])
	
	data = []
	for u in users:
		hr_profile = frappe.db.get_value("HR Employee Profile", {"user": u.name, "status": "Active"}, "position")
		if not hr_profile:
			continue
			
		role_profile = frappe.db.get_value("LMS Role Profile", {"position": hr_profile}, "name")
		if not role_profile:
			continue
			
		required_skills = frappe.get_all("LMS Skill Requirement", filters={"parent": role_profile}, fields=["skill", "required_level"])
		
		for req in required_skills:
			achieved = frappe.db.get_value("LMS Member Skill", {"member": u.name, "skill": req.skill}, "achieved_level") or 0
			gap = req.required_level - achieved
			
			if gap > 0:
				# Gợi ý course
				recommended = ""
				course_skills = frappe.get_all("LMS Course Skill", filters={"skill": req.skill, "level_awarded": [">=", req.required_level]}, fields=["parent"])
				if course_skills:
					recommended = course_skills[0].parent
					
				data.append(frappe._dict({
					"member": u.name,
					"department": u.department,
					"position": hr_profile,
					"skill": req.skill,
					"required_level": req.required_level,
					"achieved_level": achieved,
					"gap": gap,
					"recommended_course": recommended
				}))
				
	return data
