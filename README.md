# Communities Backend Template

A FastAPI starter template configured with environment-based database settings and JWT authentication flows for sign up, login, and logout.

## Features

- FastAPI application bootstrap with SQLAlchemy models and session management.
- Environment-aware configuration that switches database URLs based on `APP_ENV`.
- JWT-based authentication routes for user sign up, login, and logout.
- Password hashing using `passlib` and secure token creation with `python-jose`.
- Example `.env` file to document required environment variables.

## Getting Started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**

   Copy `.env.example` to `.env` and adjust the values for your environment.

   ```bash
   cp .env.example .env
   ```

3. **Run the API**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **API Endpoints**

   - `POST /auth/signup`: Register a new user.
   - `POST /auth/login`: Authenticate and receive a JWT access token. The token is also echoed in the `Authorization` response header.
   - `POST /auth/logout`: Placeholder endpoint that returns `204` to allow the client to clear stored tokens.

## Testing the Auth Flow

1. **Sign Up**

   ```bash
   http POST :8000/auth/signup email=user@example.com password=secret
   ```

2. **Login**

   ```bash
   http -f POST :8000/auth/login username=user@example.com password=secret
   ```

   The response includes an `access_token`. Store it client-side.

3. **Authenticated Request**

   ```bash
   http GET :8000/ "Authorization:Bearer <access_token>"
   ```

4. **Logout**

   ```bash
   http POST :8000/auth/logout "Authorization:Bearer <access_token>"
   ```

   The backend returns `204`, signaling the client to remove the token.

## Database

The template uses SQLAlchemy with a simple `User` model. Adjust `app/models.py` and database migrations as needed for your project.

## Environment Variables

All environment variables are documented in `.env.example`. The application reads them from the `.env` file by default.
