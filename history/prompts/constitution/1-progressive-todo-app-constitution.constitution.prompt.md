---
id: 1
title: progressive-todo-app-constitution
stage: constitution
date_iso: 2026-02-05
surface: agent
model: Qwen
feature: progressive-todo-application
branch: main
user: Huniza computer
command: /sp.constitution /sp.specify
labels:
  - constitution
  - todo-app
  - progressive-enhancement
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests_yaml: []
prompt_text: |
  ---
  description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
  handoffs: 
    - label: Build Specification
      agent: sp.specify
      prompt: Implement the feature specification based on the updated constitution. I want to build...
  ---

  ## User Input

  ```text
  $ARGUMENTS
  ```

  You **MUST** consider the user input before proceeding (if not empty).

  ## Outline

  You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

  Follow this execution flow:

  1. Load the existing constitution template at `.specify/memory/constitution.md`.
     - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
     **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

  2. Collect/derive values for placeholders:
     - If user input (conversation) supplies a value, use it.
     - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
     - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
     - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
       - MAJOR: Backward incompatible governance/principle removals or redefinitions.
       - MINOR: New principle/section added or materially expanded guidance.
       - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
     - If version bump type ambiguous, propose reasoning before finalizing.

  3. Draft the updated constitution content:
     - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
     - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
     - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
     - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

  4. Consistency propagation checklist (convert prior checklist into active validations):
     - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
     - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
     - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
     - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
     - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

  5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
     - Version change: old → new
     - List of modified principles (old title → new title if renamed)
     - Added sections
     - Removed sections
     - Templates requiring updates (✅ updated / ⚠ pending) with file paths
     - Follow-up TODOs if any placeholders intentionally deferred.

  6. Validation before final output:
     - No remaining unexplained bracket tokens.
     - Version line matches report.
     - Dates ISO format YYYY-MM-DD.
     - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

  7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

  8. Output a final summary to the user with:
     - New version and bump rationale.
     - Any files flagged for manual follow-up.
     - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

  Formatting & Style Requirements:

  - Use Markdown headings exactly as in the template (do not demote/promote levels).
  - Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
  - Keep a single blank line between sections.
  - Avoid trailing whitespace.

  If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

  If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

  Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

  ---

  As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

  1) Determine Stage
     - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

  2) Generate Title and Determine Routing:
     - Generate Title: 3–7 words (slug for filename)
     - Route is automatically determined by stage:
       - `constitution` → `history/prompts/constitution/`
       - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
       - `general` → `history/prompts/general/`

  3) Create and Fill PHR (Shell first; fallback agent‑native)
     - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
     - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
     - If the script fails:
       - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
       - Allocate an ID; compute the output path based on stage from step 2; write the file
       - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

  4) Validate + report
     - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
     - On failure: warn, don't block. Skip only for `/sp.phr`.

  /sp.constitution /sp.specify

  Project: Progressive Todo Application – Console → Web → AI Chatbot → K8s → Cloud-Native

  Ultimate vision
  Build a single coherent Todo application that starts extremely simple (pure in-memory console) and systematically evolves through five production-grade phases without rewriting the domain logic from scratch each time.

  Core principles
  - Strict progressive enhancement: 90%+ of business/domain logic must survive from Phase I → Phase V
  - Technology discipline: use ONLY the exact tools and stack listed for each phase — no substitutes, no extras unless explicitly needed for that phase
  - Production mindset from day one: clean structure, error handling, input validation, helpful feedback messages
  - Documentation-first development: every phase must have excellent README + inline comments explaining design decisions
  - Consistency of user mental model: same core commands/operations should feel familiar across all interfaces

  Domain model (must remain compatible across all phases)
  Todo item fields:
  - id: str or int (auto-generated, unique)
  - title: str (required, 1–200 chars)
  - description: str (optional)
  - status: str (pending | in-progress | completed) — default: pending
  - priority: str (low | medium | high) — default: medium
  - due_date: str or date (optional, ISO format YYYY-MM-DD)
  - created_at: datetime
  - updated_at: datetime

  Core operations (all phases must support):
  1. Create new todo
  2. List all todos (with optional filters: status, priority, overdue)
  3. Get single todo by id
  4. Update todo (any field except id/created_at)
  5. Delete todo
  6. Mark as completed / reopen
  7. Clear completed (optional bonus)

  Phase-specific requirements

  Phase I – In-Memory Python Console App
  - Python 3.10+
  - Storage: in-memory only (list or dict)
  - Interface: friendly REPL or numbered menu + text commands
    Examples: add "Buy milk" --desc "whole milk" --prio high --due 2026-02-10
             list --status pending --prio high
             done 3
             edit 3 --title "Buy oat milk"
             delete 7
             quit
  - Zero external dependencies (stdlib only)
  - Graceful error messages + input validation
  - Basic help command
  - Use Claude + Spec-Kit Plus for code & spec refinement

  Phase II – Full-Stack Web Application
  - Backend: FastAPI + SQLModel + async PostgreSQL (Neon serverless)
  - Frontend: Next.js 14+ App Router, TypeScript, Tailwind CSS
  - API: RESTful endpoints covering all core operations
  - Authentication: simple JWT or API key (optional but recommended)
  - Data persistence: real database (schema migrations with Alembic recommended)
  - CORS, proper status codes, request/response models
  - Docker + docker-compose for local development

  Phase III – AI-Powered Todo Chatbot
  - Natural language interface on top of Phase II backend
  - AI stack: OpenAI Chat Completions / Assistants API + OpenAI ChatKit / Agents SDK / Official MCP SDK
  - Capabilities:
    • "Add task: finish report by Friday high priority"
    • "Show me all overdue tasks"
    • "Mark task 5 as done"
    • "What should I work on today?" (smart prioritization)
  - Context-aware conversation (remembers recent tasks/user preferences)
  - Fallback to "I didn't understand, please try again" + suggestions

  Phase IV – Local Kubernetes Deployment
  - Containerize Phase II + Phase III services (separate images)
  - Local cluster: Minikube
  - Packaging: Helm 3 chart(s)
  - Tools: kubectl-ai, kagent for AI-assisted operations
  - Required manifests: Deployments, Services, Ingress (nginx ingress recommended), ConfigMaps/Secrets
  - Basic observability: readiness/liveness probes
  - Verify: helm install → port-forward → full CRUD via web + chatbot works

  Phase V – Advanced Cloud Deployment
  - Cluster: DigitalOcean Kubernetes (DOKS)
  - Event streaming: Kafka (for task created/updated/completed events, reminders, etc.)
  - Dapr sidecar: used for
    - pub/sub (Kafka)
    - state management
    - service invocation
  - Production hardening: HorizontalPodAutoscaler, Ingress with TLS, secrets from DigitalOcean vault or similar
  - End-to-end demo flow: chat message → task created → event published → processed (e.g. reminder sent or status changed)

  Constraints – apply to ALL phases
  - Never break backward compatibility of the core Todo model
  - Environment variables for all credentials, ports, connection strings
  - No hard-coded secrets ever
  - Consistent naming: todos, not tasks/items (unless intentional branding)
  - Git branch strategy recommended: main, phase-1, phase-2, ...

  Definition of Done – per phase
  Phase I:  all CRUD + filters work in console, survives many operations, clean code & README
  Phase II:  browser UI + API fully functional, data survives restart, Neon DB used
  Phase III: natural language commands correctly execute core operations
  Phase IV: helm install on minikube → everything runs and is reachable
  Phase V:  deployed to DOKS, Kafka + Dapr working, observable event flow

  Deliver each phase as:
  - Clean folder structure
  - requirements.txt / package.json
  - Dockerfile(s)
  - docker-compose.yml (Phases I–III)
  - Helm chart (Phase IV+)
  - Detailed README.md with setup, run, architecture notes
