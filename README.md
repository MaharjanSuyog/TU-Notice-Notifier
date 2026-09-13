# TU Notice Notifier

**Live App:** https://tunotice.vercel.app

TU Notice Notifier tracks new notices from `https://iost.tu.edu.np/notices`, stores them in PostgreSQL, classifies them with tags, and sends email notifications to subscribed users.

## Major Concepts

1. **Scraping Pipeline**
   - Scheduler runs every 5 minutes.
   - Scraper fetches notices, avoids duplicates using Redis + PostgreSQL checks.
   - New notices are saved and tagged automatically.

2. **Notice Classification**
   - Titles are classified into tags (program, semester, category, modifier).
   - Example tags: `bsc_csit`, `bit`, `exam`, `result`, `1st_sem` ... `8th_sem`.

3. **Authentication**
   - Google OAuth login flow.
   - Session + CSRF tokens are stored in Redis and sent as cookies.

4. **Delivery**
   - HTML emails are sent through SMTP (Gmail app password based config).
   - Unsubscribe link is included in every email.

5. **Frontend API Proxy**
   - Next.js rewrites `/api/*` to backend using `BACKEND_URL`.

## Tech Stack

- **Frontend:** Next.js 16, React 19, TypeScript
- **Backend:** FastAPI, SQLAlchemy, APScheduler
- **Database:** PostgreSQL
- **Cache/Session:** Redis
- **Email:** SMTP (aiosmtplib)
- **Containerization:** Docker Compose

## Database Structure

### Tables

| Table | Purpose | Key columns |
|---|---|---|
| `notices` | Stores scraped TU notices | `id (uuid)`, `notice_id (unique int)`, `title`, `href (unique)`, `published_date` |
| `tags` | Master tag catalog | `id`, `name (unique)`, `kind (program/semester/category/modifier)` |
| `notice_tags` | Many-to-many map: notices ↔ tags | `notice_id`, `tag_id` |
| `subscribers` | User subscription/auth state | `id (uuid)`, `email`, `google_id`, `status`, `unsubscribe_token`, `is_admin`, `program_tag_id`, `semester_tag_id` |
| `subscriber_category_tags` | Many-to-many map: subscribers ↔ category tags | `subscriber_id`, `tag_id` |

### Relationships

- `notices` ↔ `tags` via `notice_tags` (many-to-many)
- `subscribers` → `tags` via:
  - `program_tag_id` (one program tag)
  - `semester_tag_id` (one semester tag)
  - `subscriber_category_tags` (multiple category tags)

> `gen_random_uuid()` is used in PostgreSQL defaults, so ensure `pgcrypto` extension is enabled in your database.

## Environment Schema

Create `.env` in project root from `.env.example`:

```bash
cp .env.example .env
# Windows (PowerShell)
Copy-Item .env.example .env
```

Required keys are documented in `.env.example` for:
- PostgreSQL connection
- Redis connection
- Google OAuth
- SMTP/email sender
- Frontend/backend URLs
- Runtime environment mode

## Run with Docker

### Quick commands

```bash
# Development (compose.yaml)
docker compose up --build
docker compose down

# Production (compose.prod.yaml + .env.prod)
docker compose --env-file .env.prod -f compose.prod.yaml up --build -d
docker compose --env-file .env.prod -f compose.prod.yaml down
```

### Development (current `compose.yaml`)

### 1) Build and start

```bash
docker compose up --build
```

### 2) Services

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

### 3) Stop

```bash
docker compose down
```

### Production (`compose.prod.yaml`)

Use your production env file (example: `.env.prod`) and run:

```bash
docker compose --env-file .env.prod -f compose.prod.yaml up --build -d
```

Make sure `.env.prod` contains a valid `BACKEND_URL` (it is required during frontend image build and runtime).

Stop production stack:

```bash
docker compose --env-file .env.prod -f compose.prod.yaml down
```

Production frontend container runs `npm run build` during image build and `npm start` at runtime.

## Run Without Docker (Separate Backend + Frontend)

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Next.js)

```bash
cd frontend
npm ci
npm run dev
```

Ensure `BACKEND_URL=http://localhost:8000` in `.env` so frontend rewrite proxy works correctly.

## Main API Endpoints

- `GET /` → backend health message
- `GET /notices` → paginated notices (`page`, `page_size`, `tag`, `tags`)
- `GET /notices/tags` → used tags list
- `GET /auth/google/login` → start Google OAuth
- `GET /auth/google/callback` → OAuth callback
- `GET /auth/me` → current session user
- `POST /auth/logout` → logout

## Project Structure

```text
.
├─ backend/
│  ├─ main.py
│  ├─ models.py
│  ├─ scraper.py
│  ├─ scheduler.py
│  ├─ routers/
│  └─ utils/
├─ frontend/
│  ├─ app/
│  ├─ components/
│  ├─ hooks/
│  └─ utils/
└─ compose.yaml
```
