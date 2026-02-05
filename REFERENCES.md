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

**Location:** `/home/charlie/practice/example_tests/CodeSignal_Practice_Industry_Coding_Framework/`

### File Storage System (4 levels, 32 tests)

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

---

## LibreSignal Practice Framework

**Location:** `/home/charlie/practice/example_tests/LibreSignal/`

### Why LibreSignal is More Realistic
| Feature | My ICA-001 | LibreSignal |
|---------|------------|-------------|
| Timestamps in operations | No | Yes (every operation) |
| Scheduled future events | No | Yes (cashback at t+24hrs) |
| Historical queries | No | Yes (`get_balance(ts, time_at)`) |
| Output formatting | Simple | Complex (`"account1(500)"`) |
| State restoration | Simple snapshot | TTL recalculation required |

### LibreSignal Problem Patterns

**Bank System (4 levels):**
1. L1: `create_account`, `deposit`, `transfer` — basic CRUD
2. L2: `top_spenders` — ranking with formatted output
3. L3: `pay`, `get_payment_status` — cashback at future timestamp
4. L4: `merge_accounts`, `get_balance` — merge state, historical balance

**In-Memory Database (4 levels):**
1. L1: `set`, `get`, `delete` — key→field→value storage
2. L2: `scan`, `scan_by_prefix` — formatted output `"field(value)"`
3. L3: `*_at`, `*_at_with_ttl` — TTL per field (not per record)
4. L4: `backup`, `restore` — snapshot with remaining TTL, recalculate on restore

### L4 Difficulty: State Management

**Common L4 patterns requiring special care:**
1. **Backup/Restore**: Must use `copy.deepcopy()`, not reference assignment
2. **TTL Recalculation**: Store remaining TTL, recalculate `new_expiry = restore_time + remaining`
3. **Historical Queries**: Track state over time, not just current state
4. **Merge Operations**: Redirect references (payments, cashbacks) to merged account

### Test Format
```bash
cd /home/charlie/practice/example_tests/LibreSignal
pytest Questions/bank_system/test_bank_system.py::TestLevel1 -v
pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel1 -v
```

---

## File Storage System (CodeSignal Practice)

**Location:** `/home/charlie/practice/example_tests/CodeSignal_Practice_Industry_Coding_Framework/practice_assessments/file_storage/`

### Problem Structure
**Level 1 — Basic CRUD (8 tests):**
- `FILE_UPLOAD(file_name, size)` → `"uploaded {file_name}"`, error if exists
- `FILE_GET(file_name)` → `"got {file_name}"` or `"file not found"`
- `FILE_COPY(source, dest)` → `"copied {source} to {dest}"`, overwrites dest

**Level 2 — Search (7 tests):**
- `FILE_SEARCH(prefix)` → `"found [{file1}, {file2}, ...]"`
  - Sorted by size descending, then name ascending
  - Maximum 10 results

**Level 3 — Timestamps & TTL (8 tests):**
- `FILE_UPLOAD_AT(timestamp, file_name, size, ttl?)` → `"uploaded at {file_name}"`
- `FILE_GET_AT(timestamp, file_name)` → `"got at {file_name}"` or `"file not found"`
- `FILE_COPY_AT(timestamp, source, dest)` → `"copied at {source} to {dest}"`
- `FILE_SEARCH_AT(timestamp, prefix)` → `"found at [{file1}, ...]"`
- TTL: File available during `[timestamp, timestamp + ttl)`

**Level 4 — Rollback (5 tests):**
- `ROLLBACK(timestamp)` → `"rollback to {timestamp}"`
  - Restores state to given timestamp
  - Discards operations after rollback point
  - Recalculates TTLs based on new timeline

### Test Format
```bash
cd /home/charlie/practice/example_tests/CodeSignal_Practice_Industry_Coding_Framework/practice_assessments/file_storage
pytest test_simulation.py -v
pytest test_simulation.py::TestLevel1 -v
pytest test_simulation.py::TestLevel2 -v
pytest test_simulation.py::TestLevel3 -v
pytest test_simulation.py::TestLevel4 -v
```
