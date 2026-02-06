<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Added sections: All principles and sections as specified
Removed sections: None
Templates requiring updates: N/A (new constitution)
Follow-up TODOs: None
-->
# TodoApp_FullStack Constitution

## Core Principles

### Specification-First Development
All development decisions must be derived from specifications in /specs directory; Code must not be written unless a relevant specification exists

### Technology Stack Lock
Adhere to locked technology stack: Next.js, FastAPI, SQLModel, Neon PostgreSQL, Better Auth; No technology substitution without spec update

### Authentication Security
All API endpoints require JWT verification; User identity derived from JWT, not request parameters; Database queries filtered by authenticated user ID

### Agentic Workflow Compliance
Follow strict agentic workflow: Read specs → Generate plan → Break into tasks → Implement incrementally → Verify against acceptance criteria

### Monorepo Context Awareness
Consider cross-cutting changes across frontend, backend, and database; Follow CLAUDE.md instructions at all levels

### Error Handling & Safety
Stop when specs conflict or are incomplete; Do not hallucinate features, endpoints, or schemas

## Development Constraints
No manual coding assumption - all changes by agent; API endpoints must match specs exactly; Behavior changes require spec updates first

## Development Workflow
Priority order: specs/overview.md → specs/features/*.md → specs/api/*.md → specs/database/*.md → specs/ui*.md → Root CLAUDE.md → subfolder CLAUDE.md

## Governance
Constitution supersedes all practices; Amendments require documentation; All code changes must comply with locked tech stack and authentication rules

**Version**: 1.0.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21