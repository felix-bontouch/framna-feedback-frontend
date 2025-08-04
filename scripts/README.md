# Framna Feedback Scripts

This directory contains utility scripts for local development and maintenance.

## Available Scripts

### Setup & Infrastructure

- **`start-local.sh`** - Start MongoDB and Redis using Docker Compose
  ```bash
  ./scripts/start-local.sh
  ```

### User Management

- **`create-test-user-simple.sh`** - Create a test user for development
  ```bash
  ./scripts/create-test-user-simple.sh
  # Creates user: test@example.com / Test123!
  ```

- **`verify-all-users.sh`** - Mark all users as email verified
  ```bash
  ./scripts/verify-all-users.sh
  ```

### Debugging

- **`debug-login.sh`** - Test and debug login functionality
  ```bash
  ./scripts/debug-login.sh
  ```

- **`mongodb-utils.sh`** - MongoDB utility commands
  ```bash
  ./scripts/mongodb-utils.sh [command]
  
  # Commands:
  # shell       - Open MongoDB shell
  # collections - List all collections
  # users       - Count users
  # forms       - List all forms
  # stats       - Show database statistics
  ```

## Prerequisites

- Docker and Docker Compose installed
- MongoDB and Redis containers running (via `start-local.sh`)
- Backend server running on port 9157

## Notes

All scripts are executable and can be run directly from the project root:
```bash
./scripts/script-name.sh
```