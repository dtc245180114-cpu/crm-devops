FROM python:3.12-slim

RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh appuser

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY app.py /app/app.py

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
