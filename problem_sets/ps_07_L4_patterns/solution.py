"""
PS-07: L4 State Management Patterns
===================================
Focus: rollback, TTL recalculation, deep copy, control flow

Run tests:
    pytest test_L4_patterns.py -v
"""
import copy
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


# =============================================================================
# EXERCISE 1: Trace Before Code (Warm-up)
# =============================================================================
# Before implementing, answer these questions BY HAND (write in comments):
#
# Scenario:
#   10:00  upload("a.txt", ttl=600)      # 10 min TTL
#   10:03  upload("b.txt", ttl=None)     # No TTL (permanent)
#   10:05  upload("c.txt", ttl=300)      # 5 min TTL
#   10:08  rollback to 10:04
#
# Q1: Which files exist after rollback?
# YOUR ANSWER: all a and b
#
# Q2: What is the remaining TTL for "a.txt" after rollback?
# YOUR ANSWER: 6 minutes
#
# Q3: If we query at 10:15, is "a.txt" still alive?
# YOUR ANSWER: It just expires on 10:15
#
# (Implement the function below to verify your answers)

def trace_scenario() -> Dict[str, Any]:
    """
    Return the expected state after the rollback scenario above.

    Returns:
        {
            "files_after_rollback": ["a.txt", "b.txt", ...],
            "a_remaining_ttl": <int seconds>,
            "a_alive_at_10_15": <bool>
        }
    """
    return {"files_after_rollback":["a.txt", "b.txt"], "a_remaining_ttl": 360, "a_alive_at_10_15": False}


# =============================================================================
# EXERCISE 2: Snapshot Manager
# =============================================================================
class SnapshotManager:
    """
    A simple key-value store with backup/restore capability.

    Focus: Deep copy discipline

    Bug to avoid: self.snapshots[ts] = self.data  # WRONG - reference!
    """

    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
        self.snapshots: Dict[str, Dict] = {}

    def set(self, key: str, field: str, value: Any) -> None:
        """Set data[key][field] = value"""
        self.data[key]={}
        self.data[key][field]=value
        return None

    def get(self, key: str, field: str) -> Optional[Any]:
        """Get data[key][field], return None if not exists"""
        if key in self.data:
            if field in self.data[key]:
                return self.data[key][field]
        return None

    def backup(self, snapshot_id: str) -> str:
        """
        Create a snapshot of current state.

        CRITICAL: Must use deepcopy, not reference!

        Returns:
            "backup created"
        """
        self.snapshots[snapshot_id]=copy.deepcopy(self.data)
        return "backup created"

    def restore(self, snapshot_id: str) -> str:
        """
        Restore state from snapshot.

        CRITICAL: Must deepcopy the snapshot, not reference!

        Returns:
            "restored from {snapshot_id}" or "snapshot not found"
        """
        if snapshot_id in self.snapshots:
            self.data=copy.deepcopy(self.snapshots[snapshot_id])
            return "restored from "+str(snapshot_id)
        return "snapshot not found"



