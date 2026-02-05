"""
Level 1 Tests: Basic Operations
================================
Run: pytest tests/test_level1.py -v
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation import NotificationSystem


class TestLevel1:
    """Level 1: Basic CRUD Operations"""

    def test_add_notification_returns_id(self):
        """add_notification returns auto-generated ID"""
        ns = NotificationSystem()
        notif_id = ns.add_notification("alice", "Hello")
        assert notif_id == "notif_1"

    def test_add_multiple_notifications_sequential_ids(self):
        """Notification IDs are sequential"""
        ns = NotificationSystem()
        id1 = ns.add_notification("alice", "First")
        id2 = ns.add_notification("bob", "Second")
        id3 = ns.add_notification("alice", "Third")
        assert id1 == "notif_1"
        assert id2 == "notif_2"
        assert id3 == "notif_3"

    def test_get_notification_exists(self):
        """get_notification returns message when exists"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Hello World")
        result = ns.get_notification("notif_1")
        assert result == "Hello World"

    def test_get_notification_not_found(self):
        """get_notification returns None when not found"""
        ns = NotificationSystem()
        result = ns.get_notification("notif_999")
        assert result is None

    def test_delete_notification_exists(self):
        """delete_notification returns True and removes notification"""
        ns = NotificationSystem()
        ns.add_notification("alice", "To delete")
        result = ns.delete_notification("notif_1")
        assert result == True
        assert ns.get_notification("notif_1") is None

    def test_delete_notification_not_found(self):
        """delete_notification returns False when not found"""
        ns = NotificationSystem()
        result = ns.delete_notification("notif_999")
        assert result == False

    def test_list_user_notifications_basic(self):
        """list_user_notifications returns user's notification IDs"""
        ns = NotificationSystem()
        ns.add_notification("alice", "First")
        ns.add_notification("bob", "Bob's message")
        ns.add_notification("alice", "Second")
        result = ns.list_user_notifications("alice")
        assert result == ["notif_1", "notif_3"]

    def test_list_user_notifications_empty(self):
        """list_user_notifications returns empty list for user with no notifications"""
        ns = NotificationSystem()
        ns.add_notification("alice", "Hello")
        result = ns.list_user_notifications("bob")
        assert result == []

    def test_list_user_notifications_after_delete(self):
        """list_user_notifications excludes deleted notifications"""
        ns = NotificationSystem()
        ns.add_notification("alice", "First")
        ns.add_notification("alice", "Second")
        ns.delete_notification("notif_1")
        result = ns.list_user_notifications("alice")
        assert result == ["notif_2"]

    def test_add_notification_empty_message(self):
        """Handles empty message"""
        ns = NotificationSystem()
        notif_id = ns.add_notification("alice", "")
        assert notif_id == "notif_1"
        assert ns.get_notification("notif_1") == ""
