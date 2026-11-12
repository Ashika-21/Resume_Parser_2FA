# AI-Powered Resume Parser & Email OTP Onboarding Pipeline

## Project Overview

This project is developed using Python and FastAPI. It helps users upload their resumes and automatically extract important information such as name, email, phone number, skills and experience.

The project also provides user registration, email OTP verification, login authentication and profile management.

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- PyMuPDF / pdfplumber
- Argon2 Password Hashing
- JWT Authentication
- Gmail SMTP
- Python-docx

## Main Features

1. **Resume Upload:** Users can upload PDF and DOCX resumes.
2. **Resume Parsing:** Extracts name, email, phone number, skills and experience.
3. **Database Storage:** Stores user and resume details in PostgreSQL.
4. **User Registration:** Allows users to create an account.
5. **Email OTP Verification:** Sends a six-digit OTP to the registered email.
6. **Password Security:** Uses Argon2 to hash passwords.
7. **Login Authentication:** Uses JWT access tokens.
8. **Profile Management:** Users can view and update their profile.
9. **Student Dashboard:** Provides an authenticated dashboard.

## Project Structure

```text
Resume_Parser_2FA/
│
├── main.py
├── database.py
├── models/
│   ├── user.py
│   ├── resume.py
│   └── otp.py
│
├── schemas/
│   ├── auth.py
│   └── profile.py
│
├── routers/
│   ├── resume.py
│   ├── auth.py
│   ├── profile.py
│   └── dashboard.py
│
├── services/
│   ├── resume_parser.py
│   ├── password_service.py
│   ├── otp_service.py
│   ├── email_service.py
│   └── token_service.py
│
├── alembic/
├── requirements.txt
├── .env
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project

```bash
cd Resume_Parser_2FA
```

### 3. Create Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

```bash
.venv\Scripts\activate
```

### 5. Install Requirements

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file and add the following settings:

```env
DATABASE_URL=your_postgresql_database_url
JWT_SECRET_KEY=your_secret_key

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_gmail_app_password
SENDER_EMAIL=your_email
```

Use your own database and email configuration. Do not upload `.env` to GitHub.

### 7. Run the Application

```bash
uvicorn main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/resume/parse` | Upload and parse resume |
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/request-otp/{user_id}` | Send email OTP |
| POST | `/api/v1/auth/verify-2fa` | Verify email OTP |
| POST | `/api/v1/auth/login` | User login |
| GET | `/api/v1/profile` | View profile |
| PATCH | `/api/v1/profile` | Update profile |
| GET | `/api/v1/dashboard/student` | Student dashboard |

## Conclusion

This project helped me understand FastAPI, PostgreSQL, resume parsing, password hashing, email OTP verification and JWT authentication.

It also gave me practical experience in developing backend APIs and connecting them with a database and email service.