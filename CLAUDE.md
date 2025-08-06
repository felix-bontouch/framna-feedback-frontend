# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

```bash
# Start MongoDB and Redis with Docker
./scripts/start-local.sh

# Install dependencies
pnpm install

# Start development
pnpm dev
```

## Commands

### Development
- `pnpm dev` - Run both webapp and server in development mode
- `pnpm dev:webapp` - Run only the webapp (React frontend) 
- `pnpm dev:server` - Run only the server (NestJS backend)

### Docker Services
- `./scripts/start-local.sh` - Start MongoDB and Redis containers and set up environment
- `docker-compose up -d` - Start services manually
- `docker-compose down` - Stop services (data preserved)
- `docker-compose down -v` - Stop services and remove all data
- `docker ps` - View running containers
- `docker logs framna-feedback-redis` - View Redis logs
- `docker logs framna-feedback-mongodb` - View MongoDB logs

### Utility Scripts
- `./scripts/create-test-user-simple.sh` - Create a test user
- `./scripts/mongodb-utils.sh` - MongoDB utilities
- `./scripts/debug-login.sh` - Debug login issues
- `./scripts/verify-all-users.sh` - Mark all users as email verified

### Build
- `pnpm build:webapp` - Build the webapp for production
- `pnpm build:server` - Build the server for production

### Code Quality
- `pnpm lint` - Run oxlint on all packages
- `pnpm format` - Format code with Prettier
- `pnpm type-check` - Run TypeScript type checking (available in individual packages)

### Testing
- In packages with tests (`answer-utils`, `utils`):
  - `pnpm test` - Run tests with Vitest
  - `pnpm cov` - Run tests with coverage

## Architecture

Framna Feedback is a monorepo containing multiple packages:

### Core Packages
- **webapp** - React-based frontend application using Vite, Apollo Client for GraphQL, and Tailwind CSS
- **server** - NestJS backend with GraphQL API, MongoDB database, Redis for caching, and Bull for job queues
- **form-renderer** - Standalone form rendering library used to display forms to end users
- **answer-utils** - Shared utilities for processing form submissions
- **shared-types-enums** - TypeScript types and enums shared between frontend and backend
- **utils** - Common utility functions used across packages

### Key Technologies
- **Frontend**: React 19, TypeScript, Vite, Apollo Client, Tailwind CSS, Radix UI components
- **Backend**: NestJS, GraphQL, MongoDB (Mongoose), Redis, Bull queues, JWT authentication
- **Form Rendering**: Custom React-based form renderer with support for 20+ field types
- **File Storage**: Supports local filesystem and AWS S3
- **Payments**: Stripe integration for payment collection

### Development Setup
- Node.js >= 16 required (18+ recommended for webapp)
- pnpm >= 8 required for package management
- MongoDB and Redis (provided via Docker)
- Environment variables configured in `.env` files

### Environment Configuration
1. Copy `.env.local.example` to `packages/server/.env`
2. The default configuration is pre-set for Docker services
3. MongoDB URL: `mongodb://localhost:27017/framna-feedback`
4. Redis: `localhost:6379`

### Code Organization
- GraphQL resolvers in `server/src/resolver/`
- Form field components in `form-renderer/src/blocks/`
- Frontend pages follow file-based routing in `webapp/src/pages/`
- Shared GraphQL operations in `webapp/src/services/`

## Known Issues and Fixes

### Login/Signup Not Working
If login or signup spins indefinitely:
1. Check that `packages/webapp/.env` exists with proper GraphQL configuration
2. Ensure MongoDB and Redis are running (`docker ps`)
3. Verify backend is running on port 9157
4. **Important**: Login is a GraphQL query, not mutation - AuthService must use `apollo.query()`

### Debugging Login Issues
Use the debug script: `./scripts/debug-login.sh`
Or check browser console with: `framnaDebug.enableVerbose()`

### Port Already in Use Error
If you see "Error: listen EADDRINUSE: address already in use 0.0.0.0:9157":
1. You may have VS Code debug session running alongside `pnpm dev`
2. **Important**: Don't run VS Code debug and `pnpm dev` simultaneously
3. Kill all processes: `pkill -f "nest start"`
4. Use either `pnpm dev` for normal development OR VS Code debug for debugging, not both