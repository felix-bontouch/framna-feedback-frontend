<div align="center">
  <h1 align="center">
    Framna Feedback
  </h1>
  <p>Framna Feedback is a form builder forked from the open-source projet [Heyform](https://github.com/heyform/heyform) that allows anyone to create engaging conversational forms for surveys, questionnaires, quizzes, and polls. No coding skills required.</p>
</div>

<img src="./assets/images/screenshot.png" alt="Framna Feedback" />

## Features

Framna Feedback simplifies the creation of conversational forms within mobile applications, making it accessible for anyone to gather information or feedback through simple surveys, quizzes, and polls. 

### Build Forms with Ease

- 📝 **Versatile Inputs**: From basic text, email, and phone number fields to advanced options like picture choices, date pickers, and file uploads, Framna Feedback supports a wide array of input types.
- 🧠 **Smart Logic**: Conditional logic and URL redirections for dynamic, adaptable forms.
- 🔗 **Powerful Integrations**: Connect with webhooks, analytics, marketing platforms, and tools like Zapier and Make.com.

### Customize to Your Brand

- 🎨 **Visual Themes**: Tailor the look and feel of your forms to match your brand identity with customizable fonts, colors, backgrounds, and more.
- ✨ **Advanced Theming**: Gain greater control with extensive customization options, including custom CSS for deeper personalization.

### Analyze and Act on Data

- 📊 **Insightful Analytics**: Gain insights with detailed analytics, including drop-off rates and completion rates.
- 📤 **Data Export**: Easily export your form results to CSV for further analysis or integration into your systems.

## Getting Started with Framna Feedback

### Quick Start with Docker

The fastest way to get started locally is using our Docker setup:

```bash
# Clone the repository
git clone https://github.com/your-username/framna-feedback.git
cd framna-feedback/frontend

# Install dependencies
pnpm install

# Start MongoDB and Redis using Docker
./scripts/start-local.sh

# Start the development server
pnpm dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:9157

### Test User for Development

To bypass Google login for testing:
```bash
./scripts/create-test-user-simple.sh
```

Login with:
- Email: test@example.com
- Password: Test123!

See [docs/TEST_USER.md](docs/TEST_USER.md) for more details.

## Structure

```
.
└── packages
    ├── answer-utils       (form submission utils for server and webapp)
    ├── embed              (form embed javascript library)
    ├── form-renderer      (form rendering library)
    ├── shared-types-enums (shared types/enums for server and webapp)
    ├── utils              (common utils for server and webapp)
    ├── server             (node server)
    └── webapp             (react webapp)
```

## Prerequisites

- Node.js >= 16 (18+ recommended for webapp)
- pnpm >= 8
- Docker and Docker Compose (for MongoDB and Redis)

## Local Development

### Environment Setup

1. **Copy the environment template:**
   ```bash
   cp .env.local.example packages/server/.env
   ```

2. **Update the `.env` file with your configuration:**
   - Database connections are pre-configured for Docker
   - Add SMTP settings for email functionality
   - Configure any third-party services (Stripe, OAuth, etc.)

### Docker Services

The project includes a Docker Compose configuration for local development:

```yaml
services:
  - MongoDB (port 27017)
  - Redis (port 6379)
```

Manage services with:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Remove all data
docker-compose down -v
```

### Available Commands

```bash
# Development
pnpm dev          # Run both frontend and backend
pnpm dev:webapp   # Run frontend only
pnpm dev:server   # Run backend only

# Building
pnpm build:webapp # Build frontend for production
pnpm build:server # Build backend for production

# Code Quality
pnpm lint         # Run linter
pnpm format       # Format code
pnpm type-check   # Run TypeScript checks

# Testing (in packages with tests)
pnpm test         # Run tests
pnpm cov          # Run tests with coverage
```

## How to Contribute

You are awesome, let's build great software together. We welcome contributions to Framna Feedback!

## Support & Community

If you have questions or need help:

- Create an issue in this repository
- Check existing issues for solutions

## License

Framna Feedback is built on Heyform which is open-source under the GNU Affero General Public License v3.0 (AGPL-3.0).
