FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app", "--workers", "3", "--log-level", "info", "--capture-output", "--log-file", "-"]
