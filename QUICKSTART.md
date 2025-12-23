# Quick Start Guide

This guide will help you get the SME Finance App authentication system up and running quickly.

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Backend Setup (5 minutes)

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations (database is pre-configured with SQLite):
```bash
python manage.py migrate
```

5. Create a superuser (optional, for admin panel access):
```bash
python manage.py createsuperuser
```

6. Start the backend server:
```bash
python manage.py runserver
```

Backend will be running at: http://localhost:8000

## Frontend Setup (3 minutes)

1. Open a new terminal and navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend will automatically open at: http://localhost:3000

## Testing the System

### 1. Sign Up
- Go to http://localhost:3000/signup
- Create an account with email and password
- Check your terminal running the backend - you'll see the verification email in the console

### 2. Email Verification
- Copy the verification link from the backend console
- Open it in your browser to verify your email

### 3. Login
- Go to http://localhost:3000/login
- Login with your credentials
- Check "Remember me" to extend session duration

### 4. Business Setup
- After login, you'll be redirected to business setup
- Fill in your business details
- Upload a logo (optional)

### 5. Dashboard
- After business setup, you'll see the dashboard
- Note the email verification banner if you haven't verified

### 6. Settings
- Click "Settings" to update your profile, password, or business info

### 7. Password Reset
- Logout and go to forgot password
- Enter your email
- Check backend console for reset link

## Admin Panel

Access Django admin at: http://localhost:8000/admin

You can:
- View all users
- Check verification tokens
- Manage businesses
- View refresh tokens

## API Testing

You can test the API endpoints using curl or Postman:

### Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "confirm_password": "Test123!@#"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!@#",
    "remember_me": false
  }' \
  -c cookies.txt
```

### Get Profile (requires authentication)
```bash
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Common Issues

### Backend won't start
- Make sure virtual environment is activated
- Check if port 8000 is already in use
- Verify all dependencies are installed

### Frontend won't start
- Delete node_modules and package-lock.json, then run `npm install` again
- Check if port 3000 is already in use
- Clear npm cache: `npm cache clean --force`

### Can't receive emails
- In development, emails are printed to the backend console
- For production, configure SMTP settings in .env

### Database issues
- Delete db.sqlite3 and run migrations again
- Make sure you're in the backend directory when running Django commands

## Next Steps

1. Explore the API endpoints in the README.md
2. Customize the frontend styling
3. Add your business logic
4. Configure production settings
5. Set up proper email backend for production

## Support

For issues and questions, please refer to the main README.md file.

## Happy Coding! 🚀
