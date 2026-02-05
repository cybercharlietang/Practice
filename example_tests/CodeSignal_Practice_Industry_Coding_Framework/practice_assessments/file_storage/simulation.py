"""
File Storage System Simulation
==============================
Run tests:
    pytest test_simulation.py -v
    pytest test_simulation.py::TestSimulateCodingFramework::test_group_1 -v
"""
import copy
from collections import OrderedDict
from fileinput import filename
from typing import Optional, List
from collections import defaultdict
from datetime import datetime, timedelta  

class FileStorage:
    """
    A simplified file hosting service.

    Level 1: FILE_UPLOAD, FILE_GET, FILE_COPY
    Level 2: FILE_SEARCH
    Level 3: *_AT variants with timestamps and TTL
    Level 4: ROLLBACK
    """

    def __init__(self):
        self.storage=defaultdict(defaultdict)

    # ==================== LEVEL 1: Basic Operations ====================

    def file_upload(self, file_name: str, size: str) -> str:
        """
        Upload a file to the remote storage server.

        Args:
            file_name: The name of the file to upload.
            size: The size of the file (e.g., "200kb").

        Returns:
            "uploaded {file_name}" on success.

        Raises:
            RuntimeError: If a file with the same name already exists.
        """
        if file_name in self.storage:
            raise RuntimeError
        self.storage[file_name]={"size": size}
        return "uploaded "+file_name

    def file_get(self, file_name: str) -> str:
        """
        Get the size of a file.

        Args:
            file_name: The name of the file to retrieve.

        Returns:
            "got {file_name}" if file exists.
            "file not found" if file doesn't exist.
        """
        if file_name not in self.storage:
            return "file not found"
        return "got "+file_name

    def file_copy(self, source: str, dest: str) -> str:
        """
        Copy a file to a new location.

        Args:
            source: The source file name.
            dest: The destination file name.

        Returns:
            "copied {source} to {dest}" on success.

        Raises:
            RuntimeError: If source file doesn't exist.

        Note:
            If destination file already exists, it is overwritten.
        """
        if source not in self.storage:
            raise RuntimeError
        self.storage[dest]=copy.deepcopy(self.storage[source])
        return "copied "+source+" to "+dest
        

    # ==================== LEVEL 2: Search ====================

    def file_search(self, prefix: str) -> str:
        """
        Find top 10 files starting with the provided prefix.

        Args:
            prefix: The prefix to search for.

        Returns:
            "found [{file1}, {file2}, ...]" with files sorted by:
            1. Size descending
            2. File name ascending (for ties)

            Maximum 10 results.
        """
        l=len(prefix)
        res = []
        for file in self.storage:
            if file[:l]==prefix:
                res.append((file, int(self.storage[file]["size"][:-2])))
        res_sort=sorted(res, key=lambda k: (-k[1],k[0]))
        final=[file for file, size in res_sort[:10]]
        return "found ["+", ".join(final)+"]"

    # ==================== LEVEL 3: Timestamps & TTL ====================
    def check_is_alive(self, timestamp, file_name):
        if self.storage[file_name]["ttl"]==None:
            return True
        current=datetime.fromisoformat(timestamp)
        upload_dt=datetime.fromisoformat(self.storage[file_name]["upload_time"])
        is_alive = current < upload_dt + timedelta(seconds=self.storage[file_name]["ttl"])
        return is_alive


    def file_upload_at(self, timestamp: str, file_name: str, size: str, ttl: Optional[int] = None) -> str:
        """
        Upload a file with timestamp and optional TTL.

        Args:
            timestamp: The timestamp of the operation (e.g., "2021-07-01T12:00:00").
            file_name: The name of the file to upload.
            size: The size of the file (e.g., "150kb").
            ttl: Optional time-to-live in seconds. None means infinite lifetime.

        Returns:
            "uploaded at {file_name}" on success.

        Raises:
            RuntimeError: If a file with the same name already exists (and is not expired).

        Note:
            File is available during [timestamp, timestamp + ttl) if ttl is specified.
        """
        if file_name in self.storage:
            if self.check_is_alive(timestamp, file_name):
                raise RuntimeError
        self.storage[file_name]={"size": size, "upload_time": timestamp, "ttl": ttl, "copy_time": None}
        return "uploaded at "+file_name

    def file_get_at(self, timestamp: str, file_name: str) -> str:
        """
        Get a file at a specific timestamp.

        Args:
            timestamp: The timestamp of the operation.
            file_name: The name of the file to retrieve.

        Returns:
            "got at {file_name}" if file exists and is not expired.
            "file not found" if file doesn't exist or is expired.
        """
        if file_name not in self.storage:
            return "file not found"
        if not self.check_is_alive(timestamp, file_name):
            return "file not found"
        return "got at "+file_name

    def file_copy_at(self, timestamp: str, source: str, dest: str) -> str:
        """
        Copy a file at a specific timestamp.

        Args:
            timestamp: The timestamp of the operation.
            source: The source file name.
            dest: The destination file name.

        Returns:
            "copied at {source} to {dest}" on success.

        Raises:
            RuntimeError: If source file doesn't exist or is expired.

        Note:
            Copied file inherits the TTL/expiration of the source file.
        """
        if source not in self.storage:
            raise RuntimeError
        elif not self.check_is_alive(timestamp, source):
            raise RuntimeError
        self.storage[dest]=copy.deepcopy(self.storage[source])
        self.storage[dest]["copy_time"]=timestamp
        return "copied at "+source+" to "+dest


    def file_search_at(self, timestamp: str, prefix: str) -> str:
        """
        Search for files at a specific timestamp.

        Args:
            timestamp: The timestamp of the operation.
            prefix: The prefix to search for.

        Returns:
            "found at [{file1}, {file2}, ...]" with only non-expired files.
            Sorted by size descending, then file name ascending.
            Maximum 10 results.
        """
        l=len(prefix)
        res = []
        for file in self.storage:
            if file[:l]==prefix:
                if self.check_is_alive(timestamp, file):
                    res.append((file, int(self.storage[file]["size"][:-2])))
        res_sort=sorted(res, key=lambda k: (-k[1],k[0]))
        final=[file for file, size in res_sort[:10]]
        return "found at ["+", ".join(final)+"]"

    # ==================== LEVEL 4: Rollback ====================

    def rollback(self, timestamp: str) -> str:
        """
        Rollback the file storage state to a previous timestamp.

        Args:
            timestamp: The timestamp to rollback to.

        Returns:
            "rollback to {timestamp}"

        Note:
            - Restores the state as it was at the given timestamp.
            - All TTLs should be recalculated accordingly.
            - Operations after the rollback timestamp are discarded.
        """
        for file in list(self.storage.keys()):
            if self.storage[file]["upload_time"]> timestamp:
                self.storage.pop(file)
            elif self.storage[file]["copy_time"]:
                if self.storage[file]["copy_time"]> timestamp:
                    self.storage.pop(file)
            else:
                ttl=self.storage[file]["ttl"]
                if ttl is not None:
                    self.storage[file]["ttl"]=(timedelta(seconds=ttl)+datetime.fromisoformat(self.storage[file]["upload_time"])-datetime.fromisoformat(timestamp)).total_seconds()
                    self.storage[file]["restore_time"]=timestamp
        return "rollback to "+timestamp


