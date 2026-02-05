# PS-07: L4 State Management Patterns

## Focus Areas
This problem set targets the specific L4 weaknesses identified from mock assessments:

| Pattern | Your Bug | Correct Pattern |
|---------|----------|-----------------|
| Condition logic | `if upload_time < rollback` (removes old) | `if upload_time > rollback` (removes new) |
| Control flow | Access dict after pop → crash | Use `else` clause for kept items |
| Deep copy | `backup = self.data` (reference) | `backup = copy.deepcopy(self.data)` |
| TTL recalculation | `str(timedelta(...))` | `remaining = original_ttl - elapsed` (int) |
| None checks | `timedelta(seconds=None)` → TypeError | `if ttl is not None:` first |

## Exercises

| Exercise | Focus | Tests | Priority |
|----------|-------|-------|----------|
| 1 | Trace by hand FIRST | 1 | Start here |
| 2 | Deep copy basics | 5 | Warm-up |
| **2B** | **Backup/Restore + TTL** | **9** | **YOUR WEAKNESS** |
| 3 | TTL formula isolation | 6 | Foundation |
| 4 | All patterns combined | 7 | Integration |
| 5 | Edge cases | 4 | Polish |

### Exercise 1: Trace Before Code
Before implementing, trace through scenarios BY HAND. Write down the expected state after each operation.

### Exercise 2: Snapshot Manager (Simple)
Basic backup/restore with deep copy discipline. No TTL.

### Exercise 2B: Backup/Restore WITH TTL (THE HARD ONE)
**This is the exact pattern that caused your bugs.**

The tricky part:
- At backup: store REMAINING TTL (not absolute expiry)
- At restore: calculate NEW expiry = restore_time + remaining_ttl

```
10:00  set("temp", ttl=600)     # expires at 10:10
10:03  backup("snap1")          # remaining = 600 - 180 = 420 sec
10:08  restore("snap1")         # new expiry = 10:08 + 420sec = 10:15
```

### Exercise 3: TTL Calculator
Practice the TTL recalculation formula in isolation.

### Exercise 4: Rollback Engine
Combine all patterns: condition logic, control flow, TTL recalc, None checks.

### Exercise 5: Edge Cases
Handle the tricky scenarios that break L4 implementations.

## How to Run
```bash
cd /home/charlie/practice/problem_sets/ps_07_L4_patterns
pytest test_L4_patterns.py -v
pytest test_L4_patterns.py::TestExercise1 -v  # Run specific exercise
```

## Key Formulas

**TTL Recalculation:**
```python
elapsed = (rollback_time - upload_time).total_seconds()
remaining = original_ttl - elapsed  # Keep as int/float!
```

**Rollback Condition:**
```python
if upload_time > rollback_time:
    remove(file)  # Created AFTER rollback point
else:
    keep(file)    # Existed at rollback point
```

**Deep Copy:**
```python
import copy
self.snapshots[ts] = copy.deepcopy(self.data)  # Always deepcopy for snapshots
```

**Backup with TTL (store remaining):**
```python
def backup(self, timestamp, backup_id):
    backup_data = {}
    for key, item in self.data.items():
        if item["ttl"] is not None:
            elapsed = (timestamp - item["upload_time"]).total_seconds()
            remaining = item["ttl"] - elapsed
            if remaining > 0:
                backup_data[key] = {"value": item["value"], "remaining_ttl": remaining}
        else:
            backup_data[key] = {"value": item["value"], "remaining_ttl": None}
    self.backups[backup_id] = copy.deepcopy(backup_data)
```

**Restore with TTL (recalculate expiry):**
```python
def restore(self, timestamp, backup_id):
    backup = self.backups[backup_id]
    self.data = {}
    for key, item in copy.deepcopy(backup).items():
        self.data[key] = {
            "value": item["value"],
            "upload_time": timestamp,  # Reset to restore time!
            "ttl": item["remaining_ttl"]  # Remaining becomes new TTL
        }
```
