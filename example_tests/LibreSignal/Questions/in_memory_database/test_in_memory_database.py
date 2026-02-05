"""
Testing suite for the In-Memory Database simulation.
============================================================
This suite uses pytest to validate the functionality of the in-memory database
simulation.

Run from LibreSignal root directory:
    pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel1 -v
    pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel2 -v
    pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel3 -v
    pytest Questions/in_memory_database/test_in_memory_database.py::TestLevel4 -v
"""
import pytest
from simulation import Simulation


class TestLevel1:
    """Level 1: Basic Operations - SET, GET, DELETE"""

    def test_set_and_get_basic(self):
        db = Simulation()
        result = db.set("A", "B", "E")
        assert result == ""
        assert db.get("A", "B") == "E"

    def test_set_multiple_fields(self):
        db = Simulation()
        db.set("A", "B", "E")
        db.set("A", "C", "F")
        assert db.get("A", "B") == "E"
        assert db.get("A", "C") == "F"

    def test_set_overwrite(self):
        db = Simulation()
        db.set("A", "B", "E")
        db.set("A", "B", "X")
        assert db.get("A", "B") == "X"

    def test_get_missing_record(self):
        db = Simulation()
        assert db.get("missing", "field") == ""

    def test_get_missing_field(self):
        db = Simulation()
        db.set("A", "B", "E")
        assert db.get("A", "D") == ""

    def test_delete_existing(self):
        db = Simulation()
        db.set("A", "B", "E")
        result = db.delete("A", "B")
        assert result == "true"
        assert db.get("A", "B") == ""

    def test_delete_missing_record(self):
        db = Simulation()
        assert db.delete("missing", "field") == "false"

    def test_delete_missing_field(self):
        db = Simulation()
        db.set("A", "B", "E")
        assert db.delete("A", "D") == "false"

    def test_multiple_records(self):
        db = Simulation()
        db.set("rec1", "f1", "v1")
        db.set("rec1", "f2", "v2")
        db.set("rec2", "f1", "v3")
        assert db.get("rec1", "f1") == "v1"
        assert db.get("rec1", "f2") == "v2"
        assert db.get("rec2", "f1") == "v3"

    def test_example_from_spec(self):
        db = Simulation()
        assert db.set("A", "B", "E") == ""
        assert db.set("A", "C", "F") == ""
        assert db.get("A", "B") == "E"
        assert db.get("A", "D") == ""
        assert db.delete("A", "B") == "true"
        assert db.delete("A", "D") == "false"


class TestLevel2:
    """Level 2: Scan Operations - SCAN, SCAN_BY_PREFIX"""

    def test_scan_basic(self):
        db = Simulation()
        db.set("A", "BC", "E")
        db.set("A", "BD", "F")
        db.set("A", "C", "G")
        result = db.scan("A")
        assert result == "BC(E), BD(F), C(G)"

    def test_scan_missing_record(self):
        db = Simulation()
        assert db.scan("missing") == ""

    def test_scan_single_field(self):
        db = Simulation()
        db.set("A", "field", "value")
        assert db.scan("A") == "field(value)"

    def test_scan_lexicographic_order(self):
        db = Simulation()
        db.set("A", "zebra", "1")
        db.set("A", "apple", "2")
        db.set("A", "mango", "3")
        assert db.scan("A") == "apple(2), mango(3), zebra(1)"

    def test_scan_by_prefix_basic(self):
        db = Simulation()
        db.set("A", "BC", "E")
        db.set("A", "BD", "F")
        db.set("A", "C", "G")
        result = db.scan_by_prefix("A", "B")
        assert result == "BC(E), BD(F)"

    def test_scan_by_prefix_no_match(self):
        db = Simulation()
        db.set("A", "BC", "E")
        assert db.scan_by_prefix("A", "X") == ""

    def test_scan_by_prefix_missing_record(self):
        db = Simulation()
        assert db.scan_by_prefix("missing", "B") == ""

    def test_scan_by_prefix_empty_prefix(self):
        db = Simulation()
        db.set("A", "B", "1")
        db.set("A", "C", "2")
        result = db.scan_by_prefix("A", "")
        assert result == "B(1), C(2)"

    def test_example_from_spec(self):
        db = Simulation()
        db.set("A", "BC", "E")
        db.set("A", "BD", "F")
        db.set("A", "C", "G")
        assert db.scan_by_prefix("A", "B") == "BC(E), BD(F)"
        assert db.scan("A") == "BC(E), BD(F), C(G)"
        assert db.scan_by_prefix("B", "B") == ""


