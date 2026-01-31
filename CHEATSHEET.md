# Cheatsheet

## Pytest Commands

```bash
pytest test_file.py -v              # Verbose output
pytest test_file.py -k "test_name"  # Run specific test
pytest test_file.py -x              # Stop on first failure
pytest test_file.py --pdb           # Drop into debugger on failure
pytest test_file.py -s              # Show print statements
```

## PDB Debugging

```python
import pdb; pdb.set_trace()  # Add breakpoint in code
```

In pdb:
```
n       # Next line
s       # Step into function
c       # Continue to next breakpoint
p var   # Print variable
l       # List code around current line
q       # Quit debugger
```

## Code Shortcuts

```python
# String <-> List
"".join(lst)                    # ['a','b','c'] → "abc"
list(s)                         # "abc" → ['a','b','c']
s.split(" ")                    # "a b c" → ['a','b','c']

# List comprehension
[x for x in lst if condition]   # Filter
[f(x) for x in lst]             # Transform

# Counting
from collections import Counter
Counter("aab")                  # {'a': 2, 'b': 1}
counter.most_common(1)[0][0]    # Most frequent element

# Grouping
from collections import defaultdict
d = defaultdict(list)
d[key].append(val)              # Auto-creates empty list

# Safe dict access
d.get(key, 0)                   # Returns 0 if missing (no KeyError)

# Sorting
sorted(lst, key=lambda x: x[1])           # Sort by second element
sorted(lst, key=lambda x: (-x[1], x[0]))  # Descending first, then ascending

# Reverse
s[::-1]                         # Reverse string/list
lst.reverse()                   # In-place reverse
```

## Patterns

**Two Sum (complement lookup):**
```python
seen = {}
for i, num in enumerate(nums):
    if target - num in seen:
        return [seen[target - num], i]
    seen[num] = i
```

**Sliding Window (fixed size):**
```python
window_sum = sum(nums[:k])
for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]  # Add new, remove old
```

**Sliding Window (variable size):**
```python
left = 0
for right in range(len(s)):
    # Add s[right] to window
    while window_invalid:
        # Remove s[left] from window
        left += 1
```

**Prefix Sum Count:**
```python
seen = {0: 1}
prefix = 0
for num in nums:
    prefix += num
    count += seen.get(prefix - k, 0)
    seen[prefix] = seen.get(prefix, 0) + 1
```

## Gotchas

```python
# Copy vs reference
b = a        # Reference (same object)
b = a[:]     # Shallow copy (new list)
b = a.copy() # Shallow copy

# Never modify list while iterating
for x in lst:
    lst.remove(x)  # BAD - skips elements

# Dict keys must be hashable
d[sorted(s)]              # ERROR - list not hashable
d[tuple(sorted(s))]       # OK
d[''.join(sorted(s))]     # OK
```
