# SME Finance App - Authentication & Accounts System

A complete authentication and accounts system for SME finance management with JWT-based auth, email verification, business onboarding, and session management.

## Tech Stack

### Backend
- Python (Django 4.2.7)
- Django REST Framework 3.14.0
- PostgreSQL
- JWT Authentication (djangorestframework-simplejwt)
- Django CORS Headers
- Django Rate Limit

### Frontend
- React 18
- React Router DOM
- Axios
- JWT Decode

## Features

### Authentication
- ✅ User signup with email and password
- ✅ Email verification with token-based links
- ✅ Login with email and password
- ✅ JWT access tokens (15-minute expiry, stored in memory)
- ✅ Refresh tokens (7-14 days, stored in httpOnly cookies)
- ✅ Auto-refresh logic for access tokens
- ✅ Password reset via email
- ✅ Remember me functionality
- ✅ Session management with 30-minute inactivity timeout
- ✅ Rate limiting on auth endpoints

### Business Onboarding
- ✅ Business profile setup (name, currency, logo)
- ✅ One business per user enforcement
- ✅ Multi-currency support (USD, GBP, EUR, NGN, KES, ZAR, GHS)
- ✅ Optional business logo upload with validation

### Account Management
- ✅ Profile updates (username, email)
- ✅ Password change with current password verification
- ✅ Business information updates
- ✅ Email verification banner
- ✅ Resend verification email

### Security
- ✅ Password complexity validation (min 8 chars, uppercase, number, special char)
- ✅ Rate limiting to prevent brute force attacks
- ✅ httpOnly cookies for refresh tokens
- ✅ CORS configuration
- ✅ Secure file upload validation
- ✅ Single-use email verification tokens
- ✅ Password reset invalidates all active sessions

### Frontend Features
- ✅ Protected routes with authentication guards
- ✅ Business setup requirement enforcement
- ✅ Auto token refresh before expiry
- ✅ Centralized error handling
- ✅ Password strength indicator
- ✅ Loading states and error messages
- ✅ Responsive design

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Set up PostgreSQL database:
```bash
# Create database
createdb sme_finance_db

# Or using psql
psql -U postgres
CREATE DATABASE sme_finance_db;
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/api`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
# .env file should already exist with:
REACT_APP_API_URL=http://localhost:8000/api
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/signup/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh access token
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/verify-email/` - Verify email with token
- `POST /api/auth/resend-verification-email/` - Resend verification email
- `POST /api/auth/password-reset-request/` - Request password reset
- `POST /api/auth/password-reset/` - Reset password with token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/profile/` - Update user profile
- `PUT /api/auth/change-password/` - Change password

### Business Endpoints

- `POST /api/business/setup/` - Create business profile
- `GET /api/business/me/` - Get current user's business
- `PUT /api/business/update/` - Update business information

## Environment Variables

### Backend (.env)

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=sme_finance_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

FRONTEND_URL=http://localhost:3000

JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME_REMEMBER=14
JWT_REFRESH_TOKEN_LIFETIME_DEFAULT=7

INACTIVITY_TIMEOUT=30
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:8000/api
```

## Project Structure

```
.
├── backend/
│   ├── accounts/              # User authentication app
│   │   ├── models.py         # User, EmailVerificationToken, etc.
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # Auth endpoints
│   │   ├── urls.py           # URL routing
│   │   ├── validators.py     # Password validation
│   │   ├── utils.py          # Email utilities
│   │   ├── middleware.py     # Inactivity middleware
│   │   ├── exceptions.py     # Custom exception handler
│   │   └── admin.py          # Django admin config
│   ├── business/             # Business management app
│   │   ├── models.py         # Business model
│   │   ├── serializers.py    # Business serializers
│   │   ├── views.py          # Business endpoints
│   │   └── admin.py          # Django admin config
│   ├── config/               # Django project settings
│   │   ├── settings.py       # Main settings
│   │   ├── urls.py           # Root URL config
│   │   └── wsgi.py
│   ├── templates/            # Email templates
│   │   └── emails/
│   │       ├── verification_email.html
│   │       └── password_reset_email.html
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/       # Reusable components
    │   │   ├── ProtectedRoute.js
    │   │   └── EmailVerificationBanner.js
    │   ├── contexts/         # React contexts
    │   │   └── AuthContext.js
    │   ├── pages/            # Page components
    │   │   ├── Login.js
    │   │   ├── Signup.js
    │   │   ├── VerifyEmail.js
    │   │   ├── ForgotPassword.js
    │   │   ├── ResetPassword.js
    │   │   ├── BusinessSetup.js
    │   │   ├── Dashboard.js
    │   │   └── Settings.js
    │   ├── services/         # API services
    │   │   ├── api.js
    │   │   ├── authService.js
    │   │   └── businessService.js
    │   ├── utils/            # Utility functions
    │   │   └── passwordValidation.js
    │   ├── App.js
    │   └── index.js
    ├── package.json
    └── .env

## Testing

### Backend Tests (Coming Soon)
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment Considerations

### Backend
- Set `DEBUG=False` in production
- Use environment-specific secret keys
- Configure production database (PostgreSQL)
- Set up proper email backend (SMTP)
- Use a web server (Gunicorn + Nginx)
- Enable HTTPS for secure cookies
- Configure proper CORS origins
- Set up media file storage (S3, etc.)

### Frontend
- Build for production: `npm run build`
- Deploy to static hosting (Netlify, Vercel, etc.)
- Update `REACT_APP_API_URL` to production API
- Enable HTTPS

## Security Best Practices

1. Never commit `.env` files
2. Use strong secret keys in production
3. Enable HTTPS in production
4. Set `secure=True` for cookies in production
5. Regularly update dependencies
6. Monitor rate limiting logs
7. Implement logging for security events
8. Regular security audits

## License

MIT

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
