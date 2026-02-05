"""
Level 3 Tests: Timestamps & TTL
================================
Run: pytest tests/test_level3.py -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import NotificationSystem


class TestLevel3:
    """Level 3: Timestamps and TTL"""

    def test_add_notification_at_basic(self):
        """add_notification_at creates notification with timestamp"""
        ns = NotificationSystem()
        notif_id = ns.add_notification_at("2021-01-01T10:00:00", "alice", "Hello")
        assert notif_id == "notif_1"

    def test_get_notification_at_no_ttl(self):
        """Permanent notification (no TTL) always accessible"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Permanent", ttl=None)
        result = ns.get_notification_at("2025-12-31T23:59:59", "notif_1")
        assert result == "Permanent"

    def test_get_notification_at_within_ttl(self):
        """Notification accessible within TTL"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Temp", ttl=600)  # 10 min
        result = ns.get_notification_at("2021-01-01T10:05:00", "notif_1")  # 5 min later
        assert result == "Temp"

    def test_get_notification_at_expired(self):
        """Notification not accessible after TTL expires"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Temp", ttl=300)  # 5 min
        result = ns.get_notification_at("2021-01-01T10:06:00", "notif_1")  # 6 min later
        assert result is None

    def test_get_notification_at_exactly_expired(self):
        """At exactly upload_time + ttl, notification is expired"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Temp", ttl=300)
        # Exactly 5 minutes later = expired (interval is [start, end))
        result = ns.get_notification_at("2021-01-01T10:05:00", "notif_1")
        assert result is None

    def test_list_user_notifications_at_filters_expired(self):
        """list_user_notifications_at excludes expired notifications"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Permanent", ttl=None)
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Short", ttl=60)  # 1 min
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Long", ttl=600)  # 10 min

        # At 10:02, Short is expired
        result = ns.list_user_notifications_at("2021-01-01T10:02:00", "alice")
        assert "notif_1" in result  # Permanent
        assert "notif_2" not in result  # Expired
        assert "notif_3" in result  # Still alive

    def test_search_notifications_at_excludes_expired(self):
        """search_notifications_at excludes expired notifications"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Msg Permanent", ttl=None)
        ns.add_notification_at("2021-01-01T10:00:00", "bob", "Msg Temporary", ttl=60)

        result = ns.search_notifications_at("2021-01-01T10:02:00", "Msg")
        assert result == ["notif_1: Msg Permanent"]

    def test_get_notification_at_not_found(self):
        """get_notification_at returns None for non-existent notification"""
        ns = NotificationSystem()
        result = ns.get_notification_at("2021-01-01T10:00:00", "notif_999")
        assert result is None

    def test_multiple_users_with_ttl(self):
        """Multiple users with different TTLs"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "Alice msg", ttl=300)
        ns.add_notification_at("2021-01-01T10:00:00", "bob", "Bob msg", ttl=600)

        # At 10:06, alice's expired, bob's alive
        assert ns.get_notification_at("2021-01-01T10:06:00", "notif_1") is None
        assert ns.get_notification_at("2021-01-01T10:06:00", "notif_2") == "Bob msg"

    def test_list_user_notifications_at_preserves_order(self):
        """list_user_notifications_at returns in creation order"""
        ns = NotificationSystem()
        ns.add_notification_at("2021-01-01T10:00:00", "alice", "First")
        ns.add_notification_at("2021-01-01T10:01:00", "bob", "Bob's")
        ns.add_notification_at("2021-01-01T10:02:00", "alice", "Second")

        result = ns.list_user_notifications_at("2021-01-01T10:05:00", "alice")
        assert result == ["notif_1", "notif_3"]
