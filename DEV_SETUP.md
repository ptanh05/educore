# 📘 EduCore LMS - Hướng Dẫn Setup & Dọn Dẹp Nền Tảng (Phase 0)

Tài liệu này cung cấp hướng dẫn cài đặt, cấu hình môi trường phát triển (Dev Environment), danh sách module và checklist kiểm thử cho dự án **EduCore LMS**.

---

## 1. Xác Định Version Môi Trường (Environment Matrix)

| Thành phần | Yêu cầu tối thiểu | Đã kiểm tra (Local) | Ghi chú |
|---|---|---|---|
| **Node.js** | `>= 22.0.0` | `v22.17.1` | Dùng cho Frontend Vite & Vitest |
| **NPM** | `>= 10.0.0` | `10.8.2` | Package manager chính |
| **Python** | `>= 3.10.0` | `3.12.8` | Backend Frappe Framework |
| **Frappe Framework**| `v14` / `v15` / `v16` | Bench environment | Cần thiết để chạy backend fullstack |
| **Database** | MariaDB 10.6+ / PostgreSQL 14+ | Frappe DB | Cơ sở dữ liệu chính |

---

## 2. Danh Sách Module Bật / Tắt (Module Management Matrix)

Dưới đây là danh sách phân loại các module trong EduCore LMS để xác định phạm vi bật/tắt theo nhu cầu triển khai:

| Module | DocTypes / Chức năng chính | Trạng thái | Mục đích & Ghi chú |
|---|---|---|---|
| **Core Learning** | `LMS Course`, `Course Chapter`, `Course Lesson`, `LMS Enrollment`, `LMS Course Progress` | 🟢 **BẬT (Core)** | Quản lý khóa học, bài học, tiến độ học tập |
| **Assessment & Quiz** | `LMS Quiz`, `LMS Question`, `LMS Assignment`, `LMS Programming Exercise` | 🟢 **BẬT (Core)** | Bài kiểm tra trắc nghiệm, tự luận & nộp bài |
| **Batch & Timetable** | `LMS Batch`, `LMS Batch Enrollment`, `LMS Batch Timetable`, `LMS Live Class` | 🟢 **BẬT (Core)** | Quản lý lớp học theo đợt, thời khóa biểu, học trực tuyến |
| **Certification** | `LMS Certificate`, `LMS Certificate Request`, `LMS Certificate Evaluation` | 🟢 **BẬT (Core)** | Cấp chứng chỉ & chấm điểm chứng chỉ |
| **Social & Profile** | User Profile, `Discussion Reply`, `LMS Course Review`, `LMS Badge` | 🟢 **BẬT (Core)** | Hồ sơ học viên, thảo luận bài học & huy hiệu |
| **Raven Integration** | `raven_membership_providers` (Hooks) | 🟢 **BẬT (Extension)**| Tích hợp hệ thống quản lý thành viên Raven |
| **SCORM E-Learning** | `SCORMRenderer`, `SCORMChapter` | 🟡 **TÙY CHỌN** | Tắt nếu không nhập gói bài giảng SCORM chuẩn |
| **Payment & Billing** | `LMS Payment`, `LMS Coupon`, Razorpay Integration | 🟡 **TÙY CHỌN** | Tắt nếu triển khai LMS nội bộ/miễn phí |
| **Job Board** | `Job Opportunity`, `Job Applications` | 🔴 **CÓ THỂ TẮT** | Sàn tuyển dụng & cơ hội việc làm |

---

## 3. Hướng Dẫn Setup Dev Cho Dev Mới (Step-by-Step Setup Guide)

### ⚙️ Phương Án 1: Setup Frontend Standalone (Dành cho Dev UI/Frontend)
Phù hợp khi bạn chỉ làm việc trên UI Vue 3 hoặc chạy unit tests.

1. **Clone repository & chuyển vào thư mục frontend:**
   ```bash
   git clone <repository-url> educore
   cd educore/frontend
   ```

2. **Cài đặt dependencies:**
   ```bash
   npm install
   ```

