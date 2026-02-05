"""
Level 2 Tests: Search & Statistics
===================================
Run: pytest tests/test_level2.py -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import NotificationSystem


class TestLevel2:
    """Level 2: Search and Statistics"""

    def test_search_notifications_with_prefix(self):
        """search_notifications finds messages starting with prefix"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Hello World")
        ns.add_notification("bob", "Hello Bob")
        ns.add_notification("alice", "Goodbye")
        result = ns.search_notifications("Hello")
        assert result == ["notif_1: Hello World", "notif_2: Hello Bob"]

    def test_search_notifications_empty_prefix(self):
        """Empty prefix returns all notifications"""
        ns = NotificationSystem()
        ns.add_notification("alice", "First")
        ns.add_notification("bob", "Second")
        result = ns.search_notifications("")
        assert result == ["notif_1: First", "notif_2: Second"]

    def test_search_notifications_no_match(self):
        """search_notifications returns empty when no match"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Hello")
        result = ns.search_notifications("Goodbye")
        assert result == []

    def test_search_notifications_sorted_by_id(self):
        """Results sorted by notification ID"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Msg A")
        ns.add_notification("bob", "Msg B")
        ns.add_notification("charlie", "Msg C")
        result = ns.search_notifications("Msg")
        assert result == ["notif_1: Msg A", "notif_2: Msg B", "notif_3: Msg C"]

    def test_get_user_stats_basic(self):
        """get_user_stats returns formatted count"""
        ns = NotificationSystem()
        ns.add_notification("alice", "First")
        ns.add_notification("alice", "Second")
        ns.add_notification("bob", "Bob's")
        result = ns.get_user_stats("alice")
        assert result == "alice(2)"

    def test_get_user_stats_zero_notifications(self):
        """get_user_stats returns 0 for user with no notifications"""
        ns = NotificationSystem()
        result = ns.get_user_stats("nobody")
        assert result == "nobody(0)"

    def test_get_top_users_basic(self):
        """get_top_users returns users sorted by count descending"""
        ns = NotificationSystem()
        ns.add_notification("alice", "A1")
        ns.add_notification("alice", "A2")
        ns.add_notification("alice", "A3")
        ns.add_notification("bob", "B1")
        ns.add_notification("bob", "B2")
        ns.add_notification("charlie", "C1")
        result = ns.get_top_users(3)
        assert result == ["alice(3)", "bob(2)", "charlie(1)"]

    def test_get_top_users_limit(self):
        """get_top_users respects n limit"""
        ns = NotificationSystem()
        ns.add_notification("alice", "A")
        ns.add_notification("bob", "B")
        ns.add_notification("charlie", "C")
        result = ns.get_top_users(2)
        assert len(result) == 2

    def test_get_top_users_tie_break_alphabetically(self):
        """Ties broken alphabetically by user_id"""
        ns = NotificationSystem()
        ns.add_notification("charlie", "C")
        ns.add_notification("alice", "A")
        ns.add_notification("bob", "B")
        result = ns.get_top_users(3)
        # All have 1 notification, should be alphabetical
        assert result == ["alice(1)", "bob(1)", "charlie(1)"]

    def test_search_after_delete(self):
        """search_notifications excludes deleted notifications"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Keep this")
        ns.add_notification("alice", "Delete this")
        ns.delete_notification("notif_2")
        result = ns.search_notifications("")
        assert result == ["notif_1: Keep this"]
