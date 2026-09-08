# UP_AI Frontend

Production-oriented frontend foundation for the UP_AI citizen governance platform.

## Run

```bash
cd ~/Desktop/RAGHU
npm install
cp .env.example .env
npm run dev
```

Build:

```bash
npm run build
```

## Backend integration

Set:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Replace the demo/mock calls in `src/data/mock.ts` and page submit handlers with FastAPI/OpenAPI services.

Recommended API structure:

```text
src/services/api/
├── client.ts
├── auth.ts
├── complaints.ts
├── officers.ts
├── departments.ts
├── districts.ts
├── analytics.ts
└── ai.ts
```

The UI is intentionally separated into public, citizen/dashboard, directory, complaint, analytics and AI surfaces so the backend can be connected without redesigning the frontend.

## Important

- Demo data is local only.
- Login currently creates a demo token.
- Complaint submission currently shows a demo success state.
- AI currently returns a demo response.
- Map is a GIS placeholder.
- Replace those demo handlers with real FastAPI/OpenAPI generated clients.
