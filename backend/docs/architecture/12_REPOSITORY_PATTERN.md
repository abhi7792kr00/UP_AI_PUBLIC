# Repository Pattern

Version: 2.0

Status: Draft

---

# Purpose

Repositories provide a dedicated abstraction for database operations.

Repositories are responsible only for data persistence and retrieval.

---

# Responsibilities

- CRUD Operations
- Query Operations
- Database Transactions
- ORM Mapping

Repositories must never contain business logic.

---

# Base Repository

The UP AI platform uses a Generic BaseRepository.

Responsibilities

- Create
- Read
- Update
- Delete
- Pagination
- Filtering

---

# Repository Rules

Repositories

↓

Database

Only.

Repositories never call:

- API
- Workflow
- Engine

---

# Repository Structure

BaseRepository

↓

StateRepository

DivisionRepository

DistrictRepository

ComplaintRepository

OfficerRepository

CitizenRepository

---

# Design Principles

Repositories return ORM models.

Repositories never return HTTP responses.

Repositories remain independent from FastAPI.