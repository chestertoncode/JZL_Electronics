# JZL Electronics — CPE Elective 2 Full-Stack Project

A beginner-friendly electronics catalog and inventory/order system built with Vue 3 + TypeScript + Tailwind CSS and Django REST Framework.

## Features
- Register and login using JWT authentication
- Product catalog and product search
- Add, edit, and delete products (staff/admin only)
- Upload product images
- Place orders and view order history
- Inventory records
- Django admin for managing users and data
- SQLite for easy local testing; PostgreSQL-ready configuration
- API validation and protected endpoints

## Project folders
- `frontend/` — Vue 3, TypeScript, Tailwind CSS, Vue Router, Pinia, Axios
- `backend/` — Django REST Framework API, JWT authentication, product image uploads

## Requirements
- Node.js 22.18+ (or a compatible current LTS)
- Python 3.11+
- WebStorm can open the `frontend` folder. Use a terminal in the backend folder for Django.

## Run the backend (Windows PowerShell)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations store
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
If `py` is not recognized, install Python from python.org and enable the option to add Python to PATH.

Backend runs at `http://127.0.0.1:8000/`
Admin page: `http://127.0.0.1:8000/admin/`
API root: `http://127.0.0.1:8000/api/`

## Run the frontend (open a second terminal)
```powershell
cd frontend
npm install
npm run dev
```
Open the local URL Vite prints, usually `http://localhost:5173/`.

## Important setup notes
1. The frontend's API base URL is in `frontend/src/services/api.ts`.
2. The starter is configured for local development. Before public deployment, set a strong Django `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`, configure CORS for your deployed frontend, and use PostgreSQL.
3. Registering a user creates a normal customer account. To manage products, log in with the Django superuser account or grant a user staff access in Django admin.
4. Product image uploads are stored in `backend/media/` during local development.
5. This is a classroom starter. Test workflows and review security settings before production deployment.
