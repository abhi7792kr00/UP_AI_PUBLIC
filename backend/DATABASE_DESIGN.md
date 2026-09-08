# DATABASE DESIGN

Project:
UP_AI – Uttar Pradesh Unified Digital Governance & Transparency Platform

Version:
1.0

---

# Database Philosophy

The database is designed using a modular and scalable architecture.

Each government domain is implemented independently while maintaining proper relationships with common master data.

---

# Database Architecture

```
Authentication
        │
        ▼
Citizen
        │
        ▼
Complaint
        │
        ▼
Department
        │
        ▼
Officer
        │
        ▼
Service History
```

---

# Database Modules

## Authentication

Tables

- users
- roles

---

## Master

Tables

- states
- divisions
- districts
- tehsils
- blocks
- gram_panchayats
- villages
- administrative_levels

---

## Citizen

Tables

- citizens

---

## Government

Tables

- departments
- designations
- offices
- officers

Service History

- postings
- transfers
- promotions
- leaves
- suspensions
- retirements
- trainings

---

## Complaint

Tables

- complaints
- complaint_categories
- complaint_subcategories
- complaint_priorities
- complaint_statuses
- complaint_category_mappings
- complaint_subcategory_mappings
- complaint_assignments
- complaint_timelines
- complaint_attachments
- complaint_feedbacks
- complaint_otps
- complaint_escalations

---

# Primary Relationships

Citizen

↓

Complaint

Complaint

↓

Category

Complaint

↓

SubCategory

Complaint

↓

Priority

Complaint

↓

Status

Complaint

↓

Department

Complaint

↓

Office

Complaint

↓

Officer

Complaint

↓

Timeline

Complaint

↓

Attachments

Complaint

↓

Feedback

---

# Complaint Workflow Relationship

Citizen

↓

Complaint

↓

Assignment

↓

Timeline

↓

Resolution

↓

Feedback

---

# Government Hierarchy

State

↓

Division

↓

District

↓

Tehsil

↓

Block

↓

Gram Panchayat

↓

Village

---

# Officer Service History

Officer

↓

Posting

↓

Transfer

↓

Promotion

↓

Training

↓

Leave

↓

Suspension

↓

Retirement

---

# Naming Convention

Table Names

Plural

Examples

users

officers

complaints

Columns

snake_case

Examples

created_at

updated_at

department_id

officer_id

Foreign Keys

table_name_id

Examples

department_id

office_id

officer_id

Indexes

Primary Key

id

Unique

email

username

complaint_number

---

# Common Columns

Every major table contains

id

created_at

updated_at

is_active

---

# Future Database Modules

Police

Revenue

Health

Education

Agriculture

Court

Electricity

Water

Disaster Management

RTI

AI Analytics

Audit Logs

Notifications

Documents

GIS

---

# Estimated Scale

Initial Tables

35+

Target Tables

100+

Estimated Records

Millions

Designed for PostgreSQL Production Deployment.

---

END