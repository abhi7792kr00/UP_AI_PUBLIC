# Service Pattern

Version: 2.0

Status: Draft

---

# Purpose

Services coordinate repositories and implement domain-level business operations.

---

# Responsibilities

- Coordinate repositories
- Execute business operations
- Prepare data for workflows

---

# Base Service

Generic BaseService provides reusable CRUD operations.

---

# Service Rules

Services

↓

Repositories

↓

Database

Services never access FastAPI Request or Response.

---

# Structure

BaseService

↓

StateService

DivisionService

ComplaintService

OfficerService

CitizenService

---

# Design Principles

Services should remain reusable.

Services should not implement workflow orchestration.