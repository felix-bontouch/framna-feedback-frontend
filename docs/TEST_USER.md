# Test User for Development

For local development and testing, you can create a test user to bypass social login requirements.

## Quick Setup

1. Make sure MongoDB is running:
   ```bash
   ./scripts/start-local.sh
   ```

2. Create the test user:
   ```bash
   ./scripts/create-test-user-simple.sh
   ```

## Login Credentials

- **Email**: test@example.com
- **Password**: Test123!
- **Login URL**: http://localhost:3000/login

## Features

The test user is created with:
- Verified email status
- Default avatar
- English language preference
- No deletion scheduled

## Alternative Methods

### Manual creation via Sign-up:
1. Navigate to http://localhost:3000/sign-up
2. Create an account with your preferred email/password
3. The account will be ready to use immediately

## Troubleshooting

If the test user already exists, you'll see a message indicating the user ID. You can:
1. Use the existing credentials to login
2. Delete the user from MongoDB and recreate:
   ```bash
   docker exec -it framna-feedback-mongodb mongosh framna-feedback
   db.users.deleteOne({ email: "test@example.com" })
   exit
   ```

## Security Note

This test user is intended for development only. Never use these credentials in production environments.