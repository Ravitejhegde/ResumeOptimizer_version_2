# Knowledge Builder Exporters

The Exporters package is responsible for persisting optimized knowledge
artifacts into deployable formats.

Exporters are the final stage of the Knowledge Builder.

```
Knowledge Sources
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
```

---

## Responsibilities

Exporters:

- Persist optimized artifacts
- Produce runtime-ready files
- Keep serialization isolated
- Never modify knowledge

Exporters do **NOT**:

- Read source JSON
- Validate knowledge
- Build indexes
- Execute business logic

---

## Current Exporters

### JsonExporter

Exports every optimized artifact into a readable JSON file.

Output:

```
knowledge.json
```

Useful for:

- Debugging
- Inspection
- Development
- Version comparison

---

### CacheExporter

Exports a binary cache for fast startup.

Output:

```
knowledge.cache
```

Useful for:

- Production runtime
- Faster application startup
- Reduced rebuild time

---

### ExportManager

Coordinates multiple exporters.

Instead of:

```
JsonExporter
CacheExporter
```

The pipeline simply executes:

```python
manager.export(artifacts)
```

---

## Adding a New Exporter

Every exporter inherits from:

```python
BaseExporter[T]
```

Example:

```python
class SQLiteExporter(
    BaseExporter[KnowledgeArtifacts]
):
    ...
```

Register it:

```python
manager.register(
    SQLiteExporter(output_directory)
)
```

No other code changes are required.

---

## Design Principles

- Single Responsibility
- Open/Closed Principle
- Immutable inputs
- No side effects
- Production-safe serialization

---

## Future Exporters

Planned exporters include:

- SQLite
- PostgreSQL
- Redis
- Parquet
- MessagePack
- Cloud Storage
- Memory-mapped binary format

These can be added without changing the existing architecture.

---

## Package Structure

```
exporters/
│
├── __init__.py
├── base_exporter.py
├── json_exporter.py
├── cache_exporter.py
├── export_manager.py
└── README.md
```

---

## Runtime

ResumeOptimizer should consume exported artifacts rather than rebuilding
knowledge every application startup whenever possible.

Recommended startup flow:

```
Load Cache
     │
     ├── Success → Ready
     │
     └── Missing
             │
             ▼
      Rebuild Knowledge
             │
             ▼
       Export Cache
             │
             ▼
           Ready
```

This minimizes startup time while ensuring the runtime always has a
validated and optimized knowledge base.