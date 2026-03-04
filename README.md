# User Management Portal

A full-stack user management system built with **FastAPI**, **MongoDB**, and **Vanilla JavaScript**.

---

## 🚀 Features

- ✅ User Signup & Login
- ✅ Single Admin Login (pre-seeded)
- ✅ JWT Authentication with bcrypt password hashing
- ✅ Role-based Authorization (admin / user)
- ✅ User Profile — Create & Update
- ✅ Admin Dashboard — View all users, Suspend, Delete
- ✅ Real-time reflection (admin sees live user updates every 5s)

---

## 🗂 Project Structure

```
softline-user-admin-portal/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── database.py        # MongoDB connection (Motor)
│   │   ├── models.py          # Document helper / structure
│   │   ├── schemas.py         # Pydantic request/response models
│   │   ├── auth.py            # JWT + password utilities
│   │   ├── dependencies.py    # Route guards (auth, admin)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth_routes.py  # /api/auth/signup, /api/auth/login
│   │       ├── user_routes.py  # /api/user/profile (GET, PUT)
│   │       └── admin_routes.py # /api/admin/users (CRUD)
│   │
│   ├── .env                   # Environment variables
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore
│
└── frontend/
    ├── index.html             # Redirect to login
    ├── login.html             # Login page
    ├── signup.html            # Signup page
    ├── user.html              # User profile dashboard
    ├── admin.html             # Admin dashboard
    ├── css/
    │   └── style.css          # Global styles
    └── js/
        ├── api.js             # Shared API helper & auth
        ├── login.js           # Login page logic
        ├── signup.js          # Signup page logic
        ├── user.js            # User dashboard logic
        └── admin.js           # Admin dashboard logic
```

---

## 📋 Prerequisites

- **Python 3.10+**
- **MongoDB** running locally (default: `mongodb://localhost:27017`)
  _Or use [MongoDB Atlas](https://www.mongodb.com/atlas) — update `MONGO_URI` in `.env`_

---

## ⚡ Quick Start

### 1. Navigate to the project

```bash
cd softline-user-admin-portal
```

### 2. Set up the backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

Edit `backend/.env` if needed:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=user_management_portal
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_EMAIL=admin@portal.com
ADMIN_PASSWORD=Admin@123
```

### 4. Start MongoDB

Make sure MongoDB is running:

```bash
# If using mongod directly:
mongod

# Or if using Docker:
docker run -d -p 27017:27017 --name mongodb mongo:7
```

### 5. Run the server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open in browser

```
http://localhost:8000
```

---

## 🔑 Default Admin Credentials

| Field    | Value             |
|----------|-------------------|
| Email    | `admin@portal.com`|
| Password | `Admin@123`       |

> The admin account is **auto-created** on first server startup.

---

## 📡 API Endpoints

### Auth

| Method | Endpoint          | Description        | Auth Required |
|--------|-------------------|--------------------|:------------:|
| POST   | `/api/auth/signup` | Register new user  | ❌           |
| POST   | `/api/auth/login`  | Login (user/admin) | ❌           |

### User

| Method | Endpoint           | Description       | Auth Required |
|--------|--------------------|--------------------|:------------:|
| GET    | `/api/user/profile` | Get own profile   | ✅ User      |
| PUT    | `/api/user/profile` | Update profile    | ✅ User      |

### Admin

| Method | Endpoint                         | Description       | Auth Required |
|--------|----------------------------------|--------------------|:------------:|
| GET    | `/api/admin/users`               | List all users     | ✅ Admin     |
| GET    | `/api/admin/users/{id}`          | Get single user    | ✅ Admin     |
| DELETE | `/api/admin/users/{id}`          | Delete user        | ✅ Admin     |
| PATCH  | `/api/admin/users/{id}/suspend`  | Toggle suspend     | ✅ Admin     |

---

## 📄 MongoDB Document Structure

```json
{
    "_id": "ObjectId(...)",
    "email": "user@example.com",
    "password": "$2b$12$...",
    "role": "user",
    "name": "John Doe",
    "phone": "+1234567890",
    "address": "123 Main St, City",
    "is_active": true,
    "created_at": "2026-03-01T00:00:00+00:00",
    "updated_at": "2026-03-01T00:00:00+00:00"
}
```

---

## 🧪 Testing the Flow

1. Open `http://localhost:8000` → redirects to Login page
2. Click **Sign Up** → create a user account → redirected to User Dashboard
3. Update profile (name, phone, address) → click Save
4. **Logout** → Login as admin (`admin@portal.com` / `Admin@123`)
5. Admin Dashboard shows the user with updated data
6. Try **Suspend** or **Delete** actions

---

## 🛡 Security Notes

- Passwords are hashed with **bcrypt** (never stored in plain text)
- JWT tokens expire after **60 minutes** (configurable)
- Admin routes are protected — only `role: admin` can access
- User routes require valid JWT token
- CORS is set to `*` for development — **restrict in production**