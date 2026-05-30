# TaskFlow — Task Management Web App

A full-stack web application with Python Flask backend, MySQL database, JWT authentication, and a sleek dark-themed frontend.

---

## 📁 Project Structure

```
task_manager/
├── backend/
│   ├── __init__.py         # App factory, DB & JWT init
│   ├── models.py           # SQLAlchemy models (User, Task)
│   └── routes/
│       ├── auth.py         # /api/auth/* endpoints
│       ├── tasks.py        # /api/tasks/* endpoints
│       └── views.py        # HTML page routes
├── frontend/
│   └── templates/
│       ├── login.html
│       ├── register.html
│       └── dashboard.html
├── .env                    # Environment variables (edit this!)
├── db_setup.sql            # MySQL database setup
├── requirements.txt
└── run.py                  # Entry point
```

---

## 🚀 Setup Instructions

### 1. Prerequisites
- Python 3.9+
- MySQL 5.7+ or 8.x

### 2. Create & activate a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database
```bash
mysql -u root -p < db_setup.sql
```

### 5. Configure environment variables
Edit the `.env` file with your MySQL credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=task_manager_db
JWT_SECRET_KEY=change-this-secret
SECRET_KEY=change-this-flask-secret
```

### 6. Run the application
```bash
python run.py
```

Visit **http://localhost:5000** in your browser.

---

## 🔌 API Endpoints

### Auth
| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login`    | Login, get JWT token | ❌ |
| GET  | `/api/auth/profile`  | Get current user | ✅ |
| PUT  | `/api/auth/profile`  | Update username/password | ✅ |

### Tasks (all require JWT Bearer token)
| Method | URL | Description |
|--------|-----|-------------|
| GET    | `/api/tasks`             | List tasks (filter: `?status=Pending`, `?search=keyword`) |
| POST   | `/api/tasks`             | Create task |
| GET    | `/api/tasks/<id>`        | Get single task |
| PUT    | `/api/tasks/<id>`        | Update task |
| DELETE | `/api/tasks/<id>`        | Delete task |
| GET    | `/api/tasks/stats`       | Get task count statistics |

### Request/Response Examples

**POST /api/auth/login**
```json
Request:  { "email": "user@example.com", "password": "mypassword" }
Response: { "token": "eyJ...", "user": { "id": 1, "username": "john", ... } }
```

**POST /api/tasks**
```json
Request:  { "title": "Fix bug #42", "description": "...", "due_date": "2024-12-31", "status": "Pending" }
Response: { "message": "Task created", "task": { "id": 1, "title": "Fix bug #42", ... } }
```

**PUT /api/tasks/1**
```json
Request:  { "status": "Completed" }
Response: { "message": "Task updated", "task": { ... } }
```

---

## 🎯 Features

- ✅ JWT-based authentication (register, login, logout)
- ✅ Full CRUD for tasks
- ✅ Filter tasks by status (Pending / In Progress / Completed)
- ✅ Live search by task title
- ✅ Task statistics dashboard
- ✅ Overdue date highlighting
- ✅ Dark-themed, responsive UI
- ✅ Keyboard shortcuts (Ctrl+K = new task, Esc = close modal)

---

## 🛡️ Security Notes

- Passwords are hashed with bcrypt (never stored in plain text)
- JWT tokens protect all task endpoints
- Users can only access their own tasks
- All user input is validated server-side
- Change `JWT_SECRET_KEY` and `SECRET_KEY` before deploying!
