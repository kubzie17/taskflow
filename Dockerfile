# 1. Start from an official, slim Python 3.12 image (the empty travel case)
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Work in /app inside the container
WORKDIR /app

# 4. copy only the kit list and install it
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 5. copy only the application code
COPY app ./app

# 6. create a normal user and a data folder it owns
RUN useradd --create-home --uid 10001 taskflow \
 && mkdir -p /data \
 && chown taskflow /data
USER taskflow

# 7. Keep the record in /data
ENV TASKFLOW_DB=/data/taskflow.db

# 8. Document the port and start the server
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]