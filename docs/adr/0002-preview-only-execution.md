# 0002: Preview-only execution boundary

Status: Accepted

Context: Broker integration concepts should be visible without permitting execution.

Decision: Map plain orders to IB-style dictionaries with transmission disabled. Provide only an in-memory mock; reject every submit call.

Consequences: Mapping and deduplication can be tested offline. Connectivity, API-version compatibility, partial fills and reconciliation require a separately reviewed adapter and are outside this example.
