# PS-02: Array Fundamentals

**Target Time:** 30-45 minutes for all 5 problems
**Goal:** Speed and accuracy on basic array operations

---

## Problems

### 1. remove_duplicates(arr: list) -> list
Remove duplicate elements while preserving original order. Return a new list.

```
[1, 2, 2, 3, 1, 4] → [1, 2, 3, 4]
[1, 1, 1] → [1]
[] → []
```

---

### 2. rotate_array(arr: list, k: int) -> list
Rotate array to the right by k positions. Return a new list.

```
[1, 2, 3, 4, 5], k=2 → [4, 5, 1, 2, 3]
[1, 2, 3], k=4 → [3, 1, 2]  (k > len, so k % len = 1)
[1], k=100 → [1]
```

---

### 3. find_missing(arr: list) -> int
Given array containing n distinct numbers from range [0, n], find the missing one.

```
[3, 0, 1] → 2  (range 0-3, missing 2)
[0, 1] → 2  (range 0-2, missing 2)
[9,6,4,2,3,5,7,0,1] → 8
[0] → 1
```

---

### 4. merge_sorted(arr1: list, arr2: list) -> list
Merge two sorted arrays into one sorted array.

```
[1, 3, 5], [2, 4, 6] → [1, 2, 3, 4, 5, 6]
[1, 2, 3], [] → [1, 2, 3]
[], [1] → [1]
[1, 1, 1], [1, 1] → [1, 1, 1, 1, 1]
```

---

### 5. move_zeros(arr: list) -> list
Move all zeros to the end while maintaining relative order of non-zero elements. Return a new list.

```
[0, 1, 0, 3, 12] → [1, 3, 12, 0, 0]
[0, 0, 1] → [1, 0, 0]
[1, 2, 3] → [1, 2, 3]
[0, 0, 0] → [0, 0, 0]
```

---

## Running Tests

```bash
cd problem_sets/ps_02_arrays
pytest test_arrays.py -v
```

Run tests for a specific function:
```bash
pytest test_arrays.py -v -k "remove_duplicates"
```
