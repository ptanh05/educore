# 🔍 EduCore LMS — Đánh Giá Toàn Diện: Sẵn Sàng Cho Doanh Nghiệp?

> **Ngày đánh giá:** 2026-08-21  
> **Phạm vi:** Login → Quy trình nghiệp vụ → Quản lý → Báo cáo  
> **Kết luận tổng thể:** ⚠️ **CHƯA SẴN SÀNG — Cần sửa 8 vấn đề nghiêm trọng trước khi bán**

---

## 📊 Tổng Quan Điểm Đánh Giá

| Hạng mục | Điểm | Mức độ |
|---|---|---|
| Tính năng nghiệp vụ (Features) | ⭐⭐⭐⭐ 8/10 | Tốt |
| Bảo mật (Security) | ⭐⭐ 4/10 | **Cần sửa gấp** |
| Trải nghiệm người dùng (UX) | ⭐⭐⭐ 6/10 | Trung bình |
| Chất lượng mã nguồn (Code Quality) | ⭐⭐⭐ 6/10 | Trung bình |
| Khả năng mở rộng (Scalability) | ⭐⭐⭐ 6/10 | Trung bình |
| Sẵn sàng triển khai (Production-ready) | ⭐⭐ 4/10 | **Cần sửa gấp** |

---

## ✅ Những Điểm Mạnh (Đã Làm Tốt)

### 1. Kiến Trúc & Tính Năng Nghiệp Vụ — Rất Đầy Đủ
- **76 doctypes** bao phủ toàn bộ quy trình LMS doanh nghiệp
- Quy trình hoàn chỉnh: Course → Chapter → Lesson → Quiz → Assignment → Certificate
- **Programs (Lộ trình đào tạo)**: Nhóm nhiều course lại, theo dõi tiến độ tổng thể
- **Batch management**: Quản lý lớp học theo đợt, enrollment, timetable
- **SCORM support**: Import gói đào tạo SCORM chuẩn quốc tế
- **Dashboard quản lý đơn vị** (`ManagerHome.vue`): Tracking nhân sự, tỷ lệ hoàn thành, quá hạn
- **9 loại báo cáo** (competency gap, instructor effectiveness, quiz performance, v.v.)

### 2. Hệ Thống Phân Quyền — Phức Tạp & Tốt
- 4 vai trò LMS: `Moderator`, `Course Creator`, `Batch Evaluator`, `LMS Student`
- **Lesson-level permission**: `permissions.py` — single source of truth cho quyền truy cập bài học
- **Quiz permission**: Kiểm tra instructor → enrolled student → batch member
- **File-level permission hook**: Bảo vệ file tài liệu giảng viên (instructor_content)
- Sử dụng `frappe.only_for()` đúng cách ở các API endpoints quan trọng

### 3. Bảo Mật Nâng Cao (Một Số Phần)
- **Input sanitization**: `sanitize_editorjs()`, `sanitize_json()` cho nội dung Editor
- **XSS prevention**: Quiz answers được sanitize qua `sanitize_html()`
- **SCORM path traversal protection**: Kiểm tra tên chapter để tránh directory traversal
- **Rate limiting**: 12+ API endpoints có `@rate_limit` decorator
- **Endpoint whitelist** (`lms/auth.py`): Block non-LMS API cho portal users

### 4. Tính Năng Doanh Nghiệp Nổi Bật
- **Unit Manager Dashboard**: Theo dõi nhân sự theo phòng ban, export CSV với BOM UTF-8
- **Instructor Dashboard**: Stats tổng hợp — slow learners, pending assignments, quiz average
- **Certificate system**: Issue + evaluation workflow
- **Payment integration**: Razorpay, coupon, GST, multicurrency
- **Course Import/Export**: ZIP format cho di chuyển content giữa hệ thống
- **Branding**: Đã customize cho "Viettel Academy" — logo, favicon, tiếng Việt

---

## 🚨 VẤN ĐỀ NGHIÊM TRỌNG — PHẢI SỬA TRƯỚC KHI BÁN

### 🔴 CRITICAL #1: Debug `print()` Statements Trong Production Code

