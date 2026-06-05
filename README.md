# Shop Manager

Vehicle inspection and shop management system. Dark-mode, functional, local-first with free hosting on Railway.

## Features

- **Customers & Vehicles** — CRM with vehicle registry
- **Inspections** — Multi-category checklist (brakes, tires, fluids, suspension, etc.) with condition, urgency, estimated cost
- **Repairs** — Link inspection items to jobs, track parts/labor, status (pending → in_progress → done/deferred)
- **Jobs Board** — Kanban-style: Quoted → Active → Completed → Paid/Unpaid
- **Payments** — Multiple payments per job, auto-calculates balance
- **Tax Export** — One-click Excel export with labor/parts breakdown, paid/unpaid totals

## Quick Start (Local)

```bash
cd shop_manager
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

Open http://localhost:8000

## Deploy to Railway (Free)

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo
4. Railway auto-detects FastAPI, uses `python -m app.main` as start command
5. Add a **SQLite** or **PostgreSQL** volume (Railway provides both free)
6. Set `DATABASE_URL` if using Postgres (Railway injects it automatically)
7. Deploy — you get a `https://your-app.railway.app` URL

### Railway Config (optional)

`railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS" },
  "deploy": { "startCommand": "python -m app.main", "healthcheckPath": "/" }
}
```

## Data Model

- **Customer** → **Vehicles** → **Inspections** → **Inspection Items** → **Repairs** → **Jobs** → **Payments**
- Jobs have statuses: `quoted`, `active`, `completed`, `paid`, `unpaid`
- Repairs have statuses: `pending`, `in_progress`, `done`, `deferred` (for 6-month items)

## Tax Export Columns

Date, Customer, Vehicle, Job Title, Status, Quoted Total, Actual Total, Tax Amount, Labor Total, Parts Total, Paid, Balance

## Stack

- **FastAPI** — Python web framework
- **SQLAlchemy 2.0** — ORM with SQLite/Postgres
- **Jinja2** — Server-rendered templates
- **htmx + Alpine.js** — Reactive UI without SPA complexity
- **openpyxl** — Excel export

## Project Structure

```
shop_manager/
├── app/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLAlchemy setup
│   ├── models/__init__.py   # ORM models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/main.py       # All routes
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── customers.html
│   │   ├── vehicles.html
│   │   ├── inspection_form.html
│   │   ├── inspections.html
│   │   ├── jobs.html
│   │   └── vehicle_jobs.html
│   └── static/css/style.css # Dark theme
├── data/                    # SQLite database (auto-created)
├── requirements.txt
└── pyproject.toml
```

## Customization

- **Inspection categories**: Edit `categories` list in `routes/main.py` → `new_inspection_form`
- **Job statuses**: Modify `JobStatus` enum in `models/__init__.py`
- **UI colors**: Tweak CSS variables in `static/css/style.css`

## License

MIT — use it, break it, fix it.