response_text: |
  I've successfully created and updated the constitution for the Progressive Todo Application. Here's a summary of what was accomplished:

  ## Summary

  1. **New Constitution Created**: I've created a comprehensive constitution for the Progressive Todo Application with version 1.0.0, ratified on 2026-02-05.

  2. **Core Principles Defined**: The constitution includes six core principles:
     - Strict Progressive Enhancement
     - Technology Discipline
     - Production Mindset from Day One
     - Documentation-First Development
     - Consistency of User Mental Model
     - Backward Compatibility Assurance

  3. **Template Updates**: I've updated the dependent templates to align with the new constitution:
     - Updated the "Constitution Check" section in the plan template
     - Modified functional requirements in the spec template to reflect constitution principles
     - Adjusted foundational tasks in the tasks template to emphasize core domain model implementation
     - Added compliance verification steps throughout the templates

  4. **Governance Section**: Included specific governance rules for the project, emphasizing code review compliance, backward compatibility, and amendment procedures.

  ## Files Updated

  - `.specify/memory/constitution.md` - The main constitution file
  - `.specify/templates/plan-template.md` - Updated constitution check section
  - `.specify/templates/spec-template.md` - Updated functional requirements section
  - `.specify/templates/tasks-template.md` - Updated foundational tasks and implementation strategy

  ## Commit Message Suggestion

  `docs: create constitution for Progressive Todo Application v1.0.0`

  The constitution is now ready for use and will guide the development of the Progressive Todo Application through all five phases while ensuring consistency and adherence to the core principles.
outcome: |
  Successfully created the constitution for the Progressive Todo Application with version 1.0.0, including all core principles and governance rules. Updated dependent templates to align with the new constitution. Created a PHR record for this change.
evaluation: |
  The constitution has been successfully created and all dependent templates have been updated. The PHR record has been created as required. All tasks are completed.
---

# Prompt History Record: Progressive Todo Application Constitution

## Overview
This PHR documents the creation of the constitution for the Progressive Todo Application, outlining core principles and governance rules for the project.

## Changes Made
- Created a comprehensive constitution with six core principles
- Updated dependent templates to align with the new constitution
- Established governance rules for the project

## Files Modified
- `.specify/memory/constitution.md`
- `.specify/templates/plan-template.md`
- `.specify/templates/spec-template.md`
- `.specify/templates/tasks-template.md`

## Validation
- All templates updated to reflect constitution principles
- Constitution includes all required elements
- PHR record created as required