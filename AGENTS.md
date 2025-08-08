# Repository Guidelines

## Project Structure & Modules
- Monorepo managed by PNPM workspaces. Primary packages live in `packages/`:
  - `packages/webapp` (Vite + React + TS): `src/` contains `components/`, `pages/`, `services/`, `store/`, `utils/`.
  - `packages/server` (NestJS + TS): `src/` with `controller/`, `resolver/`, `service/`, `model/`, `config/`, `utils/`; runtime entry is `src/main.ts`.
- Shared libs: `packages/{utils,answer-utils,form-renderer,shared-types-enums}`.
- Root tooling/config: `.prettierrc`, `.oxlintrc.json`, `pnpm-workspace.yaml`, `Dockerfile`, `docker-compose.yml`.

## Build, Test, and Development
- Install: `pnpm install` (Node ≥ 18 recommended; root enforces pnpm ≥ 8).
- Run both apps: `pnpm dev` (spawns webapp and server).
- Webapp only: `pnpm --filter ./packages/webapp dev`.
- Server only: `pnpm --filter ./packages/server dev`.
- Build: `pnpm build:webapp`, `pnpm build:server`.
- Type check: `pnpm --filter ./packages/webapp type-check`, `pnpm --filter ./packages/server type-check`.

## Coding Style & Naming
- Formatting: Prettier (2‑space indent); run `pnpm format`.
- Linting: Oxlint at root (`pnpm lint`); server additionally uses ESLint.
- Import order: `@trivago/prettier-plugin-sort-imports` and Tailwind plugin are enabled.
- React: components `PascalCase` (e.g., `UserCard.tsx`), hooks `useX.ts`, constants `SCREAMING_SNAKE_CASE` in `consts/`.
- Server: DTOs/interfaces `PascalCase`, providers/services end with `Service`, resolvers/controllers end with `Resolver`/`Controller`.

## Testing Guidelines
- Current setup is minimal. Server tests live under `packages/server/test/` (Nest/Jest style). Prefer unit tests for services/resolvers. For the webapp, colocate tests next to files as `*.test.ts(x)` when adding coverage.
- Aim for meaningful coverage on business logic; avoid brittle DOM snapshots.

## Commit & Pull Requests
- Prefer Conventional Commits (e.g., `feat: ...`, `fix: ...`, `refactor: ...`). Keep subjects ≤ 72 chars; include scope when helpful.
- PRs should include: clear description, linked issues, screenshots/recordings for UI, and instructions to reproduce. Keep diffs focused; update docs when behavior changes.

## Security & Configuration
- Use `.env.example` as a template; never commit secrets. Server reads env from `packages/server/.env`; webapp from `packages/webapp/.env`.
- For Docker, see root `Dockerfile` and `docker-compose.yml`. Ensure ports and CORS match local dev settings.
