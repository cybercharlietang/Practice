# Strengths & Weaknesses

## Current Assessment
*Updated after PS-01 (2026-01-30)*

## Strengths
- Basic string operations: `split()`, `join()`, slicing (`[::-1]`)
- Loop logic and index tracking
- Edge case handling (empty strings, unequal lengths)
- Understands core algorithms once explained (RLE, interleaving)
- Set operations for deduplication and lookups
- Modulo arithmetic for wrap-around (rotate)
- Speed on target for basic problems (45 min for PS-02, PS-03)
- Quick to learn new tools: Counter, defaultdict, deque
- Gets correct answers — all problem sets 100% pass rate

## Weaknesses
- **Higher-order functions**: Confuses `filter(fn)` vs `filter(fn())` — passing function object vs calling it
- **Similar operation distinction**: Mixed up word reversal vs character reversal
- **Type awareness**: `int(set)` doesn't extract element — need `.pop()` or iteration
- **Mutation vs copy**: `l = arr` creates reference, not copy — mutates original (DRILLED)
- **Iteration safety**: Modifying list while iterating is undefined behavior (DRILLED)
- **Hashable types**: Initially tried using list as dict key
- **Class design**: Not yet tested — need practice with multi-class problems
- **Debugging speed**: Need to practice pytest/pdb workflow

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
