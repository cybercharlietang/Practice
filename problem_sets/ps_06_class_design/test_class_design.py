"""
PS-06: Class Design Tests
"""
import unittest
from solution import Counter, LRUCache, RateLimiter, TodoManager, EventScheduler


class TestCounter(unittest.TestCase):

    def test_increment_basic(self):
        c = Counter()
        self.assertEqual(c.increment(), 1)
        self.assertEqual(c.increment(), 2)
        self.assertEqual(c.increment(5), 7)

    def test_decrement_basic(self):
        c = Counter()
        c.increment(10)
        self.assertEqual(c.decrement(), 9)
        self.assertEqual(c.decrement(5), 4)

    def test_get_value(self):
        c = Counter()
        self.assertEqual(c.get_value(), 0)
        c.increment(5)
        c.decrement(2)
        self.assertEqual(c.get_value(), 3)

    def test_stats(self):
        c = Counter()
        c.increment(10)
        c.decrement(3)
        c.increment(5)
        stats = c.get_stats()
        self.assertEqual(stats["total_increments"], 2)
        self.assertEqual(stats["total_decrements"], 1)
        self.assertEqual(stats["max_value"], 12)
        self.assertEqual(stats["min_value"], 0)

    def test_reset(self):
        c = Counter()
        c.increment(10)
        c.reset()
        self.assertEqual(c.get_value(), 0)
        stats = c.get_stats()
        self.assertEqual(stats["total_increments"], 1)  # Stats preserved


class TestLRUCache(unittest.TestCase):

    def test_get_put_basic(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), -1)

    def test_eviction(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # Evicts "a"
        self.assertEqual(cache.get("a"), -1)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)

    def test_access_updates_recency(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # "a" is now most recent
        cache.put("c", 3)  # Evicts "b", not "a"
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), -1)

    def test_update_existing(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)  # Update, "a" becomes most recent
        cache.put("c", 3)  # Evicts "b"
        self.assertEqual(cache.get("a"), 10)
        self.assertEqual(cache.get("b"), -1)

    def test_size(self):
        cache = LRUCache(3)
        self.assertEqual(cache.size(), 0)
        cache.put("a", 1)
        self.assertEqual(cache.size(), 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.size(), 3)
        cache.put("d", 4)  # Eviction
        self.assertEqual(cache.size(), 3)


class TestRateLimiter(unittest.TestCase):

    def test_allow_within_limit(self):
        rl = RateLimiter(3, 10)  # 3 requests per 10 seconds
        self.assertTrue(rl.allow_request(1))
        self.assertTrue(rl.allow_request(2))
        self.assertTrue(rl.allow_request(3))

    def test_block_over_limit(self):
        rl = RateLimiter(3, 10)
        self.assertTrue(rl.allow_request(1))
        self.assertTrue(rl.allow_request(2))
        self.assertTrue(rl.allow_request(3))
        self.assertFalse(rl.allow_request(4))  # Blocked

    def test_window_slides(self):
        rl = RateLimiter(2, 10)
        self.assertTrue(rl.allow_request(1))
        self.assertTrue(rl.allow_request(5))
        self.assertFalse(rl.allow_request(8))  # Blocked
        self.assertTrue(rl.allow_request(12))  # t=1 is now outside [2, 12]

    def test_get_remaining(self):
        rl = RateLimiter(5, 10)
        self.assertEqual(rl.get_remaining(1), 5)
        rl.allow_request(1)
        rl.allow_request(2)
        self.assertEqual(rl.get_remaining(5), 3)
        self.assertEqual(rl.get_remaining(15), 5)  # Window slid


class TestTodoManager(unittest.TestCase):

    def test_add_and_get(self):
        tm = TodoManager()
        self.assertTrue(tm.add_task("t1", "Buy milk", 2))
        task = tm.get_task("t1")
        self.assertEqual(task["description"], "Buy milk")
        self.assertEqual(task["priority"], 2)
        self.assertFalse(task["completed"])

    def test_add_duplicate(self):
        tm = TodoManager()
        self.assertTrue(tm.add_task("t1", "Task 1", 1))
        self.assertFalse(tm.add_task("t1", "Duplicate", 2))

    def test_complete_task(self):
        tm = TodoManager()
        tm.add_task("t1", "Task 1", 1)
        self.assertTrue(tm.complete_task("t1"))
        self.assertTrue(tm.get_task("t1")["completed"])
        self.assertFalse(tm.complete_task("t1"))  # Already complete
        self.assertFalse(tm.complete_task("t2"))  # Not found

    def test_get_pending_sorted(self):
        tm = TodoManager()
        tm.add_task("c", "Task C", 2)
        tm.add_task("a", "Task A", 1)
        tm.add_task("b", "Task B", 1)
        tm.add_task("d", "Task D", 3)
        tm.complete_task("b")
        # Pending: a(p1), c(p2), d(p3) - sorted by priority then id
        self.assertEqual(tm.get_pending(), ["a", "c", "d"])

    def test_get_by_priority(self):
        tm = TodoManager()
        tm.add_task("t1", "Task 1", 1)
        tm.add_task("t2", "Task 2", 2)
        tm.add_task("t3", "Task 3", 1)
        self.assertEqual(tm.get_by_priority(1), ["t1", "t3"])
        self.assertEqual(tm.get_by_priority(2), ["t2"])
        self.assertEqual(tm.get_by_priority(3), [])


class TestEventScheduler(unittest.TestCase):

    def test_add_and_get(self):
        es = EventScheduler()
        self.assertTrue(es.add_event("e1", 10, 20))
        event = es.get_event("e1")
        self.assertEqual(event["start"], 10)
        self.assertEqual(event["end"], 20)

    def test_add_duplicate_id(self):
        es = EventScheduler()
        self.assertTrue(es.add_event("e1", 10, 20))
        self.assertFalse(es.add_event("e1", 30, 40))

    def test_conflict_overlap(self):
        es = EventScheduler()
        es.add_event("e1", 10, 20)
        self.assertFalse(es.add_event("e2", 15, 25))  # Overlaps
        self.assertFalse(es.add_event("e3", 5, 15))   # Overlaps
        self.assertFalse(es.add_event("e4", 12, 18))  # Inside

    def test_no_conflict_adjacent(self):
        es = EventScheduler()
        es.add_event("e1", 10, 20)
        self.assertTrue(es.add_event("e2", 20, 30))  # Adjacent OK (end exclusive)
        self.assertTrue(es.add_event("e3", 5, 10))   # Adjacent OK

    def test_remove(self):
        es = EventScheduler()
        es.add_event("e1", 10, 20)
        self.assertTrue(es.remove_event("e1"))
        self.assertFalse(es.remove_event("e1"))  # Already removed
        self.assertIsNone(es.get_event("e1"))

    def test_get_events_in_range(self):
        es = EventScheduler()
        es.add_event("e1", 10, 20)
        es.add_event("e2", 25, 35)
        es.add_event("e3", 40, 50)  # No conflict with e2
        # Range [15, 45) overlaps e1, e2, e3
        self.assertEqual(es.get_events_in_range(15, 45), ["e1", "e2", "e3"])
        # Range [21, 24) overlaps nothing
        self.assertEqual(es.get_events_in_range(21, 24), [])

    def test_get_conflicts(self):
        es = EventScheduler()
        es.add_event("e1", 10, 20)
        es.add_event("e2", 25, 35)
        # Proposed [15, 30) conflicts with e1, e2
        self.assertEqual(es.get_conflicts(15, 30), ["e1", "e2"])


if __name__ == '__main__':
    unittest.main()
