# pyrefly: ignore [missing-import]
import frappe
from lms.lms.utils import create_user

def create_viettel_demo_data():
	# 1. Instructors & Users
	instructor = create_user(
		email="giangvien.viettel@viettel.com.vn",
		first_name="Hoc Vien",
		last_name="Viettel",
		full_name="Giang Vien Viettel Academy",
		user_image="/assets/lms/images/instructor.png",
		roles=["Moderator", "Instructor"],
	)

	student1 = create_user(
		email="nv.nguyena@viettel.com.vn",
		first_name="Nguyen",
		last_name="Van A",
		full_name="Nguyen Van A",
		user_image="/assets/lms/images/student.jpg",
	)

	student2 = create_user(
		email="tran.thib@viettel.com.vn",
		first_name="Tran",
		last_name="Thi B",
		full_name="Tran Thi B",
		user_image="/assets/lms/images/student1.jpeg",
	)

	# 2. Khóa học 1: Văn Hóa Viettel
	course1_title = "Hanh Trang Viettel - Van Hoa & 8 Gia Tri Cot Loi"
	if not frappe.db.exists("LMS Course", {"title": course1_title}):
		course1 = frappe.new_doc("LMS Course")
		course1.update({
			"title": course1_title,
			"category": "Van Hoa Viettel",
			"tags": "Viettel, Culture, EduCore",
			"published": 1,
			"published_on": frappe.utils.now(),
			"instructors": [{"instructor": instructor.name}],
			"short_introduction": "Chuong trinh dao tao dinh huong van hoa doanh nghiep va 8 gia tri cot loi Viettel.",
			"description": """
				<h3>Chao mung den voi Khoa Hoc Van Hoa Viettel</h3>
				<p>Khoa hoc giup toan the can bo nhan vien nam vung lich su, su menh va 8 gia tri cot loi cua Tap doan Viettel.</p>
				<ul>
					<li><b>Bai 1:</b> Lich su hinh thanh & Su menh Viettel</li>
					<li><b>Bai 2:</b> 8 Gia tri cot loi Viettel</li>
					<li><b>Bai 3:</b> Van hoa ung xu & Ky luat quan doi</li>
				</ul>
			"""
		})
		course1.save()
		create_chapters_and_lessons(course1)

	# 3. Khóa học 2: Quản Trị Hệ Thống EduCore
	course2_title = "Lanh Dao & Quan Tri Dao Tao EduCore LMS"
	if not frappe.db.exists("LMS Course", {"title": course2_title}):
		course2 = frappe.new_doc("LMS Course")
		course2.update({
			"title": course2_title,
			"category": "Ky Nang Quan Ly",
			"tags": "EduCore, Management, LMS",
			"published": 1,
			"published_on": frappe.utils.now(),
			"instructors": [{"instructor": instructor.name}],
			"short_introduction": "Huong dan xay dung khoa hoc, quan ly hoc vien va cap chung chi tren Viettel Academy.",
			"description": "<p>Khoa hoc chuyen sau danh cho can bo quan ly va giang vien Viettel Academy.</p>"
		})
		course2.save()

	# 4. Tạo Batch (Lớp Học) Viettel Academy K01
	batch_title = "Lop Dao Tao Viettel Academy K01 - 2026"
	if not frappe.db.exists("LMS Batch", {"title": batch_title}):
		batch = frappe.new_doc("LMS Batch")
		batch.update({
			"title": batch_title,
			"published": 1,
			"start_date": frappe.utils.today(),
			"end_date": frappe.utils.add_months(frappe.utils.today(), 3),
			"description": "Lop hoc tap trung danh cho tan binh Viettel nam 2026.",
			"seat_count": 50,
			"allow_self_enrollment": 1
		})
		batch.save()

	frappe.db.commit()
	print("VIETTEL DEMO DATA CREATED SUCCESSFULLY!")

def create_chapters_and_lessons(course):
	# Chapter 1
	c1 = frappe.new_doc("Course Chapter")
	c1.course = course.name
	c1.title = "Chuong 1: Tong Quan Su Menh Viettel"
	c1.save()
	course.append("chapters", {"chapter": c1.name})
	course.save()

	# Lesson 1.1
	l1 = frappe.new_doc("Course Lesson")
	l1.course = course.name
	l1.chapter = c1.name
	l1.title = "Bai 1: Gioi thieu Hoc vien Viettel"
	l1.content = '{"time":1772449622100,"blocks":[{"type":"paragraph","data":{"text":"Hoc vien Viettel la trung tam phat trien tri thuc va dao tao nguon nhan luc chat luong cao."}}],"version":"2.29.0"}'
	l1.save()
	c1.append("lessons", {"lesson": l1.name})
	c1.save()
