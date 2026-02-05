# PS-06: Class Design (Q3 Simulation)

**Target Time:** 60-90 minutes
**Focus:** Progressive class design, state management, ICA Level 1-4 patterns

## Problems

1. **Counter** - Basic counter with statistics (warm-up)
2. **LRUCache** - Least Recently Used cache with capacity
3. **RateLimiter** - Sliding window rate limiting
4. **TodoManager** - Todo list with priorities and filtering
5. **EventScheduler** - Calendar with conflict detection

## Workflow

1. Write your solutions in `solution.py`
2. Run tests: `pytest test_class_design.py -v`
3. Run specific test: `pytest test_class_design.py -k "counter" -v`

## Relevant Patterns (from CHEATSHEET.md)

```python
# Dict with metadata
self.items = {}  # {key: {"value": v, "timestamp": t, "priority": p}}

# Custom sorting
sorted(items, key=lambda x: (-x["priority"], x["created_at"]))

# Timestamp/TTL checks
current_time <= created_at + ttl

# OrderedDict for LRU (maintains insertion order, move_to_end)
from collections import OrderedDict
```

## ICA Level Mapping

| Problem | Simulates |
|---------|-----------|
| Counter | Level 1 - Basic CRUD |
| LRUCache | Level 2 - Data processing |
| RateLimiter | Level 3 - Time dimension |
| TodoManager | Level 2-3 - Search/filter + state |
| EventScheduler | Level 3-4 - Complex state |
