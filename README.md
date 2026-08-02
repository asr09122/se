# 🚗 Campus Auto-Ride Sharing Platform API

A robust, RESTful Django backend designed for managing campus e-mobility and auto-rickshaw ride-sharing operations. It handles passenger bookings, driver location updates, real-time availability filtering, ride lifecycle management, and historical trip logs.

---

## 🏗️ Architecture Overview

The system is structured as modular Django applications communicating over HTTP/REST APIs:

- **[`app`](file:///Users/abhayjotsingh/asr09122_repos/se/app)**: Core Django application setup, URL routing configuration, WSGI/ASGI servers, and settings.
- **[`DriverApi`](file:///Users/abhayjotsingh/asr09122_repos/se/DriverApi)**: Manages auto driver registration, authentication tokens, GPS location tracking updates, active ride acceptance, ride cancellation/completion, and driver earnings/trip history.
- **[`PassengerApi`](file:///Users/abhayjotsingh/asr09122_repos/se/PassengerApi)**: Handles passenger registration (campus students), finding nearby available drivers based on GPS radius filtering, booking rides, cancelling pending rides, and personal travel history.

---

## 🛠️ Technology Stack

- **Framework**: Django 5.1.2 & Django REST Framework (DRF)
- **Database**: SQLite (Development) / Relational DB ready
- **Authentication**: Django REST Framework Token Authentication (`rest_framework.authtoken`)
- **CORS & Static Files**: `django-cors-headers`, `whitenoise`
- **Language**: Python 3.12+

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have **Python 3.12+** installed on your system.

### 2. Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd se
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers asgiref sqlparse tzdata whitenoise
   ```

4. **Apply Database Migrations**:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

5. **Start Development Server**:
   ```bash
   python3 manage.py runserver
   ```
   The API will be available at: `http://127.0.0.1:8000/`

---

## 📡 API Endpoints Specification

### 👤 Passenger Endpoints (`/api/passenger/`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/passenger/signup/` | Register a new passenger account | No |
| `POST` | `/api/passenger/login/` | Authenticate passenger & get API Token | No |
| `POST` | `/api/passenger/logout/` | Invalidate passenger token | Yes |
| `POST` | `/api/passenger/nearby-drivers/` | Find available drivers within radius | Yes |
| `POST` | `/api/passenger/book-ride/` | Create a new ride booking request | Yes |
| `POST` | `/api/passenger/cancel-ride/` | Cancel an active ride request | Yes |
| `GET`  | `/api/passenger/history/` | View personal travel history | Yes |

---

### 🛺 Driver Endpoints (`/api/driver/`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/driver/signup/` | Register a new driver account | No |
| `POST` | `/api/driver/login/` | Authenticate driver & get API Token | No |
| `POST` | `/api/driver/logout/` | Invalidate driver token & clear active bookings | Yes |
| `PUT`  | `/api/driver/update-location/` | Update live latitude & longitude coordinates | Yes |
| `GET`  | `/api/driver/current-booked-ride/` | Fetch current active booking details | Yes |
| `POST` | `/api/driver/complete-ride/` | Mark ride completed & move to history | Yes |
| `POST` | `/api/driver/Cancel-ride/` | Cancel active ride request | Yes |
| `GET`  | `/api/driver/rides-history/` | View driver completed trip history | Yes |

---

## 🔑 Authentication Usage

Protected endpoints require a token header in the request headers:

```http
Authorization: Token <YOUR_AUTH_TOKEN>
```

---

## 🧪 Testing

The repository includes both modular app tests and an end-to-end integration test suite.

### Run All Unit & Integration Tests:
```bash
python3 manage.py test DriverApi PassengerApi test_complete_project
```

### Run End-to-End Workflow Test Only:
```bash
python3 manage.py test test_complete_project
```

---

## 📌 Project Structure

```text
.
├── DriverApi/               # Driver management app (Models, Views, Serializers, Tests)
├── PassengerApi/            # Passenger management app (Models, Views, Serializers, Tests)
├── app/                     # Main project settings, root URLs, ASGI/WSGI entrypoints
├── manage.py                # Django CLI management script
├── requirements.txt         # Package dependencies
└── test_complete_project.py # End-to-End workflow integration test suite
```
