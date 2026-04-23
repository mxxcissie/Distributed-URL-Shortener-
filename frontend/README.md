# Frontend

This frontend is a Vite + React client for the URL shortener project.

## Features

- Create short URLs through the FastAPI backend
- Look up click statistics for an existing short code
- Surface backend error details in the UI when available

## Local Development

```bash
npm install
export VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

The app runs at `http://localhost:5173` by default.

## Scripts

- `npm run dev` — start the local development server
- `npm run build` — build the production bundle
- `npm run lint` — run ESLint
- `npm run test:run` — run the Vitest suite once
- `npm test` — run Vitest in watch mode

## Testing

Frontend tests use Vitest, jsdom, and React Testing Library.

Run them with:

```bash
npm run test:run
```
