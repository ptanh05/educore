import frappe
from lms.lms.utils import create_user

def create_viettel_demo_data():
	# 1. Instructors & Users
	instructor = create_user(
		email="giangvien.viettel@viettel.com.vn",
		first_name="Học viện",
		last_name="Viettel",
		full_name="Giảng Viên Viettel Academy",
		user_image="/assets/lms/images/instructor.png",
		roles=["Moderator", "Instructor"],
	)

	student1 = create_user(
		email="nv.nguyena@viettel.com.vn",
		first_name="Nguyen",
		last_name="Van A",
		full_name="Nguyễn Văn A",
		user_image="/assets/lms/images/student.jpg",
	)

	student2 = create_user(
		email="tran.thib@viettel.com.vn",
		first_name="Tran",
		last_name="Thi B",
		full_name="Trần Thị B",
		user_image="/assets/lms/images/student1.jpeg",
	)

	# 2. Khóa học 1: Văn Hóa Viettel
	course1_title = "Hành Trang Viettel - Văn Hóa & 8 Giá Trị Cốt Lõi"
	if not frappe.db.exists("LMS Course", {"title": course1_title}):
		course1 = frappe.new_doc("LMS Course")
		course1.update({
			"title": course1_title,
			"category": "Văn Hóa Viettel",
			"tags": "Viettel, Culture, EduCore",
			"published": 1,
			"published_on": frappe.utils.now(),
			"instructors": [{"instructor": instructor.name}],
			"short_introduction": "Chương trình đào tạo định hướng văn hóa doanh nghiệp và 8 giá trị cốt lõi Viettel.",
			"description": """
				<h3>Chào mừng đến với Khóa Học Văn Hóa Viettel</h3>
				<p>Khóa học giúp toàn thể cán bộ nhân viên nắm vững lịch sử, sứ mệnh và 8 giá trị cốt lõi của Tập đoàn Công nghiệp - Viễn thông Quân đội Viettel.</p>
				<ul>
					<li><b>Bài 1:</b> Lịch sử hình thành & Sứ mệnh Viettel</li>
					<li><b>Bài 2:</b> 8 Giá trị cốt lõi Viettel</li>
					<li><b>Bài 3:</b> Văn hóa ứng xử & Kỷ luật quân đội</li>
				</ul>
			"""
		})
		course1.save()
		create_chapters_and_lessons(course1)

	# 3. Khóa học 2: Quản Trị Hệ Thống EduCore
	course2_title = "Lãnh Đạo & Quản Trị Đào Tạo EduCore LMS"
	if not frappe.db.exists("LMS Course", {"title": course2_title}):
		course2 = frappe.new_doc("LMS Course")
		course2.update({
			"title": course2_title,
			"category": "Kỹ Năng Quản Lý",
			"tags": "EduCore, Management, LMS",
			"published": 1,
			"published_on": frappe.utils.now(),
			"instructors": [{"instructor": instructor.name}],
			"short_introduction": "Hướng dẫn xây dựng khóa học, quản lý học viên và cấp chứng chỉ trên Viettel Academy.",
			"description": "<p>Khóa học chuyên sâu dành cho cán bộ quản lý và giảng viên Viettel Academy.</p>"
		})
		course2.save()

	# 4. Tạo Batch (Lớp Học) Viettel Academy K01
	batch_title = "Lớp Đào Tạo Viettel Academy K01 - 2026"
	if not frappe.db.exists("LMS Batch", {"title": batch_title}):
		batch = frappe.new_doc("LMS Batch")
		batch.update({
			"title": batch_title,
			"published": 1,
			"start_date": frappe.utils.today(),
			"end_date": frappe.utils.add_months(frappe.utils.today(), 3),
			"description": "Lớp học tập trung dành cho tân binh Viettel năm 2026.",
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
	c1.title = "Chương 1: Tổng Quan Sứ Mệnh Viettel"
	c1.save()
	course.append("chapters", {"chapter": c1.name})
	course.save()

	# Lesson 1.1
	l1 = frappe.new_doc("Course Lesson")
	l1.course = course.name
	l1.chapter = c1.name
	l1.title = "Bài 1: Giới thiệu Học viện Viettel"
	l1.content = '{"time":1772449622100,"blocks":[{"type":"paragraph","data":{"text":"Học viện Viettel là trung tâm phát triển tri thức và đào tạo nguồn nhân lực chất lượng cao."}}],"version":"2.29.0"}'
	l1.save()
	c1.append("lessons", {"lesson": l1.name})
	c1.save()
