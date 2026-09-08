# Aggregate Design

Version: 2.0

Status: Draft

---

# Purpose

This document defines the aggregate structure of the Complaint Domain.

The Complaint Aggregate acts as the central consistency boundary for complaint processing.

---

# Aggregate Root

Complaint

The Complaint entity is the Aggregate Root.

All related entities are managed through the Complaint Aggregate.

---

# Aggregate Structure

Complaint

│

├── Complaint Details

├── Address

├── Attachments

├── Timeline

├── Assignment History

├── Feedback

├── Resolution

└── Audit Log

---

# Complaint Details

Contains

- Title

- Description

- Category

- Subcategory

- Incident Date

---

# Address

Contains

- Address Type

- Rural Hierarchy

- Urban Hierarchy

- Landmark

- Coordinates

---

# Attachments

Supports

- Images

- Videos

- Audio

- PDF

- Documents

---

# Timeline

Stores

- Status Changes

- Officer Actions

- Citizen Events

---

# Assignment History

Stores

- Assigned Officer

- Assigned Office

- Assigned Time

- Reassignment History

---

# Feedback

Stores

- Citizen Rating

- Citizen Remarks

---

# Resolution

Stores

- Resolution Summary

- Resolution Date

---

# Audit Log

Stores

- Who Changed

- What Changed

- When Changed

---

# Design Rules

Complaint is the only Aggregate Root.

Child entities should never be modified independently.

All updates must pass through the Complaint Aggregate.

---

# Future Scope

Versioning

Event Sourcing

Distributed Processing