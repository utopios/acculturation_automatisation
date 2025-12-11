# Application Telco Provisioning - Demo CI/CD
FROM python:3.11-slim

LABEL maintainer="Formation Telco"
LABEL description="API de provisionnement Telco pour démo CI/CD"

WORKDIR /app

# Dépendances
RUN pip install --no-cache-dir flask flask-cors requests

# Code application
COPY app.py .
COPY templates/ templates/

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "app.py"]
