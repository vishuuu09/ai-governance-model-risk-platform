# AI Governance & Model Risk Management Platform

Learning project: AI model inventory, risk assessments, approval decisions and audit records.

## Stack
- React + TypeScript + Vite
- Python + FastAPI + SQLAlchemy
- PostgreSQL
- JWT authentication and Argon2 password hashing

## Run on Windows
1. Install Python 3.12+, Docker Desktop, Node.js LTS and Git.
2. From the repository root: `docker compose up -d postgres`
3. Copy `backend/.env.example` to `backend/.env`; replace JWT_SECRET_KEY with a long random secret.
4. Backend:
   `cd backend`
   `python -m venv .venv`
   ` .\.venv\Scripts\Activate.ps1`
   `pip install -r requirements.txt`
   `uvicorn app.main:app --reload`
5. Frontend in another terminal:
   `cd frontend`
   `npm install`
   `npm run dev`
6. Open http://localhost:5173 and API docs at http://127.0.0.1:8000/docs.

Register an account via POST /api/v1/auth/register in Swagger, then sign in from the frontend.

## Notes
Registration assigns analyst role only. Reviewer/admin provisioning must be done securely by an administrator; do not expose role selection publicly. The risk formula is illustrative (impact × likelihood), not a validated regulatory model. Audit rows are application-level records, not tamper-proof. This starter is not production-ready; add migrations, comprehensive tests, rate limiting, secure secrets, hardened authorization and audit integrity before deployment.
