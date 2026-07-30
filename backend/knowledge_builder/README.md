# Knowledge Builder

The Knowledge Builder is the foundational component of ResumeOptimizer.

Its responsibility is to transform raw knowledge files into validated,
optimized runtime artifacts that power resume analysis, planning,
optimization, ATS intelligence, and AI prompting.

The Knowledge Builder itself contains **no resume-specific business
logic**. It exists solely to build and maintain the knowledge platform.

---

# Architecture

```
Raw Sources
      │
      ▼
Loaders
      │
      ▼
KnowledgeStore
      │
      ▼
Validators
      │
      ▼
Builders
      │
      ▼
KnowledgeArtifacts
      │
      ▼
Exporters
      │
      ▼
Runtime
```

---

# Folder Structure

```
knowledge_builder/
│
├── builders/
├── exporters/
├── loaders/
├── models/
├── output/
├── pipeline/
├── sources/
├── store/
├── tests/
├── validators/
│
├── config.py
├── main.py
└── README.md
```

---

# Module Responsibilities

## Sources

Stores raw knowledge.

Examples:

- Technologies
- Skills
- ATS rules
- Roles
- Categories
- Relationships
- Keywords
- Synonyms

---

## Loaders

Convert raw JSON into strongly typed Python models.

Loaders never:

- Validate
- Build indexes
- Modify data

---

## KnowledgeStore

Central repository containing every knowledge object.

Everything after loading uses the KnowledgeStore.

Nothing reads JSON directly anymore.

---

## Validators

Ensure:

- References exist
- IDs are unique
- Relationships are valid
- Knowledge is internally consistent

---

## Builders

Create optimized runtime structures.

Examples:

- Category index
- Technology graph
- Skill index
- Role index
- Keyword index
- Synonym index

These structures eliminate repeated linear searches.

---

## Exporters

Persist optimized artifacts.

Current exporters:

- JSON
- Binary cache

Future exporters:

- SQLite
- PostgreSQL
- Redis
- Parquet

---

# Public API

```python
from knowledge_builder.main import (
    build_knowledge_store,
    rebuild_knowledge_store,
    export_knowledge,
)
```

Build store:

```python
store = build_knowledge_store()
```

Export artifacts:

```python
export_knowledge("output")
```

---

# Runtime Flow

Application startup should follow:

```
Cache exists?
      │
      ├── Yes
      │      │
      │      ▼
      │   Load Cache
      │
      └── No
             │
             ▼
     Build Knowledge
             │
             ▼
      Validate Store
             │
             ▼
      Build Artifacts
             │
             ▼
      Export Cache
             │
             ▼
            Ready
```

---

# Design Principles

The Knowledge Builder follows these principles:

- Single Responsibility
- Strong typing
- Immutable runtime artifacts
- Separation of concerns
- No duplicated responsibilities
- Deterministic builds
- Fast runtime lookup
- Extensible architecture

---

# Integration with ResumeOptimizer

ResumeOptimizer components should depend only on exported runtime
artifacts or the validated KnowledgeStore.

Recommended dependency flow:

```
Knowledge Builder
        │
        ▼
Analyzer
        │
        ▼
Planner
        │
        ▼
Optimizer
        │
        ▼
Validator
        │
        ▼
Writer
```

This keeps every layer independent while sharing a single source of
truth.

---

# Future Roadmap

Planned enhancements include:

- Knowledge versioning
- Incremental builds
- Parallel loading
- Binary graph serialization
- Memory-mapped runtime cache
- Plugin-based knowledge providers
- Hot-reload during development
- Cloud-hosted knowledge repositories

These enhancements can be added without changing the public API.