# Implementation Plan: In-Memory Todo Console Application

**Branch**: `1-in-memory-todo-app` | **Date**: 2026-02-05 | **Spec**: [link to spec]
**Input**: Feature specification from `/specs/1-in-memory-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a clean, user-friendly, command-line based Todo application that stores all data in memory. The application will implement all 5 core features (add, list, update, delete, mark complete) using Typer for the CLI and Rich for beautiful output formatting. The architecture follows a layered approach with clear separation of concerns: domain models, repository, service layer, and presentation layer.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: Typer, Rich
**Storage**: In-memory only (dict[int, Todo] + counter for ID generation)
**Testing**: pytest
**Target Platform**: Cross-platform console application
**Project Type**: Single project with layered architecture
**Performance Goals**: Startup time < 100ms, all commands respond in < 50ms (in-memory)
**Constraints**: Dependencies limited to: typer, rich (and typing-extensions if needed), no persistence of any kind, only UV for dependency management
**Scale/Scope**: Individual user application, single-threaded, up to hundreds of todos

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification
- [x] Progressive Enhancement: 90%+ of business/domain logic preserved from previous phases
- [x] Technology Discipline: Using ONLY the exact tools and stack listed for this phase
- [x] Production Mindset: Clean structure, error handling, input validation, helpful feedback implemented
- [x] Documentation-First: README and inline comments explaining design decisions included
- [x] User Mental Model Consistency: Core commands/operations familiar across interfaces
- [x] Backward Compatibility: Core Todo model remains compatible
- [x] Constraint Adherence: Environment vars for credentials, no hard-coded secrets, consistent naming

## Phase 0: Research Completed
- [x] Researched Python 3.13 usage and features
- [x] Researched Typer for CLI framework
- [x] Researched Rich for output formatting
- [x] Researched dataclasses for data modeling
- [x] Researched layered architecture patterns
- [x] Researched in-memory storage implementations
- [x] Researched error handling strategies
- [x] Created research.md with all decisions and rationales

## Phase 1: Design & Contracts Completed
- [x] Extracted entities from feature spec to create data-model.md
- [x] Generated API contracts from functional requirements
- [x] Created quickstart.md with installation and usage instructions
- [x] Created contracts/api-contract.md with detailed interface specifications

## Project Structure

### Documentation (this feature)

```text
specs/1-in-memory-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-app/
├── pyproject.toml               # UV + dependencies + console_scripts
├── uv.lock
├── README.md                    # Installation, usage examples, architecture overview
├── .python-version              # 3.13
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── main.py              # Typer app entry point
│       ├── models.py            # Todo dataclass / Pydantic model
│       ├── repository/
│       │   ├── __init__.py
│       │   └── memory_repository.py
│       ├── service/
│       │   ├── __init__.py
│       │   └── todo_service.py
│       └── cli/
│           ├── __init__.py
│           └── commands.py      # All Typer commands
└── tests/                       # pytest structure (at least unit tests for service)
    ├── __init__.py
    └── test_todo_service.py
```

**Structure Decision**: Single project with layered architecture following the specified structure with domain models, repository, service, and CLI layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |