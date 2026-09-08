# Deployment Architecture

Version: 2.0

Status: Draft

---

# Development

FastAPI

SQLite

Local Development

---

# Testing

Separate Testing Database

---

# Staging

PostgreSQL

Docker

---

# Production

FastAPI

Gunicorn/Uvicorn

PostgreSQL

Nginx

Redis (Future)

---

# Deployment Pipeline

Developer

↓

Git

↓

CI/CD

↓

Testing

↓

Staging

↓

Production

---

# Future

- Kubernetes
- Load Balancer
- Auto Scaling