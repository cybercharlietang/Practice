# Practice Progressive Filesystem Question (Integer Container)

**Time Limit:** 90 minutes  
**Execution Time Limit:** 3 seconds per test  
**Memory Limit:** 4g

---

## Instructions

Welcome to the practice task! This task is designed to be a playground that allows you to get acquainted with the testing environment and practice the functionalities of the platform before your real assessment.

Your task is to **implement a simple container of integer numbers**. All operations that should be supported by this database are described below.

Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly solved. You always have access to the data for the current and all previous levels.

You are not required to provide the most efficient implementation. Any code that passes the unit tests is sufficient.

---

## Requirements

Your task is to implement a simple container of integer numbers. Plan your design according to the level specifications below:

- **Level 1:** Container should support adding and removing numbers.
- **Level 2:** Container should support getting the median of the numbers stored in it.

To move to the next level, you need to pass all the tests at this level when submitting the solution.

---

## Level 1

Implement two operations for adding and removing numbers from the container. Initially, the container is empty.

- `add(self, value: int) -> int` — should add the specified integer `value` to the container and return the number of integers in the container after the addition.

- `delete(self, value: int) -> bool` — should attempt to remove the specified integer `value` from the container. If the `value` is present in the container, remove it and return `True`, otherwise, return `False`.

### Examples

| Queries | Explanations |
|---------|--------------|
| `add(5)` | returns `1`; container state: `[5]` |
| `add(10)` | returns `2`; container state: `[5, 10]` |
| `add(5)` | returns `3`; container state: `[5, 10, 5]` |
| `delete(10)` | returns `True`; container state: `[5, 5]` |
| `delete(1)` | returns `False`; container state: `[5, 5]` |
| `add(1)` | returns `3`; container state: `[5, 5, 1]` |

---

## Level 2

Implement an operation for getting the median of the numbers stored in the container.

- `get_median(self) -> float` — should return the median of all integers currently in the container. If there is an even number of elements, return the average of the two middle elements. If the container is empty, return `-1`.

### Examples

| Queries | Explanations |
|---------|--------------|
| `add(5)` | returns `1`; container state: `[5]` |
| `add(10)` | returns `2`; container state: `[5, 10]` |
| `get_median()` | returns `7.5`; median of `[5, 10]` |
| `add(3)` | returns `3`; container state: `[5, 10, 3]` |
| `get_median()` | returns `5.0`; median of sorted `[3, 5, 10]` |
| `delete(5)` | returns `True`; container state: `[10, 3]` |
| `get_median()` | returns `6.5`; median of `[3, 10]` |
| `get_median()` on empty | returns `-1` |

---

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific level
python -m pytest tests/level_1_tests.py -v
python -m pytest tests/level_2_tests.py -v

# Run sandbox tests (your custom tests)
python -m pytest sandbox_tests.py -v

# Run a single test
python -m pytest tests/level_1_tests.py::TestLevel1::test_add_single -v
```

---

## Files

| File | Description |
|------|-------------|
| `integer_container.py` | Abstract base class (DO NOT MODIFY) |
| `integer_container_impl.py` | Your implementation (EDIT THIS) |
| `tests/level_1_tests.py` | Level 1 tests (DO NOT MODIFY) |
| `tests/level_2_tests.py` | Level 2 tests (DO NOT MODIFY) |
| `sandbox_tests.py` | Your custom tests (feel free to modify) |
