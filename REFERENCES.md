# References

## CodeSignal Assessment Format

### GCA vs ICA
- **GCA (General Coding Assessment)**: 4 separate problems, 70 minutes, score 300-850
- **ICA (Industry Coding Assessment)**: 1 project-based question with 4 progressive levels, 90 minutes

### Question Structure (GCA)
- **Q1**: LC Easy warmup (~10 min) — prioritize speed, dirty solutions acceptable
- **Q2**: Medium (~20-25 min) — prioritize speed, dirty solutions acceptable
- **Q3**: Medium/simulation-heavy — "bashing-friendly," lengthy but not algorithmic
- **Q4**: Algorithm — hashmap applications common, DP rare, partial credit (40-60%) for brute force

### Question Structure (ICA - Progressive)
- **Level 1**: Basic implementation + corner cases
- **Level 2**: Data processing functions (calculations, exports)
- **Level 3**: Extended functionality, more complex state
- **Level 4**: Culmination, requires refactoring earlier code for backward compatibility

### Time Allocation (from GitHub practice repo)
| Level | Expected Duration |
|-------|------------------|
| 1 | 10-15 minutes |
| 2 | 20-30 minutes |
| 3 | 30-60 minutes |
| 4 | 30-60 minutes |

*Note: Cumulative time (90-165 min) exceeds 90-min limit intentionally. Measures progression, not completion.*

### Assessment Characteristics
- Tests general coding ability
- Implement from spec, pass tests
- Toy simulation of app business logic (no frameworks/UI)
- Standard library only
- No detailed algorithms, compute systems, or ML
- No Copilot/LLMs allowed, internet OK (no copy-paste of problems/solutions)

### Recommended Strategy
1. Q1 + Q2 first, do them quick
2. Skip to Q4, get working solution in 5-10 min MAX
3. Go to Q3, spend most time here with good software principles
4. Return to Q4 with remaining time (~10 min) to optimize

### Score Benchmarks
- **700-749**: Competitive threshold
- **750+**: Elite (top 10%)
- **Below 650**: Below most hiring benchmarks

### Common Q3 Patterns
- Rate limiters, processing queues, simulations
- 95% simulation, 5% algorithm
- Often O(n²) is acceptable

---

## Prior Practice Summary

### Q1-Level Topics Covered
- Sum of digits
- Reverse words
- Unique-preserve-order
- Interleave strings
- Count vowels

### Q2-Level Topics Covered
- Longest unique substring (O(n) sliding window)
- Group anagrams
- TodoManager class (OOP)

### Q3-Level Topics Discussed
- Event counter design
- Sliding windows with deque
- Handling timestamps
- Lazy pruning

### Q4-Level Topics Covered
- Heaps (heapq)
- Streaming median (two heaps)
- Sliding window maximum (deque)

---

## Data Structures Theory

### Python Built-ins
| Structure | Implementation | Key Complexities |
|-----------|----------------|------------------|
| `list` | Dynamic array | Append O(1) amortized, middle insert O(n) |
| `deque` | Doubly-linked blocks | O(1) append/pop both ends |
| `dict`/`set` | Hash table | Average O(1), worst O(n) collisions |
| `Counter` | dict subclass | Counting elements |
| `defaultdict` | dict with default factory | Avoid KeyError |
| `OrderedDict` | dict preserving insertion order | (less needed in 3.7+) |

### heapq Module
- Min-heap by default
- Max-heap via negation
- `heapify()`: O(n)
- `nlargest(k, iterable)`: O(n log k)

### bisect Module
- Binary search utilities for sorted lists

### Linked Lists vs Arrays
- Arrays: better cache locality, O(1) random access
- Linked lists: O(1) insert/delete at known position, O(n) traversal

---

## Performance Best Practices

- Avoid O(n²) string concatenation → use `''.join()`
- Avoid slicing inside loops → prefix sums or two-pointer
- Prefer `in set`/`in dict` over `in list`
- Use indices in deques for sliding window correctness

---

## CodeSignal Practice Repo Reference

**Location:** `/home/charlie/CodeSignal_Practice_Industry_Coding_Framework`

### Example Problem: File Storage System

**Level 1 — Basic CRUD:**
- `FILE_UPLOAD(file_name, size)` — add file, error if exists
- `FILE_GET(file_name)` — return size or None
- `FILE_COPY(source, dest)` — copy file, overwrite if dest exists

**Level 2 — Search/Sort:**
- `FILE_SEARCH(prefix)` — top 10 files by prefix, sorted by size desc then name

**Level 3 — Timestamps & TTL:**
- `FILE_UPLOAD_AT(timestamp, file_name, size, ttl)` — file expires after ttl seconds
- `FILE_GET_AT(timestamp, file_name)` — check if file still alive
- `FILE_SEARCH_AT(timestamp, prefix)` — only return alive files

**Level 4 — State Management:**
- `ROLLBACK(timestamp)` — restore state to earlier time, recalculate TTLs

### Available Libraries (pre-imported)
```python
import sortedcontainers  # SortedList, SortedDict
import numpy
from collections import OrderedDict
```

### Key Patterns to Practice
1. Dict-based storage with metadata (size, timestamp, ttl)
2. Sorting with custom keys: `sorted(items, key=lambda x: (-x.size, x.name))`
3. TTL/expiration checks: `current_time < upload_time + ttl`
4. State snapshots for rollback
