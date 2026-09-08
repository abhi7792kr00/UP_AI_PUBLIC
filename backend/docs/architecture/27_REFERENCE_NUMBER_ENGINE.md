# 27_REFERENCE_NUMBER_ENGINE.md

# Reference Number Engine

Version : 2.0

Status : Draft

Author : UP_AI Core Architecture

Last Updated : 2026

---

# Purpose

The Reference Number Engine is responsible for generating unique,
configurable, and reusable reference numbers across all modules of
the UP_AI platform.

The engine provides a centralized mechanism for generating
business reference numbers while ensuring uniqueness,
consistency, scalability, and future extensibility.

---

# Why this Engine?

Almost every government module requires a unique reference number.

Examples

Complaint

CMP-2026-000001

Leave

LEV-2026-000021

Transfer

TRF-2026-000145

Property

PRP-2026-000894

Instead of implementing separate generators for every module,
UP_AI provides one reusable Reference Number Engine.

---

# Objectives

The engine must

- Generate unique references
- Support multiple business modules
- Support configurable prefixes
- Support yearly sequences
- Be reusable
- Be thread-safe
- Be database-driven
- Be independent of any single module

---

# Scope

The engine can be used by

- Complaint
- Leave
- Transfer
- Promotion
- Retirement
- Training
- Property
- Citizen
- Revenue
- Scholarship
- Birth Certificate
- Death Certificate
- Future Modules

---

# Design Principles

- Reusable
- Configurable
- Stateless
- Database Driven
- Scalable
- Enterprise Ready

---


# Functional Requirements

The Reference Number Engine shall:

1. Generate unique reference numbers.

2. Support configurable module prefixes.

3. Maintain separate sequences for every module.

4. Maintain separate sequences for every year.

5. Automatically reset sequence when a new year starts.

6. Prevent duplicate reference numbers.

7. Support concurrent requests safely.

8. Allow future customization without modifying business logic.

9. Be reusable across all UP_AI modules.

10. Generate references in less than one database transaction.

---

# Non-Functional Requirements

The engine must satisfy the following quality attributes.

## Performance

- Fast generation
- Minimal database queries
- Optimized for high-volume transactions

---

## Scalability

The engine should support

- 10 modules
- 100 modules
- 500 modules

without architecture changes.

---

## Reliability

Every generated reference must be unique.

Duplicate generation is unacceptable.

---

## Maintainability

The engine should be configurable.

Future modules should not require engine modification.

---

## Security

Users must never manually generate reference numbers.

The engine is the only authorized component responsible for generating references.

---

# Reference Number Format

General format

```

PREFIX-YEAR-SEQUENCE

```

Examples

```

CMP-2026-000001

LEV-2026-000023

TRF-2026-000184

PRP-2026-000941

```

---

# Components

Reference Number consists of three parts.

## Prefix

Identifies business module.

Example

```

CMP

LEV

TRF

PRP

```

---

## Year

Business Year

Example

```

2026

2027

2028

```

---

## Sequence

Auto Increment Number

Example

```

000001

000002

000003

```

Sequence length should remain configurable.

---

# Database Design

The Reference Number Engine is backed by three database tables.

## 1. master_reference_types

Purpose

Defines every business module that requires a reference number.

Examples

- Complaint
- Leave
- Transfer
- Promotion
- Retirement
- Property

Sample Fields

- id
- module_name
- description
- is_active

---

## 2. master_reference_prefixes

Purpose

Stores configurable prefixes for every module.

Examples

| Module | Prefix |
|---------|--------|
| Complaint | CMP |
| Leave | LEV |
| Transfer | TRF |
| Property | PRP |

Sample Fields

- id
- reference_type_id
- prefix
- is_active

---

## 3. reference_sequences

Purpose

Maintains the latest generated sequence for each module and year.

Sample Fields

- id
- reference_type_id
- year
- current_sequence
- last_generated_at

---

# Entity Relationship

master_reference_types

↓

master_reference_prefixes

↓

reference_sequences

Each business module owns one active prefix.

Each prefix maintains an independent yearly sequence.