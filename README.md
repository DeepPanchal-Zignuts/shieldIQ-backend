# Django REST Framework — Production Backend

> A **production-grade** security-awareness platform backend built with Django REST Framework, featuring a clean **Controller → Service → Repository → Model** layered architecture.

ShieldIQ is designed to manage users across organizational departments, track security scores, and power phishing-simulation campaigns — all behind a fully custom JWT authentication system.

---

## Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [Authentication System](#-authentication-system)
- [API Reference](#-api-reference)
- [API Response Format](#-api-response-format)
- [Error Handling](#-error-handling)
- [Adding a New Module](#-adding-a-new-module)
- [Project Conventions](#-project-conventions)
- [License](#-license)

---

## 📁 Architecture Overview

```
shieldIQ-backend/
│
├── config/                     # Django project configuration
│   ├── settings.py             # Single settings file (.env driven)
│   ├── urls.py                 # Root URL router
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
│
├── apps/                       # Domain modules
│   └── users/                  # Authentication & user management
│       ├── controllers/        #   ↳ ViewSets (HTTP ↔ Service bridge)
│       ├── services/           #   ↳ Business logic layer
│       ├── repositories/       #   ↳ ORM / data-access layer
│       ├── models/             #   ↳ Django ORM entities
│       ├── serializers/        #   ↳ Input validation + output shaping
│       └── urls/               #   ↳ URL routing
│
├── core/                       # Framework-level infrastructure
│   └── authentication/         #   ↳ Custom JWT authentication backend
│
├── common/                     # Shared, cross-cutting concerns
│   ├── constants/              #   ↳ Enums, error codes, message strings
│   ├── exceptions/             #   ↳ Custom exceptions + global handler
│   ├── responses/              #   ↳ Standardised API response envelope
│   └── validators/             #   ↳ Reusable validators (email, password)
│
├── utils/                      # Pure helper functions
│   ├── date_utils.py           #   ↳ UTC-aware datetime utilities
│   ├── encryption.py           #   ↳ Password hashing (PBKDF2)
│   ├── token_utils.py          #   ↳ JWT generation & verification
│   └── send_mail.py            #   ↳ Transactional email (HTML + plaintext)
│
├── templates/                  # Django templates
│   └── email/                  #   ↳ verify_email & reset_password templates
│
├── manage.py
├── requirements.txt
└── .gitignore
```

### Layer Responsibilities

```
  HTTP Request
       │
       ▼
┌──────────────┐    Parses request, validates input via serializer,
│  Controller  │    delegates to service, returns ApiResponse.
│  (ViewSet)   │    ✗ Never imports models directly.
└──────┬───────┘
       │
       ▼
┌──────────────┐    Implements business rules, orchestrates
│   Service    │    repositories, sends emails, etc.
│              │    ✗ Never writes raw SQL.
└──────┬───────┘
       │
       ▼
┌──────────────┐    Encapsulates all Django ORM queries.
│  Repository  │    ✗ No business logic.
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Model     │    Django ORM entity definition.
└──────────────┘
```

### Key Design Decisions

| Decision                                       | Rationale                                                                   |
| ---------------------------------------------- | --------------------------------------------------------------------------- |
| **UUID primary keys**                          | Avoids sequential ID enumeration attacks                                    |
| **Tokens stored on User model**                | Single-session enforcement per token type; instant revocation via DB update |
| **Separate request / response serializers**    | Strict separation of input validation from output formatting                |
| **Centralised message & error-code constants** | Zero hardcoded strings in business logic; easy i18n in the future           |
| **Global exception handler**                   | Every error — DRF, Django, or custom — returns the same JSON envelope       |

---

## 🛠 Tech Stack

| Component        | Technology            | Version  |
| ---------------- | --------------------- | -------- |
| Framework        | Django                | 6.0.4    |
| API Layer        | Django REST Framework | 3.17.1   |
| Database         | PostgreSQL            | 15+      |
| Auth             | Custom JWT (PyJWT)    | 2.12.1   |
| Password Hashing | Django PBKDF2         | built-in |
| Env Config       | python-dotenv         | 1.2.2    |
| Language         | Python                | 3.12+    |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
| ----------- | ------- |
| Python      | 3.12+   |
| PostgreSQL  | 15+     |
| pip         | latest  |

### 1 — Clone & Set Up Environment

```bash
git clone <repo-url>
cd shieldIQ-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate       # Windows
```

### 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### 3 — Configure Environment

```bash
cp .env.example .env
# Edit .env — see Environment Variables section below
```

### 4 — Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5 — Run Development Server

```bash
python manage.py runserver
```

The API is now live at **`http://localhost:8000`**.

---

## 🔑 Environment Variables

Create a `.env` file in the project root. All variables are loaded at startup via `python-dotenv`.

| Variable                                  | Description                             | Example                     |
| ----------------------------------------- | --------------------------------------- | --------------------------- |
| `SECRET_KEY`                              | Django secret key                       | `django-insecure-change-me` |
| `DEBUG`                                   | Debug mode toggle                       | `True`                      |
| `ALLOWED_HOSTS`                           | Comma-separated allowed hosts           | `localhost,127.0.0.1`       |
| `DB_NAME`                                 | PostgreSQL database name                | `shieldiq`                  |
| `DB_USER`                                 | Database user                           | `postgres`                  |
| `DB_PASSWORD`                             | Database password                       | `••••••`                    |
| `DB_HOST`                                 | Database host                           | `localhost`                 |
| `DB_PORT`                                 | Database port                           | `5432`                      |
| `ACCESS_TOKEN_LIFETIME_HOURS`             | JWT access token lifetime               | `24`                        |
| `REFRESH_TOKEN_LIFETIME_DAYS`             | JWT refresh token lifetime              | `60`                        |
| `EMAIL_VERIFICATION_TOKEN_LIFETIME_HOURS` | Email verification link expiry          | `24`                        |
| `FORGOT_PASSWORD_TOKEN_LIFETIME`          | Password reset link expiry (hours)      | `1`                         |
| `ACCESS_TOKEN_SECRET_KEY`                 | Signing key for access JWTs             | `<random-secret>`           |
| `REFRESH_TOKEN_SECRET_KEY`                | Signing key for refresh JWTs            | `<random-secret>`           |
| `FRONTEND_URL`                            | Frontend base URL (used in email links) | `http://localhost:3000`     |
| `DEFAULT_FROM_EMAIL`                      | Sender address for transactional emails | `noreply@shieldiq.com`      |

---

## 🔐 Authentication System

ShieldIQ implements a **fully custom JWT authentication system** — no `djangorestframework-simplejwt` views or middleware are used at runtime. Tokens are signed with HS256, stored on the `User` model, and verified on every authenticated request via `core.authentication.jwt_auth.JWTAuthentication`.

### Token Types

| Token                     | Stored In                    | Lifetime            | Secret Key                 | Purpose                            |
| ------------------------- | ---------------------------- | ------------------- | -------------------------- | ---------------------------------- |
| **Access Token**          | `user.access_token`          | 24 h (configurable) | `ACCESS_TOKEN_SECRET_KEY`  | Bearer auth on protected endpoints |
| **Refresh Token**         | `user.refresh_token`         | 60 d (configurable) | `REFRESH_TOKEN_SECRET_KEY` | Issue new access tokens            |
| **Verification Token**    | `user.verification_token`    | 24 h (configurable) | `ACCESS_TOKEN_SECRET_KEY`  | Email verification link            |
| **Forgot Password Token** | `user.forgot_password_token` | 1 h (configurable)  | — (UUID v4, not JWT)       | Password reset link                |

### Auth Flow

```
Register → Verification email sent → Verify email → Login → Access token issued
                                                         ↘ Refresh token issued

Forgot Password → Reset email sent → Reset password → All tokens cleared (forced re-login)

Logout → access_token & refresh_token nullified
```

### Protected Requests

```
Authorization: Bearer <access_token>
```

The custom `JWTAuthentication` backend:

1. Extracts the `Bearer` token from the `Authorization` header
2. Decodes and verifies the JWT signature + expiry
3. Looks up the user by email from the token payload
4. Checks `is_active` status
5. Returns `(user, raw_token)` to DRF

---

## 📡 API Reference

**Base URL:** `http://localhost:8000/api/v1/auth/`

All endpoints are registered via a DRF `DefaultRouter` under the `auth/` prefix.

### Endpoints

| Method | Endpoint                        | Auth | Description                                    |
| ------ | ------------------------------- | ---- | ---------------------------------------------- |
| `POST` | `/api/v1/auth/register/`        | ✗    | Register a new user & send verification email  |
| `POST` | `/api/v1/auth/login/`           | ✗    | Authenticate & receive access + refresh tokens |
| `POST` | `/api/v1/auth/verify-email/`    | ✗    | Verify email with the emailed token            |
| `POST` | `/api/v1/auth/forgot-password/` | ✗    | Request a password-reset email                 |
| `POST` | `/api/v1/auth/reset-password/`  | ✗    | Reset password using the emailed token         |
| `POST` | `/api/v1/auth/logout/`          | ✔    | Invalidate current session tokens              |

### Examples

#### Register

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@shieldiq.com",
    "password": "Str0ng!Pass",
    "confirm_password": "Str0ng!Pass",
    "full_name": "Alice Johnson",
    "department": "engineering"
  }'
```

<details>
<summary>Response <code>201 Created</code></summary>

```json
{
  "success": true,
  "message": "User registered successfully. Please verify your email.",
  "data": {
    "user": {
      "id": "a1b2c3d4-...",
      "email": "alice@shieldiq.com",
      "full_name": "Alice Johnson",
      "is_email_verified": false,
      "is_active": true,
      "is_staff": true,
      "department": "engineering",
      "security_score": 0,
      "created_at": "2026-04-16T12:00:00+0000",
      "updated_at": "2026-04-16T12:00:00+0000",
      "last_login_at": null
    }
  },
  "errors": null,
  "error_code": null,
  "meta": null
}
```

</details>

#### Login

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@shieldiq.com",
    "password": "Str0ng!Pass"
  }'
```

<details>
<summary>Response <code>200 OK</code></summary>

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": { "...": "..." },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "Bearer"
    }
  },
  "errors": null,
  "error_code": null,
  "meta": null
}
```

</details>

#### Verify Email

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{ "verification_token": "<token-from-email>" }'
```

#### Forgot Password

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/forgot-password/ \
  -H "Content-Type: application/json" \
  -d '{ "email": "alice@shieldiq.com" }'
```

#### Reset Password

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/reset-password/ \
  -H "Content-Type: application/json" \
  -d '{
    "forgot_password_token": "<token-from-email>",
    "password": "NewStr0ng!Pass"
  }'
```

#### Logout (Authenticated)

```bash
curl -s -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer <access_token>"
```

---

## 📦 API Response Format

Every endpoint returns a **consistent JSON envelope** — successes, validation errors, and server errors all share the same shape:

```json
{
  "success": true,
  "message": "Human-readable status message",
  "data": {},
  "errors": null,
  "error_code": null,
  "meta": null
}
```

### Success Response

```json
{
  "success": true,
  "message": "Login successful",
  "data": { "user": { "..." }, "tokens": { "..." } },
  "errors": null,
  "error_code": null,
  "meta": null
}
```

### Validation Error

```json
{
  "success": false,
  "message": "Validation Failed.",
  "data": null,
  "errors": {
    "confirm_password": ["Passwords do not match"]
  },
  "error_code": "VALIDATION_ERROR",
  "meta": null
}
```

### Business Logic Error

```json
{
  "success": false,
  "message": "A user with this email already exists.",
  "data": null,
  "errors": null,
  "error_code": "EMAIL_ALREADY_EXISTS",
  "meta": null
}
```

### Paginated Response

```json
{
  "success": true,
  "message": "Success",
  "data": [],
  "errors": null,
  "error_code": null,
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_count": 42,
    "total_pages": 3
  }
}
```

---

## 🚨 Error Handling

All exceptions are funnelled through a **global exception handler** (`common.exceptions.exception_handler.custom_exception_handler`) registered in the DRF settings.

### Custom Exception Hierarchy

```
BaseAPIException (500)
├── BadRequestException        (400)
├── ValidationException        (400)
├── UnauthorizedException      (401)
├── ForbiddenException         (403)
├── NotFoundException          (404)
├── ConflictException          (409)
├── TooManyRequestsException   (429)
├── InternalServerErrorException (500)
└── ServiceUnavailableException  (503)
```

### Error Codes

All error codes are centralised in `common.constants.error_code.ErrorCodes`:

| Code                   | Description                           |
| ---------------------- | ------------------------------------- |
| `VALIDATION_ERROR`     | Serializer / input validation failure |
| `INVALID_CREDENTIALS`  | Wrong email or password               |
| `EMAIL_ALREADY_EXISTS` | Duplicate registration attempt        |
| `EMAIL_NOT_VERIFIED`   | Login before email verification       |
| `ACCOUNT_DEACTIVATED`  | Deactivated user attempting action    |
| `INVALID_TOKEN`        | Malformed or tampered JWT             |
| `TOKEN_EXPIRED`        | Token past its lifetime               |
| `WEAK_PASSWORD`        | Password fails strength requirements  |
| `SAME_PASSWORD`        | Reset to same password as current     |
| `NOT_FOUND`            | Resource does not exist               |
| `UNAUTHORIZED`         | Missing or invalid auth credentials   |
| `FORBIDDEN`            | Insufficient permissions              |

### Password Validation Rules

The password strength validator enforces:

- ≥ 8 characters
- ≥ 1 uppercase letter
- ≥ 1 lowercase letter
- ≥ 1 digit
- ≥ 1 special character (`!@#$%^&*(),.?":{}|<>`)

---

## 🧩 Adding a New Module

Follow this pattern to add a new domain (e.g. `campaigns`):

### 1 — Scaffold the Directory

```
apps/campaigns/
├── __init__.py
├── apps.py
├── controllers/
│   └── campaign_controller.py
├── services/
│   └── campaign_service.py
├── repositories/
│   └── campaign_repository.py
├── models/
│   ├── __init__.py
│   └── campaign_model.py
├── serializers/
│   └── campaign_serializer.py
├── urls/
│   └── campaign_urls.py
└── tests.py
```

### 2 — Register the App

```python
# config/settings.py → INSTALLED_APPS
INSTALLED_APPS = [
    ...
    "apps.campaigns.apps.CampaignsConfig",   # ← add
]
```

### 3 — Wire the URLs

```python
# config/urls.py
urlpatterns = [
    path("api/v1/", include("apps.users.urls.auth_urls")),
    path("api/v1/", include("apps.campaigns.urls.campaign_urls")),  # ← add
]
```

### 4 — Build the Layers

- **Model** → Define fields; use UUID PK, `created_at`, `updated_at`, soft-delete if needed.
- **Repository** → Extend `BaseRepository`; expose query methods only.
- **Service** → Business rules, validation, orchestration.
- **Controller** → `ViewSet` with `@action` decorators; validate via serializer, delegate to service, return `ApiResponse`.
- **Serializer** → Separate request serializers (input) from response serializers (output).

---

## 📐 Project Conventions

| Convention           | Detail                                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| **Auth model**       | `AUTH_USER_MODEL = "users.User"` — custom user with email-based auth                                   |
| **Departments**      | `DepartmentEnum`: `it_security`, `engineering`, `marketing`, `human_resources`, `finance`, `executive` |
| **Primary keys**     | UUID v4 on all models                                                                                  |
| **Soft delete**      | `is_deleted` + `deleted_at` fields on User model                                                       |
| **Timestamps**       | `created_at` (auto), `updated_at` (auto), all UTC                                                      |
| **API versioning**   | URL prefix `/api/v1/`                                                                                  |
| **Renderer**         | JSON only (`JSONRenderer`) — no browsable API                                                          |
| **Pagination**       | `PageNumberPagination`, default 20 per page                                                            |
| **Email**            | Console backend in dev; swap to SMTP in production                                                     |
| **Password hashing** | Django's default PBKDF2 via `make_password` / `check_password`                                         |
| **Token algorithm**  | HS256                                                                                                  |

---

## 📝 License

This project is licensed under the **MIT License**.
