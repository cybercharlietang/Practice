"""
Tests for PS-07: L4 State Management Patterns
=============================================
Run:
    pytest test_L4_patterns.py -v
    pytest test_L4_patterns.py::TestExercise1 -v
"""
import pytest
from solution import (
    trace_scenario,
    SnapshotManager,
    TTLBackupStore,
    TTLCalculator,
    RollbackEngine,
    EdgeCaseHandler
)


class TestExercise1:
    """Exercise 1: Trace Before Code"""

    def test_trace_scenario(self):
        """
        Scenario:
          10:00  upload("a.txt", ttl=600)   # 10 min TTL, expires at 10:10
          10:03  upload("b.txt", ttl=None)  # Permanent
          10:05  upload("c.txt", ttl=300)   # 5 min TTL
          10:08  rollback to 10:04

        After rollback to 10:04:
        - a.txt: uploaded 10:00 < 10:04 → KEEP, remaining TTL = 600 - 240 = 360 (6 min)
        - b.txt: uploaded 10:03 < 10:04 → KEEP, no TTL
        - c.txt: uploaded 10:05 > 10:04 → REMOVE

        After rollback, a.txt has 6 min remaining.
        New expiry = 10:08 + 6 min = 10:14
        Query at 10:15 → expired (10:15 >= 10:14)
        """
        result = trace_scenario()

        assert result is not None, "trace_scenario() returned None"
        assert set(result["files_after_rollback"]) == {"a.txt", "b.txt"}
        assert result["a_remaining_ttl"] == 360  # 6 minutes = 360 seconds
        assert result["a_alive_at_10_15"] == False  # Expired


class TestExercise2:
    """Exercise 2: Snapshot Manager - Deep Copy Discipline"""

    def test_basic_set_get(self):
        sm = SnapshotManager()
        sm.set("user1", "name", "Alice")
        assert sm.get("user1", "name") == "Alice"
        assert sm.get("user1", "age") is None
        assert sm.get("user2", "name") is None

    def test_backup_creates_independent_copy(self):
        """CRITICAL: Changes after backup should NOT affect the backup"""
        sm = SnapshotManager()
        sm.set("user1", "balance", 100)
        sm.backup("snap1")

        # Modify after backup
        sm.set("user1", "balance", 999)
        sm.set("user2", "balance", 500)

        # Restore should bring back original state
        sm.restore("snap1")
        assert sm.get("user1", "balance") == 100
        assert sm.get("user2", "balance") is None  # user2 didn't exist at snap1

    def test_restore_creates_independent_copy(self):
        """CRITICAL: Changes after restore should NOT affect the snapshot"""
        sm = SnapshotManager()
        sm.set("user1", "balance", 100)
        sm.backup("snap1")

        sm.restore("snap1")
        sm.set("user1", "balance", 999)  # Modify after restore

        # Restore again - should still be 100, not 999
        sm.restore("snap1")
        assert sm.get("user1", "balance") == 100

    def test_nested_data_deep_copy(self):
        """Nested structures must be deep copied"""
        sm = SnapshotManager()
        sm.set("config", "options", {"debug": True, "levels": [1, 2, 3]})
        sm.backup("snap1")

        # Modify nested data
        sm.data["config"]["options"]["debug"] = False
        sm.data["config"]["options"]["levels"].append(4)

        # Restore should have original nested values
        sm.restore("snap1")
        assert sm.get("config", "options") == {"debug": True, "levels": [1, 2, 3]}

    def test_restore_nonexistent_snapshot(self):
        sm = SnapshotManager()
        result = sm.restore("nonexistent")
        assert result == "snapshot not found"