def simulate_coding_framework(commands: List[List[str]]) -> List[str]:
    """
    Process a list of file storage commands.

    Args:
        commands: List of commands, each command is a list of strings.
                  e.g., [["FILE_UPLOAD", "Cars.txt", "200kb"],
                        = ["FILE_GET", "Cars.txt"]]

    Returns:
        List of result strings for each command.

    Command formats:
        Level 1:
            ["FILE_UPLOAD", file_name, size]
            ["FILE_GET", file_name]
            ["FILE_COPY", source, dest]
        Level 2:
            ["FILE_SEARCH", prefix]
        Level 3:
            ["FILE_UPLOAD_AT", timestamp, file_name, size]
            ["FILE_UPLOAD_AT", timestamp, file_name, size, ttl]
            ["FILE_GET_AT", timestamp, file_name]
            ["FILE_COPY_AT", timestamp, source, dest]
            ["FILE_SEARCH_AT", timestamp, prefix]
        Level 4:
            ["ROLLBACK", timestamp]
    """
    storage = FileStorage()
    results = []

    for cmd in commands:
        operation = cmd[0]

        try:
            if operation == "FILE_UPLOAD":
                result = storage.file_upload(cmd[1], cmd[2])
            elif operation == "FILE_GET":
                result = storage.file_get(cmd[1])
            elif operation == "FILE_COPY":
                result = storage.file_copy(cmd[1], cmd[2])
            elif operation == "FILE_SEARCH":
                result = storage.file_search(cmd[1])
            elif operation == "FILE_UPLOAD_AT":
                if len(cmd) == 5:
                    result = storage.file_upload_at(cmd[1], cmd[2], cmd[3], int(cmd[4]))
                else:
                    result = storage.file_upload_at(cmd[1], cmd[2], cmd[3])
            elif operation == "FILE_GET_AT":
                result = storage.file_get_at(cmd[1], cmd[2])
            elif operation == "FILE_COPY_AT":
                result = storage.file_copy_at(cmd[1], cmd[2], cmd[3])
            elif operation == "FILE_SEARCH_AT":
                result = storage.file_search_at(cmd[1], cmd[2])
            elif operation == "ROLLBACK":
                result = storage.rollback(cmd[1])
            else:
                result = f"unknown operation: {operation}"

            results.append(result)
        except RuntimeError as e:
            results.append(str(e))

    return results
