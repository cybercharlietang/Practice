# Training Plan

## Overview
- **Total Time Budget**: 40-50 hours
- **Session Formats**: Problem sets (≤1hr), Mock interviews (1hr), Assessments (90min)
- **Approach**: Cover all topics systematically, assess after each, then mock tests

---

## Phase 1: Problem Sets (Concept Building)

### PS-01: String Manipulation ✓ (2026-01-30, 1.5 hrs)
- [x] Reverse words in a sentence
- [x] Check palindrome (ignore case/spaces)
- [x] Count vowels/consonants
- [x] Interleave two strings
- [x] Compress string ("aabbb" → "a2b3")

### PS-02: Array Fundamentals ✓ (2026-01-30, 45 min)
- [x] Remove duplicates (preserve order)
- [x] Rotate array by k positions
- [x] Find missing number in 1..n
- [x] Merge two sorted arrays
- [x] Move zeros to end

### PS-03: Hash Tables & Counting ✓ (2026-01-30, 45 min)
- [x] Two sum (return indices)
- [x] Group anagrams
- [x] First unique character
- [x] Most frequent element
- [x] Check if two strings are anagrams

### PS-04: Sliding Window ✓ (2026-01-30, 90 min)
- [x] Maximum sum of k consecutive elements
- [x] Longest substring without repeating chars
- [x] Minimum window substring (simplified)
- [x] Count subarrays with sum = k
- [x] Sliding window maximum (using deque)

### PS-05: Data Structures ✓ (2026-02-01)
- [x] Stack operations (validate parentheses, min stack)
- [x] Sorted set with bisect (insertion, range queries)
- [x] RecentCounter (sliding window)
- [ ] Linked list basics (reverse) — skipped

### PS-06: Class Design (Q3 Simulation) ✓ (2026-02-01)
- [x] Counter class with statistics
- [x] LRU Cache
- [x] Rate Limiter
- [x] Todo Manager with priorities
- [x] Event Scheduler with conflicts

### PS-07: L4 State Management Patterns ✓ (2026-02-02)
- [x] Exercise 1: Trace scenario by hand
- [x] Exercise 2: Snapshot Manager (deepcopy discipline)
- [x] Exercise 2B: Backup/Restore with TTL (the hard pattern)
- [x] Exercise 3: TTL Calculator (formula practice)
- [x] Exercise 4: Rollback Engine (all patterns combined)
- [ ] Exercise 5: Edge cases (skipped - optional)

### ~~PS-08 to PS-10: SKIPPED~~
*Binary search, heaps, intervals, graphs — not needed for ICA*

---

## Phase 2: Mock Assessments (Timed)

### Custom Assessments (mock_assessments/)
| # | Title | Levels | Focus | Status |
|---|-------|--------|-------|--------|
| ICA-001 | Notification System | 4 | CRUD, search/stats, TTL, **backup/restore with TTL recalc** | Ready (39 tests) |

### LibreSignal Assessments (example_tests/LibreSignal/)
| # | Title | Levels | Focus | Result |
|---|-------|--------|-------|--------|
| Bank System | bank_system | 4 | CRUD, top_spenders, cashback, merge, balance history | **19/21 (90%)** ✓ |
| In-Memory DB | in_memory_database | 4 | CRUD, scan, TTL per field, backup/restore | **33/39 (85%)** ✓ |

*Note: LibreSignal format more realistic — timestamps in all operations, scheduled events, historical queries*

### CodeSignal Practice Framework (example_tests/CodeSignal_Practice_Industry_Coding_Framework/)
| # | Title | Levels | Focus | Status |
|---|-------|--------|-------|--------|
| File Storage | file_storage | 4 | CRUD, prefix search, timestamps/TTL, rollback | Ready (32 tests) |

---

## Progress Tracking

### Current Phase: Phase 2 (Mock Assessments)
- [x] Complete PS-01 to PS-06 (concept building)
- [x] Assess timing and accuracy
- [x] Take LibreSignal Bank System — 90 min, 19/21 (90%)
- [x] Take LibreSignal In-Memory DB — 90 min, 33/39 (85%)
- [x] Review L4 patterns: deepcopy, TTL recalculation, state restoration (PS-07 completed)
- [ ] Take ICA-001 (revised) — 90 min timed

### Completion Criteria
- Problem sets: 80%+ first-try accuracy, reasonable speed ✓
- Mock assessments: Complete L1-L3 within 60 min, L4 attempted ✓
- **New target**: L4 patterns (backup/restore, historical queries) need more practice

---

## Session Log
| Date | Activity | Duration | Notes |
|------|----------|----------|-------|
| 2026-01-30 | PS-01 Strings | 1.5 hrs | 28/28 passed, difficulty "about right", speed needs work |
| 2026-01-30 | PS-02 Arrays | 45 min | 32/32 passed, hit target time, review mutation vs copy |
| 2026-01-30 | PS-03 Hash Tables | 45 min | 27/27 passed, learned Counter/defaultdict |
| 2026-01-30 | PS-04 Sliding Window | 90 min | 30/30 passed, solutions correct but suboptimal complexity |
| 2026-02-01 | PS-05 Data Structures | — | 19/19 passed (linked list skipped), learned stack, bisect |
| 2026-02-01 | PS-06 Class Design | — | 26/26 passed, Q3-style problems, found test bug |
| 2026-02-02 | LibreSignal Bank | 90 min | 19/21 (90%), L1-L3 perfect, L4: cashback timing, get_balance incomplete |
| 2026-02-02 | LibreSignal InMemDB | 90 min | 33/39 (85%), L1-L3 perfect, L4: reference vs copy, TTL recalc |
