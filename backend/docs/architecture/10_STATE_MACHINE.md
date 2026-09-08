# Complaint State Machine

Version: 2.0

Status: Draft

---

# Purpose

Defines the lifecycle of a complaint.

---

# States

Draft

↓

Submitted

↓

Validated

↓

Address Resolved

↓

Routed

↓

Assigned

↓

In Progress

↓

Action Taken

↓

Resolved

↓

Closed

---

# Alternative States

Rejected

Reopened

Cancelled

---

# State Responsibilities

Draft

Citizen can edit.

---

Submitted

Validation starts.

---

Validated

Address Resolution starts.

---

Address Resolved

Business Rules execute.

---

Routed

Department identified.

---

Assigned

Officer assigned.

---

In Progress

Officer performs investigation.

---

Action Taken

Action completed.

---

Resolved

Citizen verification.

---

Closed

Workflow completed.

---

# Allowed Transitions

Draft

↓

Submitted

Submitted

↓

Validated

Validated

↓

Address Resolved

Address Resolved

↓

Routed

Routed

↓

Assigned

Assigned

↓

In Progress

In Progress

↓

Action Taken

Action Taken

↓

Resolved

Resolved

↓

Closed

---

# Transition Rules

Every transition must:

- Create Timeline Entry

- Create Audit Entry

- Trigger Notification

- Validate Business Rules

---

# Future Enhancements

Auto Escalation

SLA Monitoring

AI Assisted Decisions