# Architecture — Task Master

## ER Diagram

```
┌─────────────────────┐
│ ListMember          │
├─────────────────────┤
│ id         Integer ││
│ list_id    Integer ││
│ user_id    Integer ││
│ role       String  ││
│ added_at   DateTime││
└─────────────────────┘

┌─────────────────────┐
│ List                │
├─────────────────────┤
│ id         Integer ││
│ name       String  ││
│ owner_id   Integer ││
│ created_at DateTime││
└─────────────────────┘

┌─────────────────────┐
│ Tag                 │
├─────────────────────┤
│ id         Integer ││
│ name       String  ││
└─────────────────────┘

┌─────────────────────┐
│ TaskTag             │
├─────────────────────┤
│ task_id    Integer ││
│ tag_id     Integer ││
└─────────────────────┘

┌─────────────────────┐
│ Task                │
├─────────────────────┤
│ id         Integer ││
│ title      String  ││
│ description Text    ││
│ due_date   DateTime││
│ completed  Boolean ││
│ list_id    Integer ││
│ created_at DateTime││
│ updated_at DateTime││
└─────────────────────┘

┌─────────────────────┐
│ User                │
├─────────────────────┤
│ id         Integer ││
│ email      String  ││
│ hashed_password Strin│
│ full_name  String  ││
│ created_at DateTime││
└─────────────────────┘

```

## Backend Architecture

```
FastAPI Application
├── Routing Layer (app/routes/)     → HTTP request handling
├── Service Layer (app/services/)   → Business logic
├── Model Layer (app/models/)       → Database ORM (SQLAlchemy)
├── Schema Layer (app/schemas/)     → Validation (Pydantic v2)
└── Database (app/database.py)      → Session management (SQLite)
```

## Design Patterns

- **Repository pattern**: services own DB queries, routes own HTTP logic
- **Dependency injection**: `get_db` session injected via FastAPI `Depends()`
- **Schema separation**: ORM models never exposed directly; Pydantic schemas serialize responses
- **JWT auth**: Bearer tokens validated via `oauth2_scheme` dependency
