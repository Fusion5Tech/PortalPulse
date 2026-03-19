# PortalPulse

PortalPulse is a captive portal system designed for internet cafés, built with a modern Python backend using FastAPI. It provides a modular, secure, and extendable solution for managing user authentication, sessions, and network access.

## How It Works

The system is composed of a few key components:

- **FastAPI Backend**: A high-performance web framework for building APIs.
- **PostgreSQL**: Used for storing user credentials and logging session data.
- **Redis**: Manages active user sessions for quick access and time tracking.
- **Uvicorn/Gunicorn**: Serves the FastAPI application.

When a device connects to the network, it is redirected to a captive portal page (frontend not included in this project).

- The **admin** logs in using username/password.
- The admin generates vouchers using the API.
- The **end user** receives a voucher code from the admin and logs in using that voucher only.
- The backend validates the voucher, starts a Redis-backed timed session, and the network layer can allow internet access for that device.

## Getting Started

To get the PortalPulse backend up and running, you'll need to have Python 3.11+ and `uv` installed.

### 1. Install `uv`

`uv` is a fast Python package installer and resolver. If you don't have it, you can install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create a Virtual Environment

Create and activate a virtual environment for the project:

```bash
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install project dependencies from `pyproject.toml` using `uv`:

```bash
uv sync
```

### 4. Set Up Environment Variables

Create a `.env` file in the root of the project and add the following environment variables. Adjust the values to match your local setup.

```env
DATABASE_URL="postgresql://user:password@localhost/portal_pulse"
REDIS_URL="redis://localhost:6379"
SECRET_KEY="a_very_secret_key"
```

### 5. Run the Application

You can now start the FastAPI development server using `uv`:

```bash
uv run fastapi dev main.py
```

The application will be available at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

## Voucher Workflow

1. Admin login:

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin_password"}'
```

1. Create vouchers (admin token required):

```bash
curl -X POST http://127.0.0.1:8000/admin/vouchers \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"count":5,"duration_minutes":60}'
```

1. Get printable vouchers:

```bash
curl "http://127.0.0.1:8000/admin/vouchers/print?only_unprinted=true" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

1. User voucher login (no username/password):

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"voucher_code":"ABC1234567","ip_address":"192.168.1.20","mac_address":"AA:BB:CC:DD:EE:FF","device_name":"Phone"}'
```
