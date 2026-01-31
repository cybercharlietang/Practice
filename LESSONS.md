# Lessons Learned

## Context: Coding Test vs Mock Interview

| Context | Priority |
|---------|----------|
| **Coding Test** | Correctness → Speed → Understanding. Runtime/elegance don't matter. |
| **Mock Interview** | Correctness → Understanding → Clean code → Efficiency. Explain your reasoning. |

## CodeSignal Assessment Reality
- **Correctness over elegance** — ugly code that works beats clean code that doesn't
- **Runtime doesn't matter** — O(n³) that passes all tests = full marks
- **Implementation speed is king** — get working solution fast, don't optimize
- **Must know pytest** — running tests, filtering, debugging
- **Must know pdb** — debugging when tests fail
- **Class-based problems** — 4-level progressive class design (Q3 style)
- **Always understand what you write** — even if ugly, you must know why it works

## What's Needed vs Not Needed

| NOT Needed | Needed |
|------------|--------|
| Binary search | Counter, defaultdict |
| Two pointers | Linked lists |
| Dynamic programming | Sorted sets (bisect, sortedcontainers) |
| Complex algorithms | Queues, Stacks (deque) |
| | Dict with metadata (size, timestamp, ttl) |
| | Custom sorting with lambda |
| | State management / snapshots |

**Focus:** Data structure manipulation, not algorithm patterns.

## ICA Problem Patterns (from practice repo)

1. **Level 1:** Basic CRUD with dict storage
2. **Level 2:** Search/filter with custom sorting
3. **Level 3:** Add time dimension (timestamps, TTL/expiration)
4. **Level 4:** Complex state (rollback, undo)

**Key skills:**
- Store objects with metadata: `{name: {"size": x, "timestamp": t, "ttl": ttl}}`
- Sort with multiple criteria: `sorted(items, key=lambda x: (-x[1], x[0]))`
- Check expiration: `current_time <= upload_time + ttl`
- Track history for rollback

## Problem Description Format (CodeSignal Style)
- Concise but clear — explain what the function/method does
- Use `:param` and `:return:` notation for args and return values
- Mention edge cases and special behavior briefly
- No hints, no excessive input/output examples
- Let the test cases show examples, docstring explains behavior

## Common Pitfalls (from training)
- `filter(fn, iter)` takes function object, not function call — `filter(str.isalnum, s)` not `filter(str.isalnum(), s)`
- Character reversal (`s[::-1]`) vs word reversal (`' '.join(s.split()[::-1])`) — different operations
- RLE compress: don't forget to flush the last run after loop ends
- Always run tests before declaring done — code ordering bugs are easy to miss
- `int(some_set)` doesn't work — use `.pop()` or `next(iter(s))` to extract element
- `l = arr` is reference, not copy — use `arr[:]` or `arr.copy()` for true copy
- Never modify list while iterating — use list comprehension or iterate over copy
- `sorted(a + b)` is O((n+m) log(n+m)); two-pointer merge is O(n+m)

## ICA Mock Test Structure (from CodeSignal screenshots)
- File structure: `tests/level_X_tests.py` (read-only), `sandbox_tests.py` (editable), `*_impl.py` (your code)
- Uses Python `unittest` with `@timeout(seconds)` decorator
- Tests use `@classmethod def setup(cls)` for shared container instance in sandbox
- Progressive levels: complete Level 1 to unlock Level 2
- Execution time limit: 3 seconds, Memory limit: 4g

## Assessment Strategy
- Q1+Q2: Speed over elegance
- Q4: Get working solution first (5-10 min), optimize later
- Q3: Invest most time here, modular design pays off

## Python Performance
- `''.join()` over `+=` for strings
- `set`/`dict` membership over `list`
- Avoid slicing in loops

## Data Structure Selection
- Need O(1) both ends → `deque`
- Need fast membership → `set`/`dict`
- Need min/max efficiently → `heapq`
- Need sorted insertion point → `bisect`