class TestExercise2B:
    """Exercise 2B: Backup/Restore WITH TTL - The Hard Pattern"""

    def test_basic_set_get(self):
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "key1", "value1")
        assert store.get_at("2021-01-01T10:01:00", "key1") == "value1"

    def test_ttl_expiration(self):
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "temp", "value", ttl=300)  # 5 min
        assert store.get_at("2021-01-01T10:04:00", "temp") == "value"  # 4 min, alive
        assert store.get_at("2021-01-01T10:06:00", "temp") is None  # 6 min, dead

    def test_backup_restore_basic(self):
        """Basic backup/restore without TTL"""
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "key1", "value1")
        store.backup("2021-01-01T10:01:00", "snap1")

        store.set_at("2021-01-01T10:02:00", "key2", "value2")
        store.restore("2021-01-01T10:03:00", "snap1")

        assert store.get_at("2021-01-01T10:04:00", "key1") == "value1"
        assert store.get_at("2021-01-01T10:04:00", "key2") is None

    def test_backup_stores_remaining_ttl(self):
        """
        THE CRITICAL TEST: Backup must store REMAINING TTL, not absolute.

        Timeline:
        10:00  set("temp", ttl=600)  # expires at 10:10
        10:03  backup("snap1")       # 3 min elapsed, 7 min remaining
        10:05  modify data...
        10:08  restore("snap1")      # remaining was 7 min
                                     # new expiry = 10:08 + 7 min = 10:15
        """
        store = TTLBackupStore()

        # Create item at 10:00 with 10 min TTL (expires at 10:10)
        store.set_at("2021-01-01T10:00:00", "temp", "original", ttl=600)

        # Backup at 10:03 (3 min elapsed, 7 min = 420 sec remaining)
        store.backup("2021-01-01T10:03:00", "snap1")

        # Modify after backup
        store.set_at("2021-01-01T10:05:00", "temp", "modified", ttl=60)

        # Restore at 10:08
        store.restore("2021-01-01T10:08:00", "snap1")

        # After restore: value should be "original"
        assert store.get_at("2021-01-01T10:09:00", "temp") == "original"

        # TTL should be recalculated: 7 min remaining from 10:08 = expires at 10:15
        # At 10:14 (6 min after restore), should still be alive
        assert store.get_at("2021-01-01T10:14:00", "temp") == "original"

        # At 10:16 (8 min after restore), should be expired
        assert store.get_at("2021-01-01T10:16:00", "temp") is None

    def test_backup_deepcopy_not_reference(self):
        """Changes after backup must NOT affect the backup"""
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "key", "original")
        store.backup("2021-01-01T10:01:00", "snap1")

        # Modify after backup
        store.set_at("2021-01-01T10:02:00", "key", "modified")

        # Restore - should be "original", not "modified"
        store.restore("2021-01-01T10:03:00", "snap1")
        assert store.get_at("2021-01-01T10:04:00", "key") == "original"

    def test_restore_deepcopy_not_reference(self):
        """Changes after restore must NOT affect the snapshot"""
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "key", "original")
        store.backup("2021-01-01T10:01:00", "snap1")

        # First restore
        store.restore("2021-01-01T10:02:00", "snap1")

        # Modify after restore
        store.set_at("2021-01-01T10:03:00", "key", "modified")

        # Second restore - should still be "original"
        store.restore("2021-01-01T10:04:00", "snap1")
        assert store.get_at("2021-01-01T10:05:00", "key") == "original"

    def test_backup_permanent_and_ttl_items(self):
        """Backup should handle mix of permanent and TTL items"""
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "permanent", "pval", ttl=None)
        store.set_at("2021-01-01T10:00:00", "temp", "tval", ttl=600)

        store.backup("2021-01-01T10:03:00", "snap1")

        # Clear everything
        store.data = {}

        # Restore
        store.restore("2021-01-01T10:05:00", "snap1")

        # Permanent item should exist
        assert store.get_at("2021-01-01T10:06:00", "permanent") == "pval"

        # TTL item should have recalculated expiry
        # Original: 10 min from 10:00 = expires 10:10
        # At backup (10:03): 7 min remaining
        # At restore (10:05): new expiry = 10:05 + 7 min = 10:12
        assert store.get_at("2021-01-01T10:11:00", "temp") == "tval"  # Alive
        assert store.get_at("2021-01-01T10:13:00", "temp") is None  # Expired

    def test_restore_nonexistent_backup(self):
        store = TTLBackupStore()
        result = store.restore("2021-01-01T10:00:00", "nonexistent")
        assert result == "backup not found"

    def test_list_alive(self):
        store = TTLBackupStore()
        store.set_at("2021-01-01T10:00:00", "permanent", "p", ttl=None)
        store.set_at("2021-01-01T10:00:00", "temp", "t", ttl=300)

        # At 10:03, both alive
        assert store.list_alive("2021-01-01T10:03:00") == ["permanent", "temp"]

        # At 10:06, only permanent alive
        assert store.list_alive("2021-01-01T10:06:00") == ["permanent"]


