# System Architecture

```mermaid
flowchart TD
    A["Synthetic interaction"] --> B["Local fake service"]
    B --> C["Sanitize preview"]
    B --> D["Explainable classifier"]
    C --> E["SQLite event store"]
    D --> E
    E --> F["Statistics queries"]
    F --> G["Dashboard and JSON API"]
```

| Component | Responsibility | Trust boundary |
| --- | --- | --- |
| Fake service | Sends banner and reads at most 1,024 bytes | Localhost only |
| Classifier | Matches text against explainable patterns | Never executes text |
| Store | Persists events and calculates aggregates | Local SQLite file |
| Dashboard | Escapes event text and shows statistics | Localhost only |
| Simulator | Produces synthetic demonstrations | Connects only to localhost |
| Evaluator | Compares predicted and expected categories | Offline labeled data |

## Event Flow

```mermaid
sequenceDiagram
    participant Lab as Lab simulator
    participant Decoy as Fake service
    participant Rules as Classifier
    participant DB as SQLite
    participant UI as Dashboard
    Lab->>Decoy: Safe text probe
    Decoy-->>Lab: Static denial response
    Decoy->>Rules: Text only
    Rules->>DB: Category, score, reasons
    UI->>DB: Aggregate queries
    DB-->>UI: Statistics and recent events
```

No component launches a process, authenticates a user, downloads content, scans
a network, or modifies another system.
