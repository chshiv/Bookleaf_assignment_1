# 📚 Bookleaf Publishing – Royalty Management API

This project is a backend API for managing authors, books, sales, royalties, and withdrawals for a publishing platform.

---

## 🚀 Tech Stack Used

- **FastAPI (Python)**  
  Chosen for its high performance, built-in request validation, automatic API documentation, and async support. It is ideal for scalable backend services.

- **Python**  
  Python is highly compatible with AI and ML ecosystems. This ensures future extensibility without changing the tech stack, such as:
  - AI-powered chatbot for authors
  - Smart sales insights & analytics
  - Automated royalty prediction systems

- **SQLite (In-memory / File-based)**  
  Used as a lightweight database for simplicity and quick setup within the assignment scope.

- **SQLAlchemy ORM**  
  Used for clean database abstraction, maintainable queries, and easy migration to other databases like PostgreSQL or MySQL in the future.

---


## 📂 Project Directory Structure

```
assignment-1/
├── database/
│   └── database.py          # Database connection & session management
│
├── models/
│   └── royalty_models.py    # SQLAlchemy models (Author, Book, Sale, Withdrawal)
│
├── routes/
│   └── royalty_apis.py      # API route definitions
│
├── services/
│   └── royalty_service.py   # Business logic & database operations
│
├── utils/
│   ├── logger.py            # Centralized logging configuration
│   └── validation.py       # Request payload validation logic
│
├── logs/                    # Application logs
├── seed.py                  # Database seeding script
├── main.py                  # FastAPI application entry point
├── royalty.db               # SQLite database file
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```


Readme · MD
Copy

# Project Setup Guide

## ▶️ How to Run the Project

### 1️⃣ Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv assignment-1

# Activate virtual environment (Windows)
assignment-1\Scripts\activate

# Activate virtual environment (Linux/Mac)
source assignment-1/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start the Server

```bash
uvicorn main:app --reload
```

## 📘 API Documentation

FastAPI provides automatic interactive API documentation.

After starting the server, open your browser and navigate to:

```
http://localhost:8000/docs
```

### What You Can Do:

- ✅ View all available APIs
- ✅ See request and response schemas
- ✅ Test APIs directly from the browser

## 📌 Assumptions Made

- **Dynamic Calculations**: Author total earnings and current balance are calculated dynamically from sales and withdrawals
- **Withdrawal Status**: Withdrawals are created with an initial status of `pending`
- **Database Design**: The design supports easy migration to enterprise databases like PostgreSQL or MySQL
- **Authentication**: Authentication and authorization are out of scope for this assignment

---

## ⏱️ Time Spent

**Total Time Spent: 12 hours**

| Task | Time |
|------|------|
| Database design & models | 1 hours |
| API implementation | 3 hours |
| Business logic & validations | 3 hours |
| Error handling & logging | 2 hours |
| Testing & documentation | 3 hour |

---
