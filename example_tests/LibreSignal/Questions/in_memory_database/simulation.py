"""
All your implementation code for the in-memory database simulation goes here.
"""
from collections import defaultdict
import bisect
import copy

class Simulation:
    def __init__(self):
        self.data=defaultdict(dict)
        self.expire=defaultdict(dict)
        self.back=defaultdict(dict)

    # ==================== LEVEL 1: Basic Operations ====================

    def set(self, key: str, field: str, value: str) -> str:
        """
        Insert a field-value pair to the record associated with key.
        If the field already exists, replace the existing value.
        If the record does not exist, create a new one.

        Args:
            key: The record identifier.
            field: The field name within the record.
            value: The value to store.

        Returns:
            An empty string "".
        """
        self.data[key][field]=value
        return ""


    def get(self, key: str, field: str) -> str:
        """
        Return the value contained within field of the record associated with key.

        Args:
            key: The record identifier.
            field: The field name within the record.

        Returns:
            The value if found, empty string "" if record or field doesn't exist.
        """
        if key not in self.data:
            return ""
        if field not in self.data[key]:
            return ""
        return self.data[key][field]

    def delete(self, key: str, field: str) -> str:
        """
        Remove the field from the record associated with key.

        Args:
            key: The record identifier.
            field: The field name to delete.

        Returns:
            "true" if the field was successfully deleted.
            "false" if the key or field does not exist.
        """
        if key not in self.data:
            return "false"
        if field not in self.data[key]:
            return "false"
        self.data[key].pop(field)
        return "true"

    # ==================== LEVEL 2: Scan Operations ====================

    def scan(self, key: str) -> str:
        """
        Return a string representing all fields of a record.

        Args:
            key: The record identifier.

        Returns:
            Format: "<field1>(<value1>), <field2>(<value2>), ..."
            Fields sorted lexicographically.
            Empty string "" if record doesn't exist.
        """
        if key not in self.data:
            return ""
        res = []
        for field in self.data[key]:
            res.append(str(field)+"("+str(self.data[key][field])+")")
        return ", ".join(sorted(res))

    def scan_by_prefix(self, key: str, prefix: str) -> str:
        """
        Return a string representing fields that start with prefix.

        Args:
            key: The record identifier.
            prefix: The prefix to filter fields by.

        Returns:
            Same format as scan(), but only fields starting with prefix.
            Fields sorted lexicographically.
            Empty string "" if record doesn't exist or no fields match.
        """
        if key not in self.data:
            return ""
        res = []
        l_p=len(list(prefix))
        for field in self.data[key]:
            l=len(list(field))
            if l_p>l:
                continue
            if list(prefix)==list(field)[:l_p]:
                res.append(str(field)+"("+str(self.data[key][field])+")")
        return ", ".join(sorted(res))

    # ==================== LEVEL 3: Timestamp & TTL ====================

    def set_at(self, key: str, field: str, value: str, timestamp: int) -> str:
        """
        Same as set(), but with timestamp specified.

        Args:
            key: The record identifier.
            field: The field name.
            value: The value to store.
            timestamp: The timestamp of this operation.

        Returns:
            An empty string "".
        """
        self.data[key][field]=value
        return ""

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> str:
        """
        Same as set_at(), but with TTL (Time-To-Live).

        The field-value pair will exist during [timestamp, timestamp + ttl).

        Args:
            key: The record identifier.
            field: The field name.
            value: The value to store.
            timestamp: The timestamp of this operation.
            ttl: Time-to-live in timestamp units.

        Returns:
            An empty string "".
        """
        self.data[key][field]=value
        self.expire[key][field]=timestamp+ttl
        return ""

    def get_at(self, key: str, field: str, timestamp: int) -> str:
        """
        Same as get(), but with timestamp specified.

        Args:
            key: The record identifier.
            field: The field name.
            timestamp: The timestamp of this operation.

        Returns:
            The value if found and not expired, empty string "" otherwise.
        """
        for f, expiry in list(self.expire[key].items()):
            if expiry<=timestamp:
                self.data[key].pop(f)
                self.expire[key].pop(f)
        if key not in self.data:
            return ""
        if field not in self.data[key]:
            return ""
        return self.data[key][field]

    def delete_at(self, key: str, field: str, timestamp: int) -> str:
        """
        Same as delete(), but with timestamp specified.

        Args:
            key: The record identifier.
            field: The field name.
            timestamp: The timestamp of this operation.

        Returns:
            "true" if field existed and was deleted.
            "false" if key or field doesn't exist (including if expired).
        """
        for f, expiry in list(self.expire[key].items()):
            if expiry<=timestamp:
                self.data[key].pop(f)
                self.expire[key].pop(f)
        if key not in self.data:
            return "false"
        if field not in self.data[key]:
            return "false"
        self.data[key].pop(field)
        return "true"
        

    def scan_at(self, key: str, timestamp: int) -> str:
        """
        Same as scan(), but with timestamp specified.

        Args:
            key: The record identifier.
            timestamp: The timestamp of this operation.

        Returns:
            Same format as scan(), excluding expired fields.
        """
        for f, expiry in list(self.expire[key].items()):
            if expiry<=timestamp:
                self.data[key].pop(f)
                self.expire[key].pop(f)
        if key not in self.data:
            return ""
        res = []
        for field in self.data[key]:
            res.append(str(field)+"("+str(self.data[key][field])+")")
        return ", ".join(sorted(res))

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> str:
        """
        Same as scan_by_prefix(), but with timestamp specified.

        Args:
            key: The record identifier.
            prefix: The prefix to filter fields by.
            timestamp: The timestamp of this operation.

        Returns:
            Same format as scan_by_prefix(), excluding expired fields.
        """
        for f, expiry in list(self.expire[key].items()):
            if expiry<=timestamp:
                self.data[key].pop(f)
                self.expire[key].pop(f)
        if key not in self.data:
            return ""
        res = []
        l_p=len(list(prefix))
        for field in self.data[key]:
            l=len(list(field))
            if l_p>l:
                continue
            if list(prefix)==list(field)[:l_p]:
                res.append(str(field)+"("+str(self.data[key][field])+")")
        return ", ".join(sorted(res))

    # ==================== LEVEL 4: Backup & Restore ====================

    def backup(self, timestamp: int) -> str:
        """
        Save the database state at the specified timestamp.

        Saves remaining TTL for all records and fields.
        Remaining TTL = initial TTL - (timestamp - initial timestamp).

        Args:
            timestamp: The timestamp of this backup.

        Returns:
            String representing the number of non-empty, non-expired records.
        """
        for key in list(self.data.keys()):
            for f, expiry in list(self.expire[key].items()):
                if expiry<=timestamp:
                    self.data[key].pop(f)
                    self.expire[key].pop(f)
        self.back[timestamp]={"data": copy.deepcopy(self.data), "expire": copy.deepcopy(self.expire)}
        count = sum(1 for key in self.data if self.data[key])                                                              
        return str(count)

    def restore(self, timestamp: int, timestamp_to_restore: int) -> str:
        """
        Restore the database from the latest backup at or before timestamp_to_restore.

        Expiration times are recalculated: new_expiry = timestamp + remaining_ttl.

        Args:
            timestamp: The timestamp of this restore operation.
            timestamp_to_restore: Find the latest backup at or before this time.

        Returns:
            An empty string "".
        """
        ix=bisect.bisect_left(sorted(list(self.back.keys())), timestamp_to_restore)
        t=sorted(list(self.back.keys()))[ix-1]
        self.data=self.back[t]["data"]
        self.expire=self.back[t]["expire"]
        return ""
