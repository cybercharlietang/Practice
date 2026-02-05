# Strengths & Weaknesses

## Current Assessment
*Updated after file_storage assessment (2026-02-02)*

## Strengths
- Basic string operations: `split()`, `join()`, slicing (`[::-1]`)
- Loop logic and index tracking
- Edge case handling (empty strings, unequal lengths)
- Set operations for deduplication and lookups
- Quick to learn new tools: Counter, defaultdict, deque, bisect, datetime
- Gets correct answers — all problem sets 100% pass rate
- **Class design**: Good at structuring state, dict with metadata pattern
- **L1-L3 consistency**: Perfect on CRUD, search/filter, TTL expiration across ALL mock assessments
- **Formatted output**: Handles custom output formats like `"found [x, y]"`, `"field(value)"` correctly
- **Sorting with multiple keys**: `sorted(items, key=lambda x: (-x[1], x[0]))`
- **TTL logic**: Understands `[timestamp, timestamp + ttl)` interval checking
- **Debugging persistence**: Works through errors systematically, asks clarifying questions
- **Critical thinking**: Questions test correctness when logic doesn't match (file_storage L4 test bug)

## Weaknesses

### L4 State Management (Primary Focus Area)
- **Reference vs copy (CRITICAL)**: `self.backup = self.data` stores reference — always use `copy.deepcopy()`
- **Condition inversion**: Writing `<` when meaning `>` (e.g., remove files AFTER rollback, not before)
- **Control flow after mutations**: Accessing `dict[key]` after `dict.pop(key)` — need else clause
- **TTL recalculation**: Formula confusion — remaining = original_ttl - elapsed, keep as int not string
- **None checks**: Must check `if ttl is not None` before `timedelta(seconds=ttl)`

### Datetime Arithmetic
- **Operator precedence**: `datetime(...).total_seconds()` vs `(datetime - datetime).total_seconds()`
- **timedelta vs datetime**: Only timedelta has `.total_seconds()`, not datetime objects

### Other
- **Variable shadowing**: Loop variable `for key in dict` overwrites function parameter `key`
- **Incomplete implementations**: Sometimes returns early without finishing edge cases

*Note: Runtime complexity is NOT a priority for CodeSignal — correctness and speed matter*

## Known Issues (from previous attempt)
- Environment unfamiliarity caused issues during real test
- Got stuck on Q2, didn't pass it

## Session History
| Date | Session Type | Topics | Performance | Notes |
|------|--------------|--------|-------------|-------|
| 2026-01-30 | PS-01 Strings | reverse, palindrome, vowels, interleave, compress | 28/28 tests passed | 1.5 hrs, difficulty "about right" |
| 2026-01-30 | PS-02 Arrays | dedup, rotate, missing, merge, move_zeros | 32/32 tests passed | 45 min, speed improved |
| 2026-01-30 | PS-03 Hash Tables | two_sum, anagrams, first_unique, most_freq | 27/27 tests passed | 45 min, learned Counter/defaultdict |
| 2026-01-30 | PS-04 Sliding Window | max_sum, unique_substr, min_window, subarray_sum, window_max | 30/30 tests passed | 90 min, correct but O(n²/n³) solutions |
| 2026-02-01 | PS-05 Data Structures | valid_parentheses, MinStack, SortedList, RecentCounter | 19/19 passed (skipped linked list) | Learned stack pattern, bisect |
| 2026-02-01 | PS-06 Class Design | Counter, LRUCache, RateLimiter, TodoManager, EventScheduler | 26/26 tests passed | Good class design, caught test bug |
| 2026-02-02 | LibreSignal Bank | CRUD, top_spenders, pay/cashback, merge, get_balance | 19/21 (90%) | L1-L3 perfect, L4 cashback timing + get_balance incomplete |
| 2026-02-02 | LibreSignal InMemDB | CRUD, scan, TTL, backup/restore | 33/39 (85%) | L1-L3 perfect, L4 deepcopy + TTL recalc issues |
| 2026-02-02 | File Storage | CRUD, search, TTL, rollback | 32/32 (100%)* | L1-L3 perfect, L4 needed debugging (condition inversion, control flow, None check) |
| 2026-02-02 | PS-07 L4 Patterns | backup/restore, TTL recalc, rollback | 28/32 (88%) | Exercises 1-4 perfect, Ex 5 (edge cases) skipped |

*Note: File Storage L4 required guidance to fix bugs; test had incorrect expectations that were corrected
