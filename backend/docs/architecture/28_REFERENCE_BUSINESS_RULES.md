# 28. Reference Business Rules

**Document Version:** 1.0

**Status:** Draft

**Module:** Business Engine

**Engine:** Reference Engine

---

# Purpose

This document defines the business rules that govern
reference number generation across the UP_AI platform.

Every implementation inside the Reference Engine must
follow these rules.

---

# Scope

This document applies to every module that generates
business reference numbers, including:

- Complaint
- Leave
- Transfer
- Promotion
- Retirement
- Property
- Revenue
- Scholarship
- Future Modules

---

# Rule-001

## Reference Type Must Exist

Description

The requested module must be registered in the
ReferenceType master.

Example

COMPLAINT

Result

✓ Continue

If not found

Raise

ReferenceTypeNotFound

---

# Rule-002

## Reference Type Must Be Active

Description

Inactive modules cannot generate
reference numbers.

Example

Complaint

Active = False

Result

ReferenceTypeInactive

---

# Rule-003

## Exactly One Active Reference Format Must Exist

Description

Every active module must have exactly
one active reference format.

Valid

Complaint

↓

CMP

Invalid

Complaint

↓

No Format

Invalid

Complaint

↓

CMP

↓

ICMP

(two active formats)

Result

NoActiveReferenceFormat

or

MultipleActiveReferenceFormats

---

# Rule-004

## Auto Create Sequence

Description

If no sequence exists for the requested
period, the engine shall automatically
create one.

Example

2026

↓

Sequence Missing

↓

Create

Current Sequence = 0

Continue

---

# Rule-005

## Transaction Safe Sequence Generation

Description

Sequence generation must occur inside
a database transaction.

Concurrent requests must never
generate duplicate reference numbers.

---

# Rule-006

## Increment Sequence

Description

The engine shall increment
the current sequence by one.

Example

125

↓

126

---

# Rule-007

## Persist Sequence

Description

The updated sequence must be stored
before returning the generated reference.

---

# Rule-008

## Format Reference

Description

The reference number shall be generated
using the active ReferenceFormat.

Example

Prefix

CMP

Period

2026

Sequence

126

Result

CMP-2026-000126

---

# Rule-009

## Detect Sequence Overflow

Description

Generated sequence must not exceed
the configured sequence length.

Example

Sequence Length

6

Maximum

999999

Next

1000000

Result

SequenceOverflow

---

# Rule-010

## Reference Number Must Be Unique

Description

Generated reference numbers must
always be unique.

Duplicate reference numbers are
strictly prohibited.

---

# Rule-011

## Business Engine Never Guesses

Description

If configuration is ambiguous,
the engine shall stop execution.

The engine must never guess.

Examples

Multiple Active Formats

Missing Configuration

Invalid Module

Inactive Module

Result

Raise Appropriate Exception

---

# Rule-012

## Configuration Driven Design

Description

Reference generation must always
use database configuration.

Business rules must never be
hardcoded inside the engine.

---

# Rule-013

## Engine Independence

Description

The Reference Engine must not contain
Complaint-specific, Leave-specific,
or Property-specific logic.

The engine shall remain reusable
across the entire UP_AI platform.

---

# Summary

The Reference Engine follows the
following execution flow.

Reference Type

↓

Reference Format

↓

Reference Sequence

↓

Generator

↓

Formatter

↓

Generated Reference

---

# Related Documents

26_BUSINESS_ENGINE_ARCHITECTURE.md

27_REFERENCE_NUMBER_ENGINE.md

ADR-001_REFERENCE_MANAGEMENT.md