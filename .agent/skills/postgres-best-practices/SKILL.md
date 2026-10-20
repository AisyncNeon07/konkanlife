---
name: postgres-best-practices
description: Best practices for PostgreSQL database schema design, index optimization, query tuning, and Django ORM migrations
---

# PostgreSQL Best Practices

## Overview

Guidance and standards for designing, querying, and maintaining PostgreSQL databases in full-stack applications.

## Query & ORM Optimization

### 1. Avoid N+1 Queries
In Django ORM, always use `select_related` (for ForeignKey/OneToOne) and `prefetch_related` (for ManyToMany/Reverse FK):
```python
# Good: 1 query with JOIN
destinations = Destination.objects.select_related('category').all()

# Good: 2 queries total instead of N+1
destinations = Destination.objects.prefetch_related('reviews').all()
```

### 2. Selective Field Fetching
Avoid pulling large text/binary fields when only IDs or names are needed:
```python
Destination.objects.only('id', 'name', 'slug')
# or
Destination.objects.defer('long_description')
```

### 3. Indexing Strategies
- Add B-Tree indexes on columns used in `WHERE`, `ORDER BY`, and `JOIN` conditions.
- Add composite indexes matching common multi-column queries (order columns by highest selectivity first).
- Use `db_index=True` or `Meta.indexes = [models.Index(fields=['...'])]` in Django models.

### 4. Safe Migrations
- Use `RunPython` with a reverse code callback for data migrations.
- Avoid setting default values on large existing tables without careful locking considerations.