# =============================================================================
# EXERCISE 2B: Backup/Restore WITH TTL (The Hard Pattern)
# =============================================================================
class TTLBackupStore:
    """
    Key-value store with TTL and backup/restore.

    THIS IS THE EXACT PATTERN THAT CAUSED PROBLEMS IN LIBRESIGNAL.

    The tricky part:
    - At backup time, store REMAINING TTL (not absolute expiry)
    - At restore time, calculate NEW expiry from remaining TTL

    Example:
        10:00  set("key", "val", ttl=600)  # expires at 10:10
        10:03  backup("snap1")             # remaining = 600 - 180 = 420 sec
        10:08  restore("snap1")            # new expiry = 10:08 + 420 = 10:15

    Common bugs:
    1. Storing absolute expiry instead of remaining TTL
    2. Using reference instead of deepcopy
    3. Not recalculating expiry on restore
    """

    def __init__(self):
        self.data: Dict[str, Dict] = {}
        # Each entry: {"value": any, "upload_time": str, "ttl": Optional[int]}
        self.backups: Dict[str, Dict] = {}

    def set_at(self, timestamp: str, key: str, value: Any, ttl: Optional[int] = None) -> str:
        """
        Set a key with timestamp and optional TTL.

        Args:
            timestamp: Current time
            key: The key
            value: The value
            ttl: Optional TTL in seconds (None = permanent)

        Returns:
            "set {key}"
        """
        self.data[key]={"value": value, "upload_time": timestamp, "ttl": ttl}
        return "set "+key

    def get_at(self, timestamp: str, key: str) -> Optional[Any]:
        """
        Get a key at timestamp (check if expired).

        Returns:
            The value if exists and not expired, None otherwise
        """
        if key not in self.data:
            return None
        if self.data[key]["ttl"]==None:
            return self.data[key]["value"] 
        current=datetime.fromisoformat(timestamp)
        upload=datetime.fromisoformat(self.data[key]["upload_time"])
        dt=timedelta(seconds=self.data[key]["ttl"])
        if current> upload+dt:
            return None
        return self.data[key]["value"]

    def backup(self, timestamp: str, backup_id: str) -> str:
        """
        Create a backup at timestamp.

        MUST store:
        1. Deep copy of data
        2. REMAINING TTL for each key (not absolute expiry!)

        The remaining TTL = original_ttl - elapsed
        where elapsed = timestamp - upload_time

        Returns:
            "backup {backup_id} created"
        """
        self.backups[backup_id]=copy.deepcopy(self.data)
        for key in self.backups[backup_id]:
            if self.data[key]["ttl"]==None:
                continue
            current=datetime.fromisoformat(timestamp)
            upload=datetime.fromisoformat(self.data[key]["upload_time"])
            dt=self.data[key]["ttl"]
            elapsed=(current-upload).total_seconds()
            self.backups[backup_id][key]["remaining_ttl"]=dt-elapsed
        return "backup "+backup_id+" created"

    def restore(self, timestamp: str, backup_id: str) -> str:
        """
        Restore from backup at timestamp.

        MUST:
        1. Deep copy the backup (don't use reference!)
        2. Recalculate new expiry times:
           new_upload_time = timestamp (restore time)
           new_ttl = remaining_ttl from backup

        Returns:
            "restored from {backup_id}" or "backup not found"
        """
        if backup_id not in self.backups:
            return "backup not found"
        self.data=copy.deepcopy(self.backups[backup_id])
        for key in self.data:
            self.data[key]["upload_time"]=timestamp
            if "remaining_ttl" not in self.data[key]:
                continue
            self.data[key]["ttl"]=self.data[key]["remaining_ttl"]
        return "restored from "+backup_id

    def list_alive(self, timestamp: str) -> List[str]:
        """List all keys that are alive at timestamp, sorted."""
        res=[]
        for key in self.data:
            if self.data[key]["ttl"]==None:
                res.append(key)
                continue
            current=datetime.fromisoformat(timestamp)
            upload=datetime.fromisoformat(self.data[key]["upload_time"])
            dt=self.data[key]["ttl"]
            if dt>=(current-upload).total_seconds():
                res.append(key)
        return sorted(res)


# =============================================================================
# EXERCISE 3: TTL Calculator
# =============================================================================
class TTLCalculator:
    """
    Practice TTL recalculation in isolation.

    Focus: The formula and keeping TTL as int/float, not string

    Formula: remaining = original_ttl - elapsed
             elapsed = (current_time - upload_time).total_seconds()
    """

    @staticmethod
    def calculate_remaining_ttl(
        upload_time: str,
        original_ttl: int,
        current_time: str
    ) -> Optional[int]:
        """
        Calculate remaining TTL at current_time.

        Args:
            upload_time: ISO timestamp when item was created
            original_ttl: Original TTL in seconds
            current_time: ISO timestamp to calculate remaining TTL at

        Returns:
            Remaining TTL in seconds (int), or None if expired

        Example:
            upload_time = "2021-01-01T10:00:00"
            original_ttl = 600  # 10 minutes
            current_time = "2021-01-01T10:04:00"  # 4 minutes later
            -> returns 360 (6 minutes remaining)
        """
        upload=datetime.fromisoformat(upload_time)
        current=datetime.fromisoformat(current_time)
        if original_ttl-(current-upload).total_seconds()<=0:
            return None
        return original_ttl-(current-upload).total_seconds()
    
    @staticmethod
    def is_alive(
        upload_time: str,
        ttl: Optional[int],
        query_time: str
    ) -> bool:
        """
        Check if item is alive at query_time.

        Args:
            upload_time: ISO timestamp when item was created
            ttl: TTL in seconds, or None for permanent
            query_time: ISO timestamp to check

        Returns:
            True if alive (ttl is None OR query_time < upload_time + ttl)

        Note:
            Must handle ttl=None case (permanent, always alive)
        """
        if ttl==None:
            return True
        upload=datetime.fromisoformat(upload_time)
        query=datetime.fromisoformat(query_time)
        if ttl-(query-upload).total_seconds()<=0:
            return False
        return True


