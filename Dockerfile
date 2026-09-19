FROM python:3.12-slim

WORKDIR /app



COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations, seed the database, and start the application
CMD alembic upgrade head && python backend/seed.py && uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
