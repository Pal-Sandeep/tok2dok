Here’s your fully **merged and updated `README.md`**, combining your latest info with all previous FastAPI/Firebase/SQLite setup and dev commands. It's structured cleanly for clarity, dev usability, and future growth.

---

```markdown
# 🧠 Talk to PDF (FastAPI + React)

Let your users chat with their PDFs using AI — supports chunked vector search, authentication, usage limits, and Stripe billing.

---

## 🔥 Features

- Upload PDF, split & embed using OpenAI
- Chat with your documents using RAG
- JWT Auth (via Firebase)
- Usage limits (per day, per plan)
- Stripe subscription billing
- Postgres + pgvector support (SQLite for local dev)
- Modular & production-ready FastAPI backend

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL (SQLite for dev), Alembic
- **Frontend**: React + Tailwind (to be built)
- **Auth**: Firebase JWT Auth
- **Payments**: Stripe
- **Vector Store**: PostgreSQL with `pgvector`
- **Others**: Pydantic, python-multipart, firebase-admin

---

## 🗂️ Project Structure

```
talk-to-pdf/
├── app/
│   ├── api/              # All API routers
│   ├── core/             # Settings, config
│   ├── db/               # Models & DB utils
│   ├── services/         # Core logic (e.g., chunking)
│   ├── schemas/          # Pydantic schemas
│   └── main.py           # FastAPI entrypoint
├── alembic/              # DB migration scripts
├── .env
├── README.md
└── requirements.txt
```

---

## 🧪 Quick Start

```bash
git clone https://github.com/pal-sandeep/talk-to-pdf.git
cd talk-to-pdf

python -m venv env
source env/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

# Set up your database and env vars
cp .env.example .env

# Run server
uvicorn app.main:app --reload
```

---

## ⚙️ Local Development (SQLite)

### Alembic Setup

```bash
# First-time setup (if not already done)
alembic init alembic
# Ensure `env.py` has correct target_metadata import
# target_metadata = Base.metadata

# Generate and apply migrations
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

---

## 🔐 Firebase Auth

- Firebase handles user signup/login.
- Client sends Firebase ID token in `Authorization: Bearer <token>`.
- FastAPI validates using `firebase_admin`.

---

## 📦 Usage Tracking

- Track user access per plan (free or paid).
- Use `UsageTracker` model to enforce:
  - Free users: e.g., 1 chat/session
  - Paid users: Unlimited or tiered

---

## 🛡️ Rate Limiting (Optional)

- Enforce API limits based on Firebase UID or IP.
- Store daily usage counts in DB (custom or Redis).
- Deny access or return upgrade message on exceeding limit.

---

## 🧠 Roadmap

- [x] PDF Upload + Chunking
- [x] Firebase Login/Signup APIs
- [x] Free Trial Limit + Plan Enforcement
- [x] Alembic + SQLite for local dev
- [ ] Stripe Billing Integration
- [ ] Postgres + pgvector setup
- [ ] Frontend with React + Tailwind

---

## 🧠 Dev Commands

```bash
# Run backend
uvicorn app.main:app --reload

# Create DB migrations
alembic revision --autogenerate -m "..."

# Apply migrations
alembic upgrade head
```

---

## 🧠 Author

Built by **Sandeep Pal**  
📍 Made in Rajasthan, India  
🔗 https://github.com/pal-sandeep

---

## 🪪 License

MIT — free to use, modify, or build on.
```

---

```bash
# Run FastAPI
uvicorn app.main:app --reload

# Run Alembic Migrations
alembic revision --autogenerate -m "..."
alembic upgrade head

# Install new deps
pip install firebase-admin
pip install sqlalchemy alembic pydantic fastapi
```

alembic init alembic  # if not done already
# Edit alembic/env.py: set target_metadata from your Base

# Create & Apply migrations
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
