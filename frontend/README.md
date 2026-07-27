# 🎓 EduCore LMS - Frontend Documentation

Frontend cho hệ thống **EduCore (Frappe Learning)** được xây dựng bằng **Vue 3**, **Vite 5**, **Frappe UI** và **TailwindCSS 3**.

---

## 🛠️ Công Nghệ & Thư Viện

| Công nghệ | Version / Thư viện | Vai trò |
|---|---|---|
| **Framework** | Vue 3.5+ (Composition API) | UI Component & View Logic |
| **Build Tool** | Vite 5.0 | Hỗ trợ HMR siêu nhanh & Build bundle |
| **UI Library** | Frappe UI (v1.0-beta) | Component UI chuẩn Frappe |
| **Styling** | TailwindCSS 3.4 | Utility-first CSS framework |
| **State** | Pinia 2.0 | Quản lý global state (user, session, settings) |
| **Testing** | Vitest 4.1 | Unit test runner cho Vue components |
| **Editor** | EditorJS 2.29 | Rich-text block editor cho bài học |
| **Media Player** | Plyr 3.7 | Video/Audio player hỗ trợ HLS, YouTube |

---

## 🚀 Hướng Dẫn Chạy Local (Quickstart)

### 1. Cài Đặt Dependencies
Chạy command sau tại thư mục `frontend`:
```bash
npm install
```

### 2. Môi Trường Dev (Development Server)
```bash
npm run dev
```
Dev server sẽ khởi chạy tại `http://localhost:8085` (hoặc port cấu hình qua biến `VITE_PORT`).

> [!TIP]
> Để không bị lỗi CSRF khi gọi API tới Frappe Backend `:8000`, thêm cấu hình sau vào `site_config.json` của Frappe site:
> ```json
> "ignore_csrf": 1
> ```

### 3. Kiểm Tra Unit Test
Chạy toàn bộ 42 unit test suites (393 tests):
```bash
npm run test
```
Để chạy test ở chế độ watch mode khi code:
```bash
npm run test:watch
```

### 4. Build Production Bundle
Build các tài sản static xuất ra thư mục `../lms/public/frontend` và tự động cập nhật `_lms.html`:
```bash
npm run build
```

---

## 📁 Cấu Trúc Thư Mục Frontend

```
frontend/
├── src/
│   ├── assets/         # Images, SVG icons & static assets
│   ├── components/     # Vue UI Components (CourseOutline, Quiz, BlockEditor...)
│   ├── pages/          # Vue Pages (Home, Courses, Lesson, Batches, Profile...)
│   ├── stores/         # Pinia Stores (user.js, session.js, settings.js...)
│   ├── tests/          # Vitest Unit Tests (42 test suites)
│   ├── router.js       # Vue Router mapping 30+ routes
│   ├── socket.js       # Socket.IO connection handling
│   └── main.js         # Entry point initialization
├── vite.config.js      # Vite build & Frappe proxy configuration
└── package.json        # Dependencies & NPM Scripts
```

---

## 📋 Danh Sách Command Chi Tiết

- `npm run dev`: Chạy Vite development server với HMR.
- `npm run build`: Build production bundle sang `../lms/public/frontend`.
- `npm run test`: Chạy toàn bộ Vitest unit test.
- `npm run test:watch`: Chạy Vitest ở chế độ tương tác (watch mode).
- `npm run serve`: Preview production build tại local.