class TestExercise3:
    """Exercise 3: TTL Calculator"""

    def test_remaining_ttl_basic(self):
        """4 minutes elapsed from 10 minute TTL = 6 minutes remaining"""
        remaining = TTLCalculator.calculate_remaining_ttl(
            upload_time="2021-01-01T10:00:00",
            original_ttl=600,  # 10 minutes
            current_time="2021-01-01T10:04:00"  # 4 minutes later
        )
        assert remaining == 360  # 6 minutes

    def test_remaining_ttl_expired(self):
        """Returns None if TTL has expired"""
        remaining = TTLCalculator.calculate_remaining_ttl(
            upload_time="2021-01-01T10:00:00",
            original_ttl=60,  # 1 minute
            current_time="2021-01-01T10:05:00"  # 5 minutes later
        )
        assert remaining is None

    def test_remaining_ttl_exactly_zero(self):
        """Returns None if remaining is exactly 0 (expired at boundary)"""
        remaining = TTLCalculator.calculate_remaining_ttl(
            upload_time="2021-01-01T10:00:00",
            original_ttl=300,  # 5 minutes
            current_time="2021-01-01T10:05:00"  # exactly 5 minutes later
        )
        assert remaining is None  # 0 or less means expired

    def test_is_alive_with_ttl(self):
        # Alive: 4 minutes into 10 minute TTL
        assert TTLCalculator.is_alive(
            upload_time="2021-01-01T10:00:00",
            ttl=600,
            query_time="2021-01-01T10:04:00"
        ) == True

        # Dead: 11 minutes into 10 minute TTL
        assert TTLCalculator.is_alive(
            upload_time="2021-01-01T10:00:00",
            ttl=600,
            query_time="2021-01-01T10:11:00"
        ) == False

    def test_is_alive_no_ttl_permanent(self):
        """ttl=None means permanent, always alive"""
        assert TTLCalculator.is_alive(
            upload_time="2021-01-01T10:00:00",
            ttl=None,
            query_time="2025-12-31T23:59:59"
        ) == True

    def test_is_alive_boundary(self):
        """Exactly at expiration time = dead (interval is [start, end))"""
        assert TTLCalculator.is_alive(
            upload_time="2021-01-01T10:00:00",
            ttl=300,  # 5 minutes
            query_time="2021-01-01T10:05:00"  # exactly at expiration
        ) == False


