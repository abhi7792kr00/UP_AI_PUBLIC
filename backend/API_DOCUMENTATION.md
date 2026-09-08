# API DOCUMENTATION

Project:
UP_AI – Uttar Pradesh Unified Digital Governance & Transparency Platform

Version:
1.0

---

# API Standards

Base URL

```
http://localhost:8000
```

Swagger

```
/docs
```

OpenAPI

```
/openapi.json
```

---

# Authentication

## Login

POST

```
/login
```

Description

Authenticate a user and return a JWT access token.

---

## Protected Endpoint

GET

```
/protected
```

Description

Verify JWT authentication.

---

# Role APIs

## Get Roles

GET

```
/roles
```

---

## Create Role

POST

```
/roles
```

---

# User APIs

## Get Users

GET

```
/users
```

---

## Create User

POST

```
/users
```

---

# Master Data APIs

## States

GET

```
/states
```

POST

```
/states
```

PUT

```
/states/{id}
```

DELETE

```
/states/{id}
```

---

## Divisions

GET

```
/divisions
```

POST

```
/divisions
```

---

## Districts

GET

```
/districts
```

POST

```
/districts
```

---

## Tehsils

GET

```
/tehsils
```

POST

```
/tehsils
```

---

## Blocks

GET

```
/blocks
```

POST

```
/blocks
```

---

## Gram Panchayats

GET

```
/gram-panchayats
```

POST

```
/gram-panchayats
```

---

## Villages

GET

```
/villages
```

POST

```
/villages
```

---

# Government APIs

## Departments

GET

```
/departments
```

POST

```
/departments
```

---

## Designations

GET

```
/designations
```

POST

```
/designations
```

---

## Offices

GET

```
/offices
```

POST

```
/offices
```

---

## Officers

GET

```
/officers
```

POST

```
/officers
```

---

## Posting

GET

```
/postings
```

POST

```
/postings
```

---

## Transfer

GET

```
/transfers
```

POST

```
/transfers
```

---

## Promotion

GET

```
/promotions
```

POST

```
/promotions
```

---

## Leave

GET

```
/leaves
```

POST

```
/leaves
```

---

## Suspension

GET

```
/suspensions
```

POST

```
/suspensions
```

---

## Retirement

GET

```
/retirements
```

POST

```
/retirements
```

---

## Training

GET

```
/trainings
```

POST

```
/trainings
```

---

# Complaint APIs

## Register Complaint

POST

```
/complaints
```

Description

Register a new complaint.

Future Features

- Auto Complaint Number
- AI Classification
- Auto Department Mapping
- Timeline Creation
- Assignment Engine

---

## Get All Complaints

GET

```
/complaints
```

---

## Get Complaint

GET

```
/complaints/{id}
```

---

## Update Complaint

PUT

```
/complaints/{id}
```

---

## Delete Complaint

DELETE

```
/complaints/{id}
```

---

# Dashboard APIs

Department Dashboard

District Dashboard

Officer Dashboard

State Dashboard

---

# Future APIs

Citizen Dashboard

Officer Dashboard

Transparency Portal

Analytics

Notification

Audit Logs

AI Engine

GIS

Public Officer Profile

---

# Response Format

Success

```json
{
  "success": true,
  "message": "Request completed successfully",
  "data": {}
}
```

Error

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": []
}
```

---

# HTTP Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error

---

# Versioning

Current Version

v1

Future

v2

v3

---

END