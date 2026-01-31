# PS-05: Data Structures

**Target Time:** 45-60 minutes for all 5 problems
**Priority:** Correctness → Speed. Don't worry about elegance.

---

## Workflow

1. Write code in `solution.py`
2. Run tests:
   ```bash
   cd /home/charlie/practice/problem_sets/ps_05_data_structures
   pytest test_data_structures.py -v
   pytest test_data_structures.py -v -k "stack"
   pytest test_data_structures.py --pdb -x
   ```

---

## Relevant Techniques

**Stack (LIFO):**
```python
stack = []
stack.append(x)    # Push
stack.pop()        # Pop (returns top)
stack[-1]          # Peek
```

**Queue (FIFO) with deque:**
```python
from collections import deque
q = deque()
q.append(x)        # Enqueue (right)
q.popleft()        # Dequeue (left)
q[0]               # Peek front
```

**Sorted insertion with bisect:**
```python
import bisect
arr = [1, 3, 5]
bisect.insort(arr, 4)  # arr becomes [1, 3, 4, 5]
bisect.bisect_left(arr, 3)  # Returns index 1
```

**Linked list node:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

---

## Problems

### 1. valid_parentheses(s: str) -> bool
Check if string of `()[]{}` has valid matching pairs.

```
"()" → True
"()[]{}" → True
"(]" → False
"([)]" → False
"{[]}" → True
```

---

### 2. MinStack (Class)
Implement a stack that supports push, pop, top, and retrieving minimum in O(1).

```python
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
ms.get_min()  → -3
ms.pop()
ms.top()      → 0
ms.get_min()  → -2
```

---

### 3. reverse_linked_list(head: ListNode) -> ListNode
Reverse a singly linked list. Return the new head.

```
1 → 2 → 3 → None  becomes  3 → 2 → 1 → None
```

---

### 4. SortedList (Class)
Implement a sorted list that maintains order on insert and supports range queries.

```python
sl = SortedList()
sl.insert(5)
sl.insert(2)
sl.insert(8)
sl.get_all()         → [2, 5, 8]
sl.count_range(3, 7) → 1  (only 5 in range)
sl.remove(5)         → True
sl.get_all()         → [2, 8]
```

---

### 5. RecentCounter (Class)
Count requests in the last 3000 milliseconds.

```python
rc = RecentCounter()
rc.ping(1)     → 1
rc.ping(100)   → 2
rc.ping(3001)  → 3
rc.ping(3002)  → 3  (request at t=1 is now outside window)
```

---

## Running Tests

```bash
pytest test_data_structures.py -v
```
