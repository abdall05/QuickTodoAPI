# 📌 Task Management API

A simple **FastAPI + SQLModel** project built to practice REST API design, authentication, and database handling.  
This project uses **SQLite** as the database for simplicity.

## 🚀 Features

✅ JWT-based Authentication  
✅ User Signup & Login  
✅ Get Current User (`/users/me`)  
✅ CRUD for Tasks (per user)  
✅ Admin-only User Management

## 📚 API Endpoints

### 🔑 Auth

| Method | Endpoint       | Description                 |
|--------|----------------|-----------------------------|
| POST   | `/auth/signup` | Create a new user account   |
| POST   | `/auth/login`  | Login and receive JWT token |

### 👥 Users

| Method | Endpoint           | Description                     |
|--------|--------------------|---------------------------------|
| GET    | `/users/`          | Get all users (**admin only**)  |
| GET    | `/users/{user_id}` | Get user by ID (**admin only**) |
| DELETE | `/users/{user_id}` | Delete user (**admin only**)    |
| GET    | `/users/me`        | Get current logged-in user info |

### ✅ Tasks

| Method | Endpoint           | Description                                    |
|--------|--------------------|------------------------------------------------|
| GET    | `/tasks/`          | Get all tasks for the authenticated user       |
| GET    | `/tasks/{task_id}` | Get a specific task (must belong to user)      |
| POST   | `/tasks/`          | Create a new task for the authenticated user   |
| PATCH  | `/tasks/{task_id}` | Update a specific task (must belong to user)   |
| DELETE | `/tasks/{task_id}` | Delete a specific task (must belong to user)   |
| DELETE | `/tasks/`          | Delete **all tasks of the authenticated user** |

## 🛠 Setup & Installation

Clone the repository:

```bash
git clone https://github.com/abdall05/QuickTodoAPI.git
cd QuickTodoAPI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app.main:app --reload
```

Open in your browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)  
Here you can **interactively explore all endpoints, see request and response schemas, try example requests, and check
model structures**.

## 🧪 Example Payloads

## 1️⃣ Signup

{
  "username": "john123",
  "email": "john@example.com",
  "name": "John Doe",
  "password": "strongpassword",
  "password_confirm": "strongpassword"
}

## 2️⃣ Login

POST /auth/login  
Content-Type: application/x-www-form-urlencoded

Fields:
- username: Your username
- password: Your password

Example using curl:

curl -X POST "http://127.0.0.1:8000/auth/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=john123&password=strongpassword"

Example Response:

{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6InVzZXIiLCJleHAiOjE3NTg1MjcyMDV9.4D0TNpjUxRSulNCogLYyuLfKLj6zPFXnahr3_JkJ47M",
    "token_type": "Bearer"
}

Use the returned access_token from login in the Authorization header:  
Authorization: Bearer <token>

## 3️⃣ Create a Task

POST /tasks/  
JSON Payload:

{
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs"
}

Example Response:

{
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs",
    "id": 3,
    "completed": false,
    "created_at": "2025-09-22T07:15:47.040381"
}

## 4️⃣ Update a Task (Mark as Completed)

PATCH /tasks/{task_id}  
JSON Payload:

{
    "completed": true
}

Example Response:

{
    "title": "Buy groceries",
    "description": "Milk, Bread, Eggs",
    "id": 3,
    "completed": true,
    "created_at": "2025-09-22T07:15:47.040381"
}

## 5️⃣ Get All Tasks

GET /tasks/  
Header: Authorization: Bearer <token>

Example Response:

[
    {
        "title": "CP",
        "description": "30 minutes",
        "id": 2,
        "completed": false,
        "created_at": "2025-09-22T07:02:13.563533"
    },
    {
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs",
        "id": 3,
        "completed": false,
        "created_at": "2025-09-22T07:15:47.040381"
    }
]

## 6️⃣ Delete a Task

DELETE /tasks/{task_id}  
Header: Authorization: Bearer <token>

Example Response: 204 No Content

## 7️⃣ Delete All Tasks

DELETE /tasks/  
Header: Authorization: Bearer <token>

Example Response: 204 No Content

### 8️⃣ Get Current User
GET /users/me  
Header: Authorization: Bearer <token>

Example Response:
{
  "username": "ali99",
  "name": "ali",
  "id": 1,
  "role": "user"
}


## 🗄 Database Schema

**users**
| Column | Type | Notes |
|--------------|----------|-------------------------------|
| id | int (PK) | Auto-increment |
| username | str | Unique, required |
| name | str | Required |
| password_hash| str | Stored as hash |
| role | enum | USER or ADMIN, default = USER |

**tasks**
| Column | Type | Notes |
|--------------|----------|----------------------------------------|
| id | int (PK) | Auto-increment |
| title | str | Required |
| description | str | Optional |
| completed | bool | Default = False |
| created_at | datetime | Default = UTC now |
| user_id | int (FK) | References users.id, `CASCADE` on delete|

**Relationships**

- `User.tasks` → list of tasks for that user (`back_populates="user"`)
- `Task.user` → the owner user of the task (`back_populates="tasks"`)
- 
## 🚀 Future Improvements

- Add **email-based password recovery** (forgot password) functionality.  
  Users can request a password reset link via email to securely update their password.

- Implement **email verification** upon signup to ensure valid user accounts.

- Add **pagination and filtering** for tasks and users endpoints.


## 📄 License

MIT License - free to use for learning and personal projects.

## 🙌 Author

**Ali Abdallah**  
Practice project using [FastAPI](https://fastapi.tiangolo.com/) + [SQLModel](https://sqlmodel.tiangolo.com/)
