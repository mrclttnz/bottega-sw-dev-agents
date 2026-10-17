# Architecture

## Architectural drivers
| Driver (NFR / SR / constraint) | Implication |
|---|---|

## Context (C4 level 1)
```mermaid
flowchart TB
  user([User]) --> system[System]
  system --> external[(External service)]
```

## Containers (C4 level 2)
```mermaid
flowchart TB
  web[Web app] --> api[API]
  api --> db[(Database)]
```

## Components and responsibilities
| Component | Responsibility | Interfaces | Technology |
|---|---|---|---|

## Technology stack
| Layer | Choice | Version | ADR |
|---|---|---|---|

## Key flows
```mermaid
sequenceDiagram
  participant U as User
  participant A as API
  U->>A: request
  A-->>U: response
```

## Trust boundaries
## Cross-cutting strategies
- Configuration and secrets:
- Logging and observability:
- Error handling:
- Authentication and authorization:
- Caching:
- Internationalization:

## Requirements → solutions map
| ID | How it is satisfied |
|---|---|

## Architectural risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
