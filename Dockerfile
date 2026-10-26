FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py ./app.py
COPY tests/ ./tests/
COPY pytest.ini .

CMD ["python", "-m", "pytest", "-v"]