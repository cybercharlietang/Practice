"""
Level 4 Tests: Backup & Restore
================================
Run: pytest tests/test_level4.py -v

CRITICAL PATTERN: TTL Recalculation
- At backup: store REMAINING TTL (not absolute expiry)
- At restore: new_expiry = restore_time + remaining_ttl
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import NotificationSystem


class TestLevel4:
    """Level 4: Backup and Restore with TTL Recalculation"""

    def test_backup_basic(self):
        """backup creates a snapshot"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Hello")
        result = ns.backup("2021-01-01T10:01:00", "snap1")
        assert result == "backup snap1 created"

    def test_restore_basic(self):
        """restore brings back state from snapshot"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Original")
        ns.backup("2021-01-01T10:01:00", "snap1")

        # Modify after backup
        ns.add_notification_at("2021-01-01T10:02:00", "bob", "New")

        # Restore
        result = ns.restore("2021-01-01T10:03:00", "snap1")
        assert result == "restored from snap1"

        # notif_1 should exist, notif_2 should not
        assert ns.get_notification_at("2021-01-01T10:04:00", "notif_1") == "Original"
        assert ns.get_notification_at("2021-01-01T10:04:00", "notif_2") is None

    def test_restore_not_found(self):
        """restore returns error for non-existent backup"""
        ns = NotificationSystem()
        result = ns.restore("2021-01-01T10:00:00", "nonexistent")
        assert result == "backup not found"

    def test_backup_uses_deep_copy(self):
        """Changes after backup do NOT affect the backup"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Original")
        ns.backup("2021-01-01T10:01:00", "snap1")

        # Delete after backup
        ns.delete_notification("notif_1")

        # Restore should bring it back
        ns.restore("2021-01-01T10:02:00", "snap1")
        assert ns.get_notification_at("2021-01-01T10:03:00", "notif_1") == "Original"

    def test_restore_uses_deep_copy(self):
        """Changes after restore do NOT affect the backup"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Original")
        ns.backup("2021-01-01T10:01:00", "snap1")

        # First restore
        ns.restore("2021-01-01T10:02:00", "snap1")

        # Modify after restore
        ns.delete_notification("notif_1")

        # Second restore should still work
        ns.restore("2021-01-01T10:03:00", "snap1")
        assert ns.get_notification_at("2021-01-01T10:04:00", "notif_1") == "Original"

    def test_backup_stores_remaining_ttl(self):
        """
        CRITICAL: Backup stores REMAINING TTL, restore recalculates expiry.

        Timeline:
        10:00  add notif with ttl=600 (expires 10:10)
        10:03  backup (3 min elapsed, 7 min = 420 sec remaining)
        10:08  restore (new expiry = 10:08 + 420 sec = 10:15)
        """
        ns = NotificationSystem()

        # Create notification at 10:00 with 10 min TTL
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Temp", ttl=600)

        # Backup at 10:03 (420 sec remaining)
        ns.backup("2021-01-01T10:03:00", "snap1")

        # Restore at 10:08
        ns.restore("2021-01-01T10:08:00", "snap1")

        # New expiry should be 10:08 + 420 sec = 10:15
        # At 10:14 (6 min after restore), should be alive
        assert ns.get_notification_at("2021-01-01T10:14:00", "notif_1") == "Temp"

        # At 10:16 (8 min after restore), should be expired
        assert ns.get_notification_at("2021-01-01T10:16:00", "notif_1") is None

    def test_backup_handles_permanent_notifications(self):
        """Permanent notifications (ttl=None) work correctly with backup/restore"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Permanent", ttl=None)
        ns.backup("2021-01-01T10:01:00", "snap1")

        # Clear and restore
        ns.delete_notification("notif_1")
        ns.restore("2021-01-01T10:02:00", "snap1")

        # Should still be permanent
        assert ns.get_notification_at("2025-12-31T23:59:59", "notif_1") == "Permanent"

    def test_backup_mixed_ttl_and_permanent(self):
        """Backup handles mix of TTL and permanent notifications"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Permanent", ttl=None)
        ns.add_notification_at("2021-01-01T10:00:00", "bob", "Temporary", ttl=600)

        ns.backup("2021-01-01T10:03:00", "snap1")

        # Modify
        ns.delete_notification("notif_1")
        ns.delete_notification("notif_2")

        # Restore at 10:05
        ns.restore("2021-01-01T10:05:00", "snap1")

        # Permanent still alive
        assert ns.get_notification_at("2021-01-01T10:10:00", "notif_1") == "Permanent"

        # Temporary: was 10 min TTL, 3 min elapsed at backup, 7 min remaining
        # New expiry = 10:05 + 7 min = 10:12
        assert ns.get_notification_at("2021-01-01T10:11:00", "notif_2") == "Temporary"
        assert ns.get_notification_at("2021-01-01T10:13:00", "notif_2") is None

    def test_multiple_backups(self):
        """Multiple backups work independently"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "V1")
        ns.backup("2021-01-01T10:01:00", "snap1")

        ns.add_notification_at("2021-01-01T10:02:00", "alice", "V2")
        ns.backup("2021-01-01T10:03:00", "snap2")

        # Restore to snap1 (only V1)
        ns.restore("2021-01-01T10:04:00", "snap1")
        assert ns.get_notification_at("2021-01-01T10:05:00", "notif_1") == "V1"
        assert ns.get_notification_at("2021-01-01T10:05:00", "notif_2") is None

        # Restore to snap2 (V1 and V2)
        ns.restore("2021-01-01T10:06:00", "snap2")
        assert ns.get_notification_at("2021-01-01T10:07:00", "notif_1") == "V1"
        assert ns.get_notification_at("2021-01-01T10:07:00", "notif_2") == "V2"
