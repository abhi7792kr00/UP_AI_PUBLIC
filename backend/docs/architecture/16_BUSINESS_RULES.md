# Business Rules Architecture

Version: 2.0

Status: Draft

---

# Purpose

Business Rules determine routing, priority, SLA, and escalation decisions.

---

# Rule Examples

Road Complaint

↓

PWD

---

Water Supply

↓

Jal Nigam

---

Street Light

↓

Electricity Department

---

# Rule Inputs

Category

Subcategory

Address

Administrative Hierarchy

Priority

Citizen Context

---

# Rule Outputs

Department

Office

Priority

SLA

Escalation

---

# Rule Source

Business Rules should be configurable.

Avoid hardcoded routing logic.

Future implementation may use database-driven configuration.

---

# Rule Engine

Complaint

↓

Business Rule Engine

↓

Decision

↓

Workflow