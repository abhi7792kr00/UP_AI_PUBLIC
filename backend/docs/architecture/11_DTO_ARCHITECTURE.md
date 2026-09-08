# DTO Architecture

Version: 2.0

Status: Draft

---

# Purpose

DTOs define communication contracts between application layers.

ORM models must never be exposed outside the service boundary.

---

# Complaint Registration

ComplaintRegistrationRequest

↓

ValidatedComplaintRequest

↓

ResolvedAddress

↓

BusinessRuleDecision

↓

JurisdictionContext

↓

RoutingDecision

↓

AssignmentDecision

↓

TrackingInfo

↓

ComplaintResponse

---

# Location DTOs

StateDTO

DivisionDTO

DistrictDTO

TehsilDTO

BlockDTO

GramPanchayatDTO

VillageDTO

MunicipalBodyDTO

WardDTO

LocalityDTO

---

# Government DTOs

DepartmentDTO

OfficeDTO

OfficerDTO

DesignationDTO

PostingDTO

---

# Notification DTOs

SMSRequest

EmailRequest

WhatsAppRequest

PushNotificationRequest

---

# AI DTOs

ComplaintClassification

PriorityPrediction

DuplicateComplaintResult

SummaryResponse

---

# Design Principles

DTOs are immutable.

DTOs contain no business logic.

DTOs are serialization-friendly.

DTOs remain independent of ORM models.

---

# Future Expansion

GraphQL DTOs

Public API DTOs

Mobile DTOs