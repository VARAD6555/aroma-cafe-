# Aroma Cafe — Flask + SQLite Backend

This project turns the supplied Aroma Cafe table-ordering frontend into a Flask application with a SQLite database.

## What is connected

- Menu is loaded from SQLite through `GET /api/menu`.
- Quick Add and custom add-ons continue to work in the existing frontend.
- Checkout sends the cart to `POST /api/orders`.
- The server recalculates prices and the 5% tax instead of trusting browser totals.
- "Call Waiter" saves a waiter request.
- "Request Bill" saves a bill request.
- Feedback saves a 1–5 star rating and message.
- Order status is available at `GET /api/orders/<order_id>`.
- Basic registration/login routes are included under `/auth`.

## Project structure

```text
aroma-cafe-backend/
├── wsgi.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── forms.py
│   ├── cli.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── main/
│   │       └── index.html
│   └── static/
│       ├── css/style.css
│       └── js/backend.js
├── database/
│   └── schema.sql
├── scripts/
│   └── seed_db.py
├── instance/
└── tests/
```

## Run on Windows

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2. Install packages

```powershell
pip install -r requirements.txt
```

### 3. Create `.env`

```powershell
copy .env.example .env
```

Change `SECRET_KEY` in `.env`.

### 4. Create and seed the database

```powershell
python scripts/seed_db.py
```

This creates `instance/aroma_cafe.db`.

### 5. Start the website

```powershell
flask --app wsgi.py run --debug
```

Open:

```text
http://127.0.0.1:5000/?table=04
```

Change the table number with:

```text
http://127.0.0.1:5000/?table=01
http://127.0.0.1:5000/?table=02
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Server health |
| GET | `/api/menu` | Menu + add-ons |
| POST | `/api/orders` | Create table order |
| GET | `/api/orders/<id>` | Check order status |
| POST | `/api/waiter-requests` | Call waiter |
| POST | `/api/bill-requests` | Request bill |
| POST | `/api/feedback` | Save feedback |

## Important GitHub rule

Do **not** commit `.env` or `instance/aroma_cafe.db`. They are ignored by `.gitignore`.

Commit `database/schema.sql` and `scripts/seed_db.py` so another computer can recreate the database.

## Production

For deployment, set a strong `SECRET_KEY` and a production database URL. Run with Gunicorn, for example:

```bash
gunicorn wsgi:app
```

SQLite is excellent for a college project/small prototype. For a busy production cafe, use PostgreSQL or another server database.
