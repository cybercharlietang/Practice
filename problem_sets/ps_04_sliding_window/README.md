# PS-04: Sliding Window

**Target Time:** 30-45 minutes for all 5 problems
**Goal:** Master the sliding window pattern for subarray/substring problems

---

## Core Concept

A sliding window maintains a range `[left, right]` that expands or contracts based on conditions. Two main types:

1. **Fixed-size window:** Window size is constant (e.g., "sum of k elements")
2. **Variable-size window:** Window grows/shrinks based on constraints (e.g., "longest without repeats")

---

## Problems

### 1. max_sum_k(nums: list, k: int) -> int
Find maximum sum of k consecutive elements. Return 0 if array has fewer than k elements.

```
[1, 4, 2, 10, 2, 3, 1, 0, 20], k=4 → 24  (subarray [2, 10, 2, 10] wait no... [10, 2, 3, 1]? Let me recalc: [4,2,10,2]=18, [2,10,2,3]=17, [10,2,3,1]=16, [2,3,1,0]=6, [3,1,0,20]=24 ✓)
[1, 2, 3], k=2 → 5  (2 + 3)
[5], k=2 → 0  (not enough elements)
```

---

### 2. longest_unique_substring(s: str) -> int
Find length of longest substring without repeating characters.

```
"abcabcbb" → 3  ("abc")
"bbbbb" → 1  ("b")
"pwwkew" → 3  ("wke")
"" → 0
```

---

### 3. min_window_substring(s: str, t: str) -> str
Find minimum window in s that contains all characters of t. Return "" if no such window.

```
"ADOBECODEBANC", "ABC" → "BANC"
"a", "a" → "a"
"a", "aa" → ""  (not enough 'a's)
```

---

### 4. subarray_sum_count(nums: list, k: int) -> int
Count number of contiguous subarrays that sum to exactly k.

```
[1, 1, 1], k=2 → 2  ([1,1] at index 0-1 and 1-2)
[1, 2, 3], k=3 → 2  ([1,2] and [3])
[1, -1, 0], k=0 → 3  ([1,-1], [-1,0,1]... wait: [1,-1], [0], [1,-1,0])
```

---

### 5. sliding_window_max(nums: list, k: int) -> list
Return max element in each window of size k. Use deque for O(n) solution.

```
[1, 3, -1, -3, 5, 3, 6, 7], k=3 → [3, 3, 5, 5, 6, 7]
[1], k=1 → [1]
[1, 2, 3, 4], k=2 → [2, 3, 4]
```

---

## Running Tests

```bash
cd problem_sets/ps_04_sliding_window
pytest test_sliding_window.py -v
```

Run tests for a specific function:
```bash
pytest test_sliding_window.py -v -k "max_sum"
```