class TestExercise4:
    """Exercise 4: Rollback Engine - All Patterns Combined"""

    def test_add_and_get_basic(self):
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "key1", "value1")
        assert engine.get("2021-01-01T10:01:00", "key1") == "value1"

    def test_get_expired_item(self):
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "key1", "value1", ttl=60)
        assert engine.get("2021-01-01T10:00:30", "key1") == "value1"  # 30s, alive
        assert engine.get("2021-01-01T10:02:00", "key1") is None  # 2min, dead

    def test_rollback_removes_future_items(self):
        """Items added AFTER rollback point should be removed"""
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "old", "value1")
        engine.add("2021-01-01T10:05:00", "new", "value2")

        engine.rollback("2021-01-01T10:02:00")

        assert engine.get("2021-01-01T10:10:00", "old") == "value1"
        assert engine.get("2021-01-01T10:10:00", "new") is None

    def test_rollback_keeps_old_items(self):
        """Items added BEFORE rollback point should be kept"""
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "a", "1")
        engine.add("2021-01-01T10:01:00", "b", "2")
        engine.add("2021-01-01T10:02:00", "c", "3")

        engine.rollback("2021-01-01T10:01:30")

        items = engine.list_items("2021-01-01T10:05:00")
        assert items == ["a", "b"]

    def test_rollback_recalculates_ttl(self):
        """TTL should be recalculated based on elapsed time at rollback"""
        engine = RollbackEngine()
        # Upload at 10:00 with 10 min TTL (expires at 10:10)
        engine.add("2021-01-01T10:00:00", "temp", "value", ttl=600)

        # Rollback to 10:04 (4 min elapsed, 6 min remaining)
        engine.rollback("2021-01-01T10:04:00")

        # After rollback, remaining TTL = 6 min
        # New expiry = rollback_time + remaining = 10:04 + 6min = 10:10
        # But we reset upload_time to rollback_time, so:
        # Query at 10:09 (5 min after rollback) should be alive
        assert engine.get("2021-01-01T10:09:00", "temp") == "value"
        # Query at 10:11 (7 min after rollback) should be dead
        assert engine.get("2021-01-01T10:11:00", "temp") is None

    def test_rollback_handles_permanent_items(self):
        """Items with ttl=None should not crash TTL calculation"""
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "permanent", "value", ttl=None)
        engine.add("2021-01-01T10:05:00", "new", "value2")

        # This should not crash with "unsupported type for timedelta"
        engine.rollback("2021-01-01T10:02:00")

        assert engine.get("2021-01-01T10:10:00", "permanent") == "value"

    def test_list_items_filters_expired(self):
        engine = RollbackEngine()
        engine.add("2021-01-01T10:00:00", "permanent", "1", ttl=None)
        engine.add("2021-01-01T10:00:00", "temp", "2", ttl=300)  # 5 min

        # At 10:03, both alive
        assert engine.list_items("2021-01-01T10:03:00") == ["permanent", "temp"]

        # At 10:06, temp expired
        assert engine.list_items("2021-01-01T10:06:00") == ["permanent"]


class TestExercise5:
    """Exercise 5: Edge Cases"""

    def test_rollback_before_any_uploads(self):
        """Rollback to time before all uploads = empty state"""
        items = {
            "a": {"upload_time": "2021-01-01T10:05:00", "ttl": None},
            "b": {"upload_time": "2021-01-01T10:10:00", "ttl": 600}
        }
        result = EdgeCaseHandler.rollback_before_any_uploads(
            items,
            "2021-01-01T10:00:00"  # Before any uploads
        )
        assert result == {}

    def test_ttl_exactly_zero_remaining(self):
        """Item with exactly 0 remaining TTL should be considered expired"""
        result = EdgeCaseHandler.ttl_exactly_zero_remaining(
            upload_time="2021-01-01T10:00:00",
            original_ttl=300,  # 5 minutes
            rollback_time="2021-01-01T10:05:00"  # exactly 5 min later
        )
        assert result == False  # Should NOT keep (remaining = 0 = expired)

    def test_copy_inherits_ttl(self):
        """Copy should have same expiration as source"""
        result = EdgeCaseHandler.copy_inherits_ttl(
            source_upload_time="2021-01-01T10:00:00",
            source_ttl=600,
            copy_time="2021-01-01T10:03:00"
        )
        # Copy should inherit source's upload_time and ttl
        # So it expires at the same absolute time as source
        assert result["upload_time"] == "2021-01-01T10:00:00"
        assert result["ttl"] == 600

    def test_copy_permanent_source(self):
        """Copy of permanent item should also be permanent"""
        result = EdgeCaseHandler.copy_inherits_ttl(
            source_upload_time="2021-01-01T10:00:00",
            source_ttl=None,
            copy_time="2021-01-01T10:03:00"
        )
        assert result["ttl"] is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
