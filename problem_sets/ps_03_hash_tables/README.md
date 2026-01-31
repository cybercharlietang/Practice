# PS-03: Hash Tables & Counting

**Target Time:** 30-45 minutes for all 5 problems
**Goal:** Master dict/set patterns for O(1) lookups and counting

---

## Problems

### 1. two_sum(nums: list, target: int) -> list
Find two indices whose values add up to target. Return [i, j] where i < j.
Assume exactly one solution exists.

```
[2, 7, 11, 15], target=9 → [0, 1]  (2 + 7 = 9)
[3, 2, 4], target=6 → [1, 2]  (2 + 4 = 6)
[3, 3], target=6 → [0, 1]
```

---

### 2. group_anagrams(strs: list) -> list
Group strings that are anagrams of each other. Return list of groups (order doesn't matter).

```
["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"], ["tan","nat"], ["bat"]]
[""] → [[""]]
["a"] → [["a"]]
```

---

### 3. first_unique_char(s: str) -> int
Return index of first non-repeating character. Return -1 if none exists.

```
"leetcode" → 0  ('l' is first unique)
"loveleetcode" → 2  ('v' is first unique)
"aabb" → -1
"" → -1
```

---

### 4. most_frequent(nums: list) -> int
Return the element that appears most frequently. If tie, return any of them.

```
[1, 3, 2, 1, 4, 1] → 1
[1, 2, 2, 3, 3] → 2 or 3  (either valid)
[5] → 5
```

---

### 5. is_anagram(s1: str, s2: str) -> bool
Check if two strings are anagrams (same characters, same counts).

```
"anagram", "nagaram" → True
"rat", "car" → False
"listen", "silent" → True
"", "" → True
```

---

## Running Tests

```bash
cd problem_sets/ps_03_hash_tables
pytest test_hash_tables.py -v
```

Run tests for a specific function:
```bash
pytest test_hash_tables.py -v -k "two_sum"
```
