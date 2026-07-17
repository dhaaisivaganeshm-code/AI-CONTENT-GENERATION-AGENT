# 🚀 AI Content Generation Agent

An AI-powered content generation application built with **React**, **FastAPI**, **MongoDB**, and the **Groq API**. The application provides secure user authentication and an AI chat interface for generating content.

---

# 📌 Features

* 🔐 User Registration & Login (JWT Authentication)
* 🤖 AI-powered chat using the Groq API
* 💬 Chat history stored in MongoDB
* ⚡ FastAPI backend
* 🎨 React frontend
* 📖 Interactive API documentation (Swagger UI)

---

# 🛠️ Tech Stack

## Frontend

* React.js
* JavaScript
* HTML
* CSS

## Backend

* FastAPI
* Python 3.12
* Uvicorn

## Database

* MongoDB

## AI

* Groq API

---

# 📂 Project Structure

```text
AI-CONTENT-GENERATION-AGENT/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│
├── .gitignore
└── README.md
```

---

# ⚙️ Prerequisites

Install the following before running the project:

* Python 3.12 or later
* Node.js (v18 or later recommended)
* npm
* MongoDB (local or MongoDB Atlas)
* Git
* Groq API Key

---

# 📥 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Content-Generation-Agent.git
```

```bash
cd AI-Content-Generation-Agent
```

---

## 2. Backend Setup

Move into the backend folder:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
```

Activate the virtual environment:

**PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a file named `.env` inside the `backend` folder.

Example:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=ai_content_db

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

GROQ_API_KEY=your_groq_api_key
```

---

## 4. Run the Backend

From the `backend` directory:

```bash
python -m uvicorn app.main:app --reload
```

If successful, you'll see output similar to:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 5. Frontend Setup

Open a new terminal.

Go to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will typically be available at:

```text
http://localhost:5173
```

---

# ▶️ Running the Project

### Terminal 1 (Backend)

```bash
cd backend

.venv\Scripts\Activate.ps1

python -m uvicorn app.main:app --reload
```

### Terminal 2 (Frontend)

```bash
cd frontend

npm run dev
```

Open your browser and visit:

```text
Frontend:
http://localhost:5173

Backend:
http://127.0.0.1:8000

Swagger API Docs:
http://127.0.0.1:8000/docs
```

---

# 🧪 API Endpoints

## Authentication

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/api/auth/register` |
| POST   | `/api/auth/login`    |
| GET    | `/api/auth/me`       |

## Chat

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | `/api/chat/send` |
| GET    | `/api/chat/list` |

---





# 🔒 Security

* JWT Authentication
* Password Hashing with bcrypt
* Environment Variables
* Protected API Routes

---

# 📝 License

This project is licensed under the MIT License.

---

