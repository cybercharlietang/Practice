"""
ICA-001: Notification System
============================
Implement a notification management system with TTL and backup/restore.

Run tests:
    pytest tests/ -v
    pytest tests/test_level1.py -v
"""
from collections import defaultdict, Counter
import copy
from datetime import datetime, timedelta
from email.policy import default
from typing import Optional, List, Dict, Any


class NotificationSystem:
    """
    A notification management system.

    Level 1: add_notification, get_notification, delete_notification, list_user_notifications
    Level 2: search_notifications, get_user_stats, get_top_users
    Level 3: *_at variants with timestamps and TTL
    Level 4: backup, restore
    """

    def __init__(self):
        self.notifications=defaultdict(dict)
        self.count=0

    # ==================== LEVEL 1: Basic Operations ====================

    def add_notification(self, user_id: str, message: str) -> str:
        """
        Create a new notification for a user.

        Args:
            user_id: The user who receives the notification.
            message: The notification message.

        Returns:
            The notification ID (auto-generated: "notif_1", "notif_2", ...).
        """
        self.count+=1
        nid="notif_"+str(self.count)
        self.notifications[nid] = {"message": message, "user": user_id}
        return nid

    def get_notification(self, notification_id: str) -> Optional[str]:
        """
        Get a notification message by ID.

        Args:
            notification_id: The notification ID to look up.

        Returns:
            The message if found, None otherwise.
        """
        if notification_id in self.notifications:
            return self.notifications[notification_id]["message"]
        return None

    def delete_notification(self, notification_id: str) -> bool:
        """
        Delete a notification by ID.

        Args:
            notification_id: The notification ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        if notification_id in self.notifications:
            self.notifications.pop(notification_id)
            return True
        return False

    def list_user_notifications(self, user_id: str) -> List[str]:
        """
        List all notification IDs for a user.

        Args:
            user_id: The user ID to query.

        Returns:
            List of notification IDs, sorted by creation order.
        """
        res = []
        for notif in self.notifications:
            if self.notifications[notif]["user"]==user_id:
                res.append(notif)
        return sorted(res)

    # ==================== LEVEL 2: Search & Statistics ====================

    def search_notifications(self, prefix: str) -> List[str]:
        """
        Search notifications by message prefix.

        Args:
            prefix: The prefix to search for (empty string matches all).

        Returns:
            List of "notif_id: message" strings, sorted by notification ID.
        """
        res = []
        l = len(prefix)
        for notif in self.notifications:
            if prefix == self.notifications[notif]["message"][:l]:
                res.append((notif, self.notifications[notif]["message"]))
        sorted_res=sorted(res, key=lambda k: k[0])
        return [notif+": "+message for notif, message in sorted_res]

    def get_user_stats(self, user_id: str) -> str:
        """
        Get notification count for a user.

        Args:
            user_id: The user ID to query.

        Returns:
            Formatted string "user_id(count)", e.g., "alice(5)".
        """
        count=0
        for notif in self.notifications:
            if self.notifications[notif]["user"]==user_id:
                count+=1
        return user_id+"("+str(count)+")"

    def get_top_users(self, n: int) -> List[str]:
        """
        Get top n users by notification count.

        Args:
            n: Maximum number of users to return.

        Returns:
            List of "user_id(count)" strings.
            Sorted by count descending, then user_id ascending.
        """
        counter=defaultdict(int)
        for notif in self.notifications:
            counter[self.notifications[notif]["user"]]+=1
        res =  list(counter.items())
        sort_res=sorted(res, key=lambda k: (-k[1],k[0]))[:n]
        return [user_id+"("+str(count)+")" for user_id, count in sort_res]


    # ==================== LEVEL 3: Timestamps & TTL ====================

    def add_notification_at(
        self, timestamp: str, user_id: str, message: str, ttl: Optional[int] = None
    ) -> str:
        """
        Create a notification with timestamp and optional TTL.

        Args:
            timestamp: ISO timestamp (e.g., "2021-01-01T10:00:00").
            user_id: The user who receives the notification.
            message: The notification message.
            ttl: Time-to-live in seconds. None means permanent.

        Returns:
            The notification ID.

        Note:
            Notification is available during [timestamp, timestamp + ttl).
        """
        # TODO: Implement
        pass

    def get_notification_at(self, timestamp: str, notification_id: str) -> Optional[str]:
        """
        Get a notification at a specific timestamp.

        Args:
            timestamp: The query timestamp.
            notification_id: The notification ID.

        Returns:
            The message if exists and not expired, None otherwise.
        """
        # TODO: Implement
        pass

    def list_user_notifications_at(self, timestamp: str, user_id: str) -> List[str]:
        """
        List non-expired notifications for a user at timestamp.

        Args:
            timestamp: The query timestamp.
            user_id: The user ID.

        Returns:
            List of notification IDs that are not expired.
        """
        # TODO: Implement
        pass

    def search_notifications_at(self, timestamp: str, prefix: str) -> List[str]:
        """
        Search non-expired notifications at timestamp.

        Args:
            timestamp: The query timestamp.
            prefix: The message prefix to search for.

        Returns:
            List of "notif_id: message" for non-expired notifications.
        """
        # TODO: Implement
        pass

    # ==================== LEVEL 4: Backup & Restore ====================

    def backup(self, timestamp: str, backup_id: str) -> str:
        """
        Create a backup of current state.

        Args:
            timestamp: The backup timestamp.
            backup_id: Identifier for this backup.

        Returns:
            "backup {backup_id} created"

        CRITICAL:
            - Use deep copy (changes after backup don't affect it)
            - Store REMAINING TTL, not absolute expiry
            - remaining_ttl = original_ttl - elapsed_time
        """
        # TODO: Implement
        pass

    def restore(self, timestamp: str, backup_id: str) -> str:
        """
        Restore state from a backup.

        Args:
            timestamp: The restore timestamp.
            backup_id: The backup to restore from.

        Returns:
            "restored from {backup_id}" or "backup not found"

        CRITICAL:
            - Use deep copy (changes after restore don't affect the backup)
            - Recalculate TTL: new_upload_time = restore_time, new_ttl = remaining_ttl
        """
        # TODO: Implement
        pass