3. **Chạy Frontend Dev Server:**
   ```bash
   npm run dev
   ```
   Ứng dụng sẽ chạy tại `http://localhost:8085`.

4. **Chạy Unit Test:**
   ```bash
   npm run test
   ```

---

### ⚙️ Phương Án 2: Setup Fullstack với Frappe Bench (Dành cho Dev Fullstack/Backend)
Phù hợp để chạy toàn bộ hệ thống gồm Python Backend + Database + Vue Frontend.

1. **Khởi tạo Frappe Bench (nếu chưa có):**
   ```bash
   bench init frappe-bench --python python3.12
   cd frappe-bench
   ```

2. **Tạo site mới:**
   ```bash
   bench new-site educore.test
   ```

3. **Đưa app EduCore vào bench:**
   Sao chép hoặc clone thư mục `educore` vào `frappe-bench/apps/lms`.

4. **Cài đặt app vào site:**
   ```bash
   bench --site educore.test install-app lms
   ```

5. **Cấu hình bypass CSRF cho dev frontend:**
   Thêm cấu hình vào `sites/educore.test/site_config.json`:
   ```json
   {
     "ignore_csrf": 1
   }
   ```

6. **Khởi chạy hệ thống:**
   ```bash
   bench start
   ```

---

### ⚙️ Phương Án 3: Setup Nhanh Bằng Docker Container
Phù hợp để dựng môi trường kiểm thử hoặc demo nhanh mà không cần cài MariaDB/Bench thủ công.

1. **Chạy docker-compose:**
   ```bash
   docker compose -f docker/docker-compose.yml up -d
   ```

---

## 4. Checklist Kiểm Thử & Build (Test & Build Checklist)

| Hạng mục kiểm tra | Command / Thao tác | Trạng thái | Chi tiết |
|---|---|---|---|
| **Cấu hình Node / Python** | `node -v` & `python --version` | ✅ **PASSED** | Node v22.17.1, Python 3.12.8 |
| **Frontend Dependencies** | `npm install` (trong `/frontend`) | ✅ **PASSED** | Cài đặt thành công 820 packages |
| **Frontend Unit Tests** | `npm run test` (Vitest) | ✅ **PASSED** | **42/42 files passed** (393 tests) |
| **Frontend Production Build**| `npm run build` (Vite) | ✅ **PASSED** | OutDir: `../lms/public/frontend` & `_lms.html` |
| **Backend Bench Tests** | `bench --site [site] run-tests --app lms` | ⏳ **CẦN BENCH** | Chạy trong môi trường Frappe Bench |
| **End-to-End Tests** | `npm run test-local` (Cypress) | ⏳ **CẦN SERVER** | Yêu cầu server backend đang chạy |
| **Git Status Baseline** | `git status` | ✅ **CLEAN** | Sẵn sàng cho feature lớn tiếp theo |

---

## 5. Những Lỗi Thường Gặp & Cách Xử Lý (Troubleshooting)

1. **Lỗi `findBenchPath` vòng lặp vô hạn trên Windows:**
   - *Nguyên nhân*: Plugin Vite của `frappe-ui` kiểm tra đường dẫn gốc `currentDir !== '/'` không bao giờ dùng lại ở đĩa Windows (`D:\`).
   - *Đã xử lý*: Đã cập nhật `findBenchPath()` và `findAppName()` trong `frontend/node_modules/frappe-ui/vite/utils.js` để nhận biết đường dẫn đĩa gốc Windows.

2. **Lỗi thiếu file `common_site_config.json` khi build standalone:**
   - *Nguyên nhân*: Thư mục `sites/` chỉ có khi ứng dụng đặt trong Frappe Bench.
   - *Đã xử lý*: Đã tạo fallback config `frontend/src/common_site_config_fallback.json` và alias trong `vite.config.js`.

3. **Lỗi lệnh `cp` / `yarn` không tìm thấy trên Windows cmd:**
   - *Đã xử lý*: Cập nhật `package.json` và `frontend/package.json` sử dụng lệnh Node cross-platform (`node -e ...`).
