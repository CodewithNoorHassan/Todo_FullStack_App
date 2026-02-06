---
id: "0001"
title: "Amend Project Constitution"
stage: "constitution"
date_iso: "2026-01-21"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "unknown"
command: "manual"
labels: ["constitution", "governance", "spec-driven-development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml:
  - "none"
---

# Amend Project Constitution

## Prompt Text
```
You are Claude Code acting as an autonomous agent in a Spec-Driven Development workflow.

This project MUST strictly follow Specification-First and Agentic Development principles.

==============================
SP-CONSTITUTION (MANDATORY)
==============================

1. SOURCE OF TRUTH
- All development decisions MUST be derived from specifications located in the /specs directory.
- Code MUST NOT be written unless a relevant specification exists.
- If a required behavior is missing from specs, STOP and request a spec update instead of guessing.

2. SPEC PRIORITY ORDER
When implementing any feature, follow this strict priority:
1) /specs/overview.md
2) /specs/features/*.md
3) /specs/api/*.md
4) /specs/database/*.md
5) /specs/ui/*.md
6) Root CLAUDE.md
7) frontend/CLAUDE.md or backend/CLAUDE.md

3. AGENTIC WORKFLOW (NO EXCEPTIONS)
For every feature or change:
- First: Read and summarize the relevant specs.
- Second: Generate an implementation plan.
- Third: Break the plan into explicit tasks.
- Fourth: Implement tasks incrementally.
- Fifth: Verify implementation against acceptance criteria in specs.

DO NOT skip or merge steps.

4. NO MANUAL CODING ASSUMPTION
- Assume the human will NOT write or modify any code.
- All code changes must be made by you.
- Do NOT instruct the human to "add", "edit", or "fix" code manually.

5. TECHNOLOGY LOCK
The following technologies are LOCKED and MUST NOT be replaced:
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Spec System: GitHub Spec-Kit Plus

6. AUTHENTICATION RULES
- All API endpoints MUST require a valid JWT token.
- JWT must be verified in FastAPI using a shared secret (BETTER_AUTH_SECRET).
- User identity MUST be derived from the JWT, not trusted from request parameters.
- All database queries MUST be filtered by authenticated user ID.
- Unauthorized requests MUST return 401.
- Cross-user access MUST be rejected.

7. API STABILITY
- REST API endpoints MUST match exactly what is defined in /specs/api/rest-endpoints.md.
- Endpoint paths and HTTP methods MUST NOT change unless the spec changes.
- Behavior changes require spec updates first.

8. MONOREPO CONTEXT
- This is a single monorepo containing frontend and backend.
- You MUST consider cross-cutting changes across frontend, backend, and database.
- Follow CLAUDE.md instructions at root and subfolder levels.

9. ERROR HANDLING & SAFETY
- If specs conflict, STOP and explain the conflict.
- If specs are incomplete, STOP and request clarification.
- Do NOT hallucinate features, endpoints, or schemas.

10. EVALUATION MODE
- This project is evaluated on PROCESS, not speed.
- Clarity, spec compliance, and agentic reasoning are more important than shortcuts.

==============================
ACKNOWLEDGEMENT REQUIRED
==============================

Before writing any code, you MUST:
- Confirm that you have read and understood this SP-Constitution.
- List the specs you will read first for Phase
```

## Response Text
Successfully updated the project constitution at .specify/memory/constitution.md with specific principles for the TodoApp_FullStack project, including Specification-First Development, Technology Stack Lock, Authentication Security, Agentic Workflow Compliance, Monorepo Context Awareness, and Error Handling & Safety.

## Outcome Impact
Established a comprehensive project constitution that enforces specification-first development, locked technology stack adherence, and security-focused authentication patterns for the TodoApp_FullStack project.

## Tests Summary
No automated tests were run as this was a documentation/governance update.

## Files Summary
Updated .specify/memory/constitution.md with project-specific governance principles and development constraints.

## Next Prompts
Consider creating the initial feature specifications in the /specs directory to align with the new constitution's requirements.

## Reflection Note
The constitution establishes strong governance patterns that will ensure consistent development practices and prevent deviations from the agreed-upon technology stack and security requirements.

## Failure Modes Observed
None observed - the constitution was updated successfully with appropriate project-specific values.

## Next Experiment to Improve Prompt Quality
None needed - the constitution template was well-structured and allowed for proper customization with project-specific values.