class TestLevel3:
    """Level 3: Timestamp & TTL"""

    def test_set_at_basic(self):
        db = Simulation()
        db.set_at("A", "B", "C", 1)
        assert db.get_at("A", "B", 2) == "C"

    def test_set_at_with_ttl_basic(self):
        db = Simulation()
        db.set_at_with_ttl("A", "BC", "E", 1, 9)
        assert db.get_at("A", "BC", 5) == "E"
        assert db.get_at("A", "BC", 9) == "E"

    def test_set_at_with_ttl_expired(self):
        db = Simulation()
        db.set_at_with_ttl("A", "BC", "E", 1, 9)
        # TTL of 9 starting at 1 means valid during [1, 10)
        assert db.get_at("A", "BC", 10) == ""
        assert db.get_at("A", "BC", 15) == ""

    def test_set_at_with_ttl_overwrite(self):
        db = Simulation()
        db.set_at_with_ttl("A", "BC", "E", 1, 9)  # expires at 10
        db.set_at_with_ttl("A", "BC", "E", 5, 10)  # now expires at 15
        assert db.get_at("A", "BC", 14) == "E"
        assert db.get_at("A", "BC", 15) == ""

    def test_set_at_no_ttl_never_expires(self):
        db = Simulation()
        db.set_at("A", "BD", "F", 5)
        assert db.get_at("A", "BD", 1000000) == "F"

    def test_delete_at_basic(self):
        db = Simulation()
        db.set_at("A", "B", "C", 1)
        assert db.delete_at("A", "B", 2) == "true"
        assert db.get_at("A", "B", 3) == ""

    def test_delete_at_expired(self):
        db = Simulation()
        db.set_at_with_ttl("X", "Y", "Z", 2, 15)  # expires at 17
        assert db.delete_at("X", "Y", 20) == "false"

    def test_scan_at_basic(self):
        db = Simulation()
        db.set_at("A", "B", "C", 1)
        db.set_at_with_ttl("A", "D", "E", 4, 10)  # expires at 14
        assert db.scan_at("A", 13) == "B(C), D(E)"

    def test_scan_at_excludes_expired(self):
        db = Simulation()
        db.set_at_with_ttl("X", "Y", "Z", 2, 15)  # expires at 17
        assert db.scan_at("X", 16) == "Y(Z)"
        assert db.scan_at("X", 17) == ""

    def test_scan_by_prefix_at(self):
        db = Simulation()
        db.set_at_with_ttl("A", "BC", "E", 1, 9)  # expires at 10
        db.set_at("A", "BD", "F", 5)  # never expires
        assert db.scan_by_prefix_at("A", "B", 14) == "BD(F)"
        assert db.scan_by_prefix_at("A", "B", 15) == "BD(F)"

    def test_example_1_from_spec(self):
        db = Simulation()
        db.set_at_with_ttl("A", "BC", "E", 1, 9)
        db.set_at_with_ttl("A", "BC", "E", 5, 10)  # overwrite, now expires at 15
        db.set_at("A", "BD", "F", 5)
        assert db.scan_by_prefix_at("A", "B", 14) == "BC(E), BD(F)"
        assert db.scan_by_prefix_at("A", "B", 15) == "BD(F)"

    def test_example_2_from_spec(self):
        db = Simulation()
        db.set_at("A", "B", "C", 1)
        db.set_at_with_ttl("X", "Y", "Z", 2, 15)  # expires at 17
        assert db.get_at("X", "Y", 3) == "Z"
        db.set_at_with_ttl("A", "D", "E", 4, 10)  # expires at 14
        assert db.scan_at("A", 13) == "B(C), D(E)"
        assert db.scan_at("X", 16) == "Y(Z)"
        assert db.scan_at("X", 17) == ""
        assert db.delete_at("X", "Y", 20) == "false"


class TestLevel4:
    """Level 4: Backup & Restore"""

    def test_backup_basic(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 10)
        result = db.backup(3)
        assert result == "1"

    def test_backup_multiple_records(self):
        db = Simulation()
        db.set_at("A", "f1", "v1", 1)
        db.set_at("B", "f2", "v2", 2)
        db.set_at("C", "f3", "v3", 3)
        assert db.backup(4) == "3"

    def test_backup_excludes_expired(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 5)  # expires at 6
        db.set_at("B", "D", "E", 2)  # never expires
        assert db.backup(7) == "1"  # only B is valid

    def test_backup_empty_record_not_counted(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 5)  # expires at 6
        assert db.backup(10) == "0"

    def test_restore_basic(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 10)  # expires at 11
        db.backup(3)
        db.set_at("A", "D", "E", 4)
        db.restore(10, 7)  # restore to backup at 3
        # Field D should be gone, B should still exist
        assert db.get_at("A", "D", 11) == ""
        assert db.get_at("A", "B", 11) == "C"

    def test_restore_recalculates_ttl(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 10)  # expires at 11
        db.backup(3)  # remaining TTL = 10 - (3-1) = 8
        db.restore(10, 7)  # restore at timestamp 10, new expiry = 10 + 8 = 18
        assert db.get_at("A", "B", 17) == "C"
        assert db.get_at("A", "B", 18) == ""

    def test_restore_to_specific_backup(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 10)
        db.backup(3)
        db.set_at("A", "D", "E", 4)
        db.backup(5)
        db.delete_at("A", "B", 8)
        db.backup(9)
        # Restore to backup at 5 (latest at or before 7)
        db.restore(10, 7)
        assert db.scan_at("A", 11) == "B(C), D(E)"

    def test_example_from_spec(self):
        db = Simulation()
        db.set_at_with_ttl("A", "B", "C", 1, 10)  # expires at 11
        assert db.backup(3) == "1"
        db.set_at("A", "D", "E", 4)
        assert db.backup(5) == "1"
        assert db.delete_at("A", "B", 8) == "true"
        assert db.backup(9) == "1"
        # Restore to backup at 5: B had remaining TTL of 6 (11-5)
        # New expiry = 10 + 6 = 16
        assert db.restore(10, 7) == ""
        assert db.backup(11) == "1"
        assert db.scan_at("A", 15) == "B(C), D(E)"
        assert db.scan_at("A", 16) == "D(E)"
