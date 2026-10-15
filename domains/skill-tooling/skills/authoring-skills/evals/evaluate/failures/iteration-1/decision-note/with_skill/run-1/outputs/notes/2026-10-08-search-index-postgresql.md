---
status: draft
---

# Move the search index to PostgreSQL

## Decision

We will move the search index to PostgreSQL.

## Reason

The current store cannot do full-text search. PostgreSQL can.

## Next

- Migrate the schema to PostgreSQL: Alice, next week (week of 2026-10-12).
