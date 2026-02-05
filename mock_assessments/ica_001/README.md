# ICA-001: Notification System

## Overview
Implement a notification management system that handles user notifications with expiration and state management.

**Time Limit:** 90 minutes
**Tests:** 39 total across 4 levels

## How to Run Tests

```bash
cd /home/charlie/practice/mock_assessments/ica_001

# Run all tests
pytest tests/ -v

# Run specific level
pytest tests/test_level1.py -v
pytest tests/test_level2.py -v
pytest tests/test_level3.py -v
pytest tests/test_level4.py -v
```

## Problem Description

Build a `NotificationSystem` class that manages notifications for users.

---

## Level 1: Basic Operations (10 tests)

Implement basic CRUD operations for notifications.

| Method | Description | Returns |
|--------|-------------|---------|
| `add_notification(user_id, message)` | Create notification | `"notification_id"` (auto-generated: "notif_1", "notif_2", ...) |
| `get_notification(notification_id)` | Get message by ID | `"message"` or `None` if not found |
| `delete_notification(notification_id)` | Delete notification | `True` if deleted, `False` if not found |
| `list_user_notifications(user_id)` | Get all notification IDs for user | `["notif_1", "notif_3"]` sorted by creation order |

**Notes:**
- Notification IDs are auto-generated: "notif_1", "notif_2", etc. (sequential)
- Each notification belongs to exactly one user

---

## Level 2: Search & Statistics (10 tests)

Add search functionality and user statistics.

| Method | Description | Returns |
|--------|-------------|---------|
| `search_notifications(prefix)` | Find notifications where message starts with prefix | `["notif_id: message", ...]` sorted by ID |
| `get_user_stats(user_id)` | Get notification count for user | `"user_id(count)"` e.g. `"alice(5)"` |
| `get_top_users(n)` | Top n users by notification count | `["user1(count1)", "user2(count2)", ...]` sorted by count desc, then user_id asc |

**Notes:**
- `search_notifications("")` with empty prefix returns ALL notifications
- `get_top_users(n)` returns at most n users
- Tie-breaking: higher count first, then alphabetically by user_id

---

## Level 3: Timestamps & TTL (10 tests)

Add timestamp-aware operations with optional TTL (time-to-live).

| Method | Description | Returns |
|--------|-------------|---------|
| `add_notification_at(timestamp, user_id, message, ttl=None)` | Create with timestamp and optional TTL | `"notif_id"` |
| `get_notification_at(timestamp, notification_id)` | Get if exists and not expired | `"message"` or `None` |
| `list_user_notifications_at(timestamp, user_id)` | List non-expired notifications | `["notif_1", ...]` |
| `search_notifications_at(timestamp, prefix)` | Search non-expired notifications | `["notif_id: message", ...]` |

**Notes:**
- `ttl` is in seconds. `None` means permanent (never expires)
- Notification is available during `[upload_time, upload_time + ttl)`
- At exactly `upload_time + ttl`, the notification is expired

---

## Level 4: Backup & Restore (10 tests)

Add state snapshot and restoration with TTL recalculation.

| Method | Description | Returns |
|--------|-------------|---------|
| `backup(timestamp, backup_id)` | Create snapshot of current state | `"backup backup_id created"` |
| `restore(timestamp, backup_id)` | Restore from snapshot | `"restored from backup_id"` or `"backup not found"` |

**CRITICAL - TTL Recalculation:**
- At backup time: store **remaining TTL** (not absolute expiry)
- At restore time: recalculate new expiry = `restore_time + remaining_ttl`

**Example:**
```
10:00  add_notification_at("alice", "msg", ttl=600)  # expires 10:10
10:03  backup("snap1")                               # remaining = 420 sec (7 min)
10:08  restore("snap1")                              # new expiry = 10:08 + 420 = 10:15
```

**Notes:**
- Backup must use deep copy (changes after backup don't affect it)
- Restore must use deep copy (changes after restore don't affect the backup)
- Notifications created AFTER backup time should NOT be in the backup

---

## Implementation File

Edit `simulation.py` to implement the `NotificationSystem` class.

## Scoring

Each level has 10 tests. Partial credit is given for passing tests.

| Level | Tests | Focus |
|-------|-------|-------|
| 1 | 10 | Basic CRUD |
| 2 | 10 | Search, formatted output |
| 3 | 10 | Timestamps, TTL expiration |
| 4 | 10 | Backup/restore, TTL recalculation |