**File:** [utils.py](file:///d:/du%20an/educore/lms/lms/utils.py#L126-L131)

```python
def create_user(email, first_name=None, ...):
    validate_email_address(email, True)
    print(email)                           # ❌ LỘ EMAIL RA STDOUT
    print(frappe.db.exists("User", email)) # ❌ LỘ THÔNG TIN DB
    existing_user = frappe.db.exists("User", email)
    print("existing_user", existing_user)  # ❌ DEBUG LEAK
    if existing_user:
        print("User already exists")       # ❌ DEBUG LEAK
```

> [!CAUTION]
> **Rủi ro:** Lộ thông tin email và trạng thái user ra server logs. Với doanh nghiệp, đây là vi phạm GDPR/PDPA. Phải xóa ngay.

---

### 🔴 CRITICAL #2: Sign-up Không Có Password Validation

**File:** [auth.py](file:///d:/du%20an/educore/lms/lms/auth.py#L22-L56)

```python
@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str, password: str) -> dict:
    # ❌ KHÔNG kiểm tra độ mạnh mật khẩu!
    # ❌ KHÔNG kiểm tra length tối thiểu!
    # ❌ KHÔNG rate limit cho sign-up!
    user.insert(ignore_permissions=True)
    update_password(email, password)
    login_manager.login_as(user.name)  # Auto-login ngay — không cần verify email
```

> [!CAUTION]
> **Rủi ro:**
> 1. Password `"1"` hay `"abc"` sẽ được chấp nhận
> 2. Không xác thực email → doanh nghiệp không thể quản lý user thật
> 3. Không có rate limit → có thể spam tạo hàng ngàn tài khoản
> 4. `ignore_permissions=True` + auto login = bypass mọi security check

---

### 🔴 CRITICAL #3: Admin Login Bằng Static API Key — Nguy Hiểm Cực Độ

**File:** [auth.py](file:///d:/du%20an/educore/lms/lms/auth.py#L5-L18)

```python
@frappe.whitelist(allow_guest=True)
def admin_login(api_key: str) -> dict:
    valid_key = frappe.conf.get("admin_api_key")
    if api_key != valid_key:
        frappe.throw("Invalid Admin API Key", frappe.AuthenticationError)
    login_manager = LoginManager()
    login_manager.login_as("Administrator")  # ❌ FULL ADMIN ACCESS!
```

> [!CAUTION]
> **Rủi ro nghiêm trọng cho doanh nghiệp:**
> 1. Static API key trong `site_config.json` — nếu leak là mất toàn bộ hệ thống
> 2. Không có brute-force protection / rate limit
> 3. Không có audit log cho admin login
> 4. Không có 2FA cho admin access
> 5. Guest user có thể gọi API này → AI pentest tool sẽ tìm ra trong vài phút

---

### 🔴 CRITICAL #4: Không Có "Forgot Password" Trong Custom Auth UI

**File:** [Auth.vue](file:///d:/du%20an/educore/frontend/src/pages/Auth.vue)

- Login form chỉ có Email + Password
- **KHÔNG CÓ** link "Quên mật khẩu?"
- **KHÔNG CÓ** email verification khi đăng ký
- Frappe có sẵn `reset_password` API (đã whitelist ở `lms/auth.py` line 47) nhưng UI chưa sử dụng

> [!WARNING]
> Mọi ứng dụng doanh nghiệp **BẮT BUỘC** phải có forgot password. Không có = không bán được.

---

### 🔴 CRITICAL #5: Auth.vue Thiếu Tab Admin Trong UI Công Khai

**File:** [Auth.vue](file:///d:/du%20an/educore/frontend/src/pages/Auth.vue#L25-L34)

Tab "Admin (Key)" hiện **công khai** cho tất cả user, kể cả khách:

```html
<button @click="activeTab = 'admin'">
    {{ __('Admin (Key)') }}
</button>
```

> [!WARNING]
> Người dùng bình thường không nên biết sự tồn tại của admin backdoor. Doanh nghiệp sẽ đặt câu hỏi về bảo mật ngay khi nhìn thấy tab này.

---

### 🟡 HIGH #6: `get_unit_manager_dashboard` Không Kiểm Tra Quyền Manager

**File:** [api.py](file:///d:/du%20an/educore/lms/lms/api.py#L2830-L2916)

```python
@frappe.whitelist()
def get_unit_manager_dashboard(course=None, ...):
    user = frappe.session.user
    # Fallback: nếu không có managed_users → xem TẤT CẢ users
    if not managed_users and ("Moderator" in roles or "System Manager" in roles):
        managed_users = frappe.get_all("User", ...)
```

- Bất kỳ user đã login nào cũng gọi được API này
- Nếu user không có `managed_users` nhưng có role Moderator → thấy ALL users
- **KHÔNG CÓ** `frappe.only_for()` guard

---

### 🟡 HIGH #7: N+1 Query Problem Trong Dashboard

**File:** [api.py](file:///d:/du%20an/educore/lms/lms/api.py#L2864-L2899)

```python
for e in enrollments:          # Có thể 10,000+ enrollments
    if e.progress < 100:
        user_doc = frappe.get_cached_value(...)       # Query 1 per user
        course_title = frappe.get_cached_value(...)    # Query 2 per enrollment

for be in batch_enrollments:   # Lại loop nữa
    batch_end = frappe.get_cached_value(...)           # Query per batch
    for c in batch_courses:                            # Nested loop!
        prog = frappe.db.get_value(...)                # Query per course per user
```

> [!WARNING]
> Với 500 nhân sự × 10 khóa = 5,000+ queries chỉ cho 1 lần load dashboard. Doanh nghiệp 1000+ người sẽ timeout.

---

### 🟡 HIGH #8: Course List API Mở Cho Guest Với Query Injection Risk

**File:** [utils.py](file:///d:/du%20an/educore/lms/lms/utils.py#L778-L800)

```python
@frappe.whitelist(allow_guest=True)
def get_courses(filters: dict = None, start: int = 0):
    # filters được pass trực tiếp từ client vào frappe.get_all()
    # Frappe có built-in sanitization, nhưng custom filters chưa được validate
```

---

## 🟡 VẤN ĐỀ TRUNG BÌNH — NÊN SỬA TRƯỚC KHI BÁN

### 9. Giao Diện Auth Quá Cơ Bản
- Trang login chỉ là form đơn giản Tailwind trắng/xám
- Không có logo, không có branding "Viettel Academy"
- Placeholder "John Doe" không phù hợp thị trường Việt Nam
- Không có animation, hover effect, hay visual appeal nào

### 10. Thiếu Error Boundary / Loading State Đồng Bộ
- `ManagerHome.vue` gọi 2 resources (`dashboardStats`, `courses`) nhưng chỉ check loading cho 1
- Không có error state khi API thất bại — UI sẽ trắng xóa

### 11. Export Báo Cáo Chỉ CSV — Thiếu Excel/PDF
- Doanh nghiệp thường cần: PDF cho print, Excel cho phân tích
- CSV export thiếu cột ngày bắt đầu, deadline, phòng ban chi tiết

### 12. Không Có Audit Trail
- Không log ai login, lúc nào, từ IP nào
- Không log thay đổi enrollment, grade, certificate
- Doanh nghiệp compliance (ISO, SOC2) yêu cầu bắt buộc

### 13. Không Có Multi-tenancy / Org Isolation
- Mọi data trong 1 Frappe site — không tách biệt giữa các tổ chức/đơn vị
- Nếu bán cho nhiều khách hàng → mỗi khách cần 1 instance riêng

### 14. Thiếu i18n Nhất Quán
- Mix tiếng Anh và tiếng Việt: `__('Hey')` + `'Viettel Academy'` + `__('Quản lý khóa học')`
- Placeholder "John Doe" thay vì "Nguyễn Văn A"
- Subtitle hardcode tiếng Việt nhưng wrapper `__()` không hoạt động

---

## 📋 Checklist Sẵn Sàng Cho Doanh Nghiệp

| # | Hạng mục | Trạng thái | Ghi chú |
|---|---|---|---|
| 1 | Login/Sign-up hoạt động | ✅ Có | Nhưng thiếu security |
| 2 | Password policy | ❌ Thiếu | Chấp nhận bất kỳ password |
| 3 | Forgot Password | ❌ Thiếu | Backend sẵn sàng, UI chưa có |
| 4 | Email verification | ❌ Thiếu | Auto-login ngay sau sign-up |
| 5 | Admin 2FA | ❌ Thiếu | Chỉ static key |
| 6 | Course Management | ✅ Hoàn chỉnh | CRUD + SCORM + Import/Export |
| 7 | Student Enrollment | ✅ Hoàn chỉnh | Manual + Batch + Payment |
| 8 | Quiz/Assessment | ✅ Hoàn chỉnh | MCQ + Programming + Grade |
| 9 | Certificate | ✅ Hoàn chỉnh | Template + Evaluation workflow |
| 10 | Progress Tracking | ✅ Hoàn chỉnh | Lesson + Course + Program |
| 11 | Manager Dashboard | ✅ Có | Cần optimize performance |
| 12 | Reports | ✅ 9 loại | Cần thêm export format |
| 13 | Payment | ✅ Có | Razorpay + coupon |
| 14 | Mobile responsive | ✅ Có | Separate layout |
| 15 | Branding customizable | ✅ Có | Logo, favicon, tên |
| 16 | Audit logging | ❌ Thiếu | Bắt buộc cho enterprise |
| 17 | Debug code removed | ❌ Chưa | 4 print() trong production |
| 18 | Rate limiting auth | ❌ Thiếu | sign_up, admin_login không rate limit |
| 19 | Data export (Excel/PDF) | ❌ Thiếu | Chỉ CSV |
| 20 | API documentation | ❌ Thiếu | 2900+ dòng API không có docs |

---

## 🎯 Roadmap Đề Xuất (Ưu Tiên)

### Phase 1 — Sửa Khẩn Cấp (1-2 ngày)
1. ❌ **Xóa tất cả `print()` debug statements** trong `utils.py`
2. ❌ **Thêm password validation** cho `sign_up()` — min 8 chars, 1 uppercase, 1 number
3. ❌ **Thêm `@rate_limit` cho `sign_up()` và `admin_login()`**
4. ❌ **Ẩn tab Admin** khỏi Auth.vue — chuyển sang URL ẩn `/admin-login`
5. ❌ **Thêm `frappe.only_for()`** vào `get_unit_manager_dashboard()`

### Phase 2 — Enterprise Features (3-5 ngày)
6. Thêm **"Quên mật khẩu"** vào Auth.vue
7. Thêm **email verification** trước khi active account
8. **Optimize N+1 queries** trong dashboard API — dùng batch query
9. Thiết kế lại **Auth.vue** — thêm branding, animation, localization VN
10. Thêm **audit trail** — login events, enrollment changes

### Phase 3 — Polish (1 tuần)
11. Export báo cáo **Excel (XLSX)** + **PDF**
12. API documentation — Swagger/OpenAPI
13. End-to-end testing — Cypress (thư mục đã có nhưng chưa thấy tests)
14. Bỏ admin API key mechanism → dùng Frappe standard login + 2FA

---

## 💰 Kết Luận

### Điểm mạnh nổi bật:
EduCore có **kiến trúc vững chắc**, tính năng nghiệp vụ rất đầy đủ (76 doctypes, 9 báo cáo, SCORM, certificate workflow). Hệ thống phân quyền lesson/quiz/file được triển khai chuyên nghiệp. Đây là nền tảng **tốt** để phát triển thành sản phẩm thương mại.

### Vấn đề chặn bán hàng:
Tuy nhiên, **5 vấn đề CRITICAL (#1-#5)** liên quan đến **bảo mật** khiến ứng dụng **CHƯA THỂ bán cho doanh nghiệp**. Đặc biệt:
- Admin static key + public tab = rủi ro bị hack toàn bộ
- Không password policy + không rate limit = tạo tài khoản vô tội vạ  
- Debug `print()` = vi phạm data privacy

### Ước tính công sức sửa:
- Phase 1 (bắt buộc): **2 ngày** → sau đó có thể demo cho khách
- Phase 1+2: **1 tuần** → có thể bán pilot  
- Phase 1+2+3: **2-3 tuần** → sản phẩm production-ready

> [!IMPORTANT]
> **Tóm lại:** Sản phẩm có ~80% features cần thiết. Cần ~20% effort sửa bảo mật + polish thì mới sẵn sàng bán. Ưu tiên **Phase 1** trước — chỉ cần 2 ngày là có thể demo an toàn.