# =============================================================================
# EXERCISE 4: Rollback Engine
# =============================================================================
class RollbackEngine:
    """
    A data store with timestamps, TTL, and rollback capability.

    Focus: Combining all patterns correctly

    Patterns to use:
    1. Condition: remove if upload_time > rollback_time
    2. Control flow: else clause for items we keep
    3. TTL recalc: remaining = original - elapsed
    4. None check: if ttl is not None before calculation
    """

    def __init__(self):
        self.items: Dict[str, Dict] = {}
        # Each item: {"value": any, "upload_time": str, "ttl": Optional[int]}

    def add(self, timestamp: str, key: str, value: Any, ttl: Optional[int] = None) -> str:
        """
        Add an item with timestamp and optional TTL.

        Returns:
            "added {key}"
        """
        self.items[key]={"value": value, "upload_time": timestamp, "ttl": ttl}
        return "added "+ key

    def get(self, timestamp: str, key: str) -> Optional[Any]:
        """
        Get item if it exists and is not expired at timestamp.

        Returns:
            The value if alive, None otherwise
        """
        if key not in self.items:
            return None
        if self.items[key]["ttl"]==None:
            return self.items[key]["value"]
        upload=datetime.fromisoformat(self.items[key]["upload_time"])
        current=datetime.fromisoformat(timestamp)
        if self.items[key]["ttl"]>(current-upload).total_seconds():
            return self.items[key]["value"]
        return None

    def rollback(self, timestamp: str) -> str:
        """
        Rollback to the given timestamp.

        Must:
        1. Remove items added AFTER timestamp (upload_time > timestamp)
        2. Recalculate TTL for remaining items with TTL
        3. Handle items without TTL (ttl=None) - just keep them
        4. Use proper control flow (else clause after remove)

        Returns:
            "rollback to {timestamp}"
        """
        for key in list(self.items.keys()):
            upload=datetime.fromisoformat(self.items[key]["upload_time"])
            current=datetime.fromisoformat(timestamp)
            if upload >= current:
                self.items.pop(key)
                continue
            else:
                if self.items[key]["ttl"]==None:
                    continue
                else: 
                    self.items[key]["ttl"]=self.items[key]["ttl"]-(current-upload).total_seconds()
                    self.items[key]["upload_time"]=timestamp
        return "rollback to "+timestamp
        


    def list_items(self, timestamp: str) -> List[str]:
        """
        List all alive item keys at timestamp, sorted alphabetically.

        Returns:
            List of keys that are alive at timestamp
        """
        alive=[]
        for key in self.items:
            if self.get(timestamp, key) != None:
                alive.append(key)
        return sorted(alive)



# =============================================================================
# EXERCISE 5: Edge Cases
# =============================================================================
class EdgeCaseHandler:
    """
    Handle the tricky edge cases that break L4 implementations.
    """

    @staticmethod
    def rollback_before_any_uploads(items: Dict, rollback_time: str) -> Dict:
        """
        What happens if rollback_time is before all uploads?

        Args:
            items: {"key": {"upload_time": str, "ttl": Optional[int], ...}}
            rollback_time: ISO timestamp

        Returns:
            Empty dict (all items were uploaded after rollback point)
        """
        # TODO: Implement
        pass

    @staticmethod
    def ttl_exactly_zero_remaining(
        upload_time: str,
        original_ttl: int,
        rollback_time: str
    ) -> bool:
        """
        Should we keep an item if remaining TTL is exactly 0?

        The interval is [upload_time, upload_time + ttl)
        So exactly at upload_time + ttl, it's expired.

        Returns:
            False - item should be removed (TTL of 0 means expired)
        """
        # TODO: Implement
        pass

    @staticmethod
    def copy_inherits_ttl(
        source_upload_time: str,
        source_ttl: Optional[int],
        copy_time: str
    ) -> Dict:
        """
        When copying an item, the copy inherits the SAME expiration time.

        NOT the same TTL from copy_time, but the same absolute expiration.

        Args:
            source_upload_time: When source was uploaded
            source_ttl: Source's original TTL
            copy_time: When copy was made

        Returns:
            {"upload_time": <same as source>, "ttl": <same as source>}

        Note:
            The copy expires at the same time as the source would have.
            This means storing the original upload_time and ttl, not recalculating.
        """
        # TODO: Implement
        pass
