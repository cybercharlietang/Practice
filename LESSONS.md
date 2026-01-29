# Lessons Learned

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
