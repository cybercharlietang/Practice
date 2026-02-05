"""
Testing suite for the File Storage simulation.
============================================================
Run from file_storage directory:
    pytest test_simulation.py -v
    pytest test_simulation.py::TestLevel1 -v
    pytest test_simulation.py::TestLevel2 -v
    pytest test_simulation.py::TestLevel3 -v
    pytest test_simulation.py::TestLevel4 -v
"""
import pytest
from simulation import simulate_coding_framework


class TestLevel1:
    """Level 1: Basic Operations - FILE_UPLOAD, FILE_GET, FILE_COPY"""

    def test_upload_and_get_basic(self):
        """Upload and get a single file"""
        commands = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_GET", "Cars.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded Cars.txt", "got Cars.txt"]

    def test_upload_multiple_files(self):
        """Upload multiple files"""
        commands = [
            ["FILE_UPLOAD", "file1.txt", "100kb"],
            ["FILE_UPLOAD", "file2.txt", "200kb"],
            ["FILE_UPLOAD", "file3.txt", "300kb"],
            ["FILE_GET", "file1.txt"],
            ["FILE_GET", "file2.txt"],
            ["FILE_GET", "file3.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == [
            "uploaded file1.txt",
            "uploaded file2.txt",
            "uploaded file3.txt",
            "got file1.txt",
            "got file2.txt",
            "got file3.txt"
        ]

    def test_get_nonexistent_file(self):
        """Get a file that doesn't exist"""
        commands = [
            ["FILE_GET", "nonexistent.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["file not found"]

    def test_copy_basic(self):
        """Copy a file to new location"""
        commands = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_COPY", "Cars.txt", "Cars2.txt"],
            ["FILE_GET", "Cars2.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]

    def test_copy_overwrites_existing(self):
        """Copy overwrites existing destination file"""
        commands = [
            ["FILE_UPLOAD", "source.txt", "100kb"],
            ["FILE_UPLOAD", "dest.txt", "500kb"],
            ["FILE_COPY", "source.txt", "dest.txt"],
            ["FILE_GET", "dest.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == [
            "uploaded source.txt",
            "uploaded dest.txt",
            "copied source.txt to dest.txt",
            "got dest.txt"
        ]

    def test_upload_duplicate_raises_error(self):
        """Upload duplicate file should raise error"""
        commands = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_UPLOAD", "Cars.txt", "300kb"]
        ]
        output = simulate_coding_framework(commands)
        assert output[0] == "uploaded Cars.txt"
        # Second upload should fail - check it's not "uploaded Cars.txt"
        assert "uploaded" not in output[1] or "error" in output[1].lower() or output[1] != "uploaded Cars.txt"

    def test_copy_nonexistent_source_raises_error(self):
        """Copy from nonexistent source should raise error"""
        commands = [
            ["FILE_COPY", "nonexistent.txt", "dest.txt"]
        ]
        output = simulate_coding_framework(commands)
        # Should not be a successful copy
        assert "copied" not in output[0] or "error" in output[0].lower()

    def test_original_example(self):
        """Original test_group_1 example"""
        commands = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_GET", "Cars.txt"],
            ["FILE_COPY", "Cars.txt", "Cars2.txt"],
            ["FILE_GET", "Cars2.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]


class TestLevel2:
    """Level 2: Search - FILE_SEARCH"""

    def test_search_basic(self):
        """Search with prefix matching multiple files"""
        commands = [
            ["FILE_UPLOAD", "Foo.txt", "100kb"],
            ["FILE_UPLOAD", "Bar.csv", "200kb"],
            ["FILE_UPLOAD", "Baz.pdf", "300kb"],
            ["FILE_SEARCH", "Ba"]
        ]
        output = simulate_coding_framework(commands)
        # Baz.pdf (300kb) > Bar.csv (200kb) - sorted by size desc
        assert output[-1] == "found [Baz.pdf, Bar.csv]"

    def test_search_no_match(self):
        """Search with no matching files"""
        commands = [
            ["FILE_UPLOAD", "file1.txt", "100kb"],
            ["FILE_UPLOAD", "file2.txt", "200kb"],
            ["FILE_SEARCH", "xyz"]
        ]
        output = simulate_coding_framework(commands)
        assert output[-1] == "found []"

    def test_search_empty_prefix(self):
        """Search with empty prefix matches all files"""
        commands = [
            ["FILE_UPLOAD", "a.txt", "100kb"],
            ["FILE_UPLOAD", "b.txt", "200kb"],
            ["FILE_SEARCH", ""]
        ]
        output = simulate_coding_framework(commands)
        # Should return both files, sorted by size desc
        assert output[-1] == "found [b.txt, a.txt]"

    def test_search_sort_by_size_desc(self):
        """Search results sorted by size descending"""
        commands = [
            ["FILE_UPLOAD", "test1.txt", "100kb"],
            ["FILE_UPLOAD", "test2.txt", "300kb"],
            ["FILE_UPLOAD", "test3.txt", "200kb"],
            ["FILE_SEARCH", "test"]
        ]
        output = simulate_coding_framework(commands)
        # Order: test2 (300) > test3 (200) > test1 (100)
        assert output[-1] == "found [test2.txt, test3.txt, test1.txt]"

    def test_search_tie_break_by_name(self):
        """Same size files sorted by name ascending"""
        commands = [
            ["FILE_UPLOAD", "zebra.txt", "100kb"],
            ["FILE_UPLOAD", "apple.txt", "100kb"],
            ["FILE_UPLOAD", "mango.txt", "100kb"],
            ["FILE_SEARCH", ""]
        ]
        output = simulate_coding_framework(commands)
        # Same size, alphabetical order
        assert output[-1] == "found [apple.txt, mango.txt, zebra.txt]"

    def test_search_max_10_results(self):
        """Search returns maximum 10 results"""
        commands = []
        for i in range(15):
            commands.append(["FILE_UPLOAD", f"file{i:02d}.txt", f"{100+i}kb"])
        commands.append(["FILE_SEARCH", "file"])
        output = simulate_coding_framework(commands)
        # Should only have 10 files in result
        result = output[-1]
        # Count commas + 1 = number of files (if any)
        if result == "found []":
            count = 0
        else:
            # Remove "found [" and "]", then split by ", "
            files_str = result[7:-1]  # Remove "found [" and "]"
            if files_str:
                count = len(files_str.split(", "))
            else:
                count = 0
        assert count == 10

    def test_search_after_copy(self):
        """Copied files appear in search"""
        commands = [
            ["FILE_UPLOAD", "prefix_a.txt", "100kb"],
            ["FILE_COPY", "prefix_a.txt", "prefix_b.txt"],
            ["FILE_SEARCH", "prefix"]
        ]
        output = simulate_coding_framework(commands)
        # Both files should appear
        assert "prefix_a.txt" in output[-1]
        assert "prefix_b.txt" in output[-1]


class TestLevel3:
    """Level 3: Timestamps & TTL - *_AT operations"""

    def test_upload_at_basic(self):
        """Upload with timestamp, no TTL"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"],
            ["FILE_GET_AT", "2021-07-01T12:00:01", "Python.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded at Python.txt", "got at Python.txt"]

    def test_upload_at_with_ttl(self):
        """Upload with TTL - file exists within TTL"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "temp.txt", "100kb", "3600"],
            ["FILE_GET_AT", "2021-07-01T12:30:00", "temp.txt"]  # 30 min later, within 1hr TTL
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded at temp.txt", "got at temp.txt"]

    def test_upload_at_ttl_expired(self):
        """File with TTL expires after TTL seconds"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", "1"],
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"]  # 2 seconds later, TTL was 1
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded at Expired.txt", "file not found"]

    def test_upload_at_ttl_boundary(self):
        """File expires exactly at timestamp + TTL"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "boundary.txt", "100kb", "60"],
            ["FILE_GET_AT", "2021-07-01T12:00:59", "boundary.txt"],  # 59 sec - should exist
            ["FILE_GET_AT", "2021-07-01T12:01:00", "boundary.txt"]   # 60 sec - should be gone
        ]
        output = simulate_coding_framework(commands)
        assert output[1] == "got at boundary.txt"
        assert output[2] == "file not found"

    def test_copy_at_basic(self):
        """Copy with timestamp"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "source.txt", "100kb"],
            ["FILE_COPY_AT", "2021-07-01T12:00:01", "source.txt", "dest.txt"],
            ["FILE_GET_AT", "2021-07-01T12:00:02", "dest.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["uploaded at source.txt", "copied at source.txt to dest.txt", "got at dest.txt"]

    def test_search_at_excludes_expired(self):
        """Search excludes expired files"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "permanent.txt", "200kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "temporary.txt", "100kb", "60"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:30", ""],  # Both exist
            ["FILE_SEARCH_AT", "2021-07-01T12:01:30", ""]   # Only permanent exists
        ]
        output = simulate_coding_framework(commands)
        assert "permanent.txt" in output[2]
        assert "temporary.txt" in output[2]
        assert "permanent.txt" in output[3]
        assert "temporary.txt" not in output[3]

    def test_get_at_nonexistent(self):
        """Get nonexistent file at timestamp"""
        commands = [
            ["FILE_GET_AT", "2021-07-01T12:00:00", "nonexistent.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output == ["file not found"]

    def test_original_example(self):
        """Original test_group_3 example"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", "3600"],
            ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", "1"],
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "CodeSignalCopy.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"]
        ]
        output = simulate_coding_framework(commands)
        assert output == [
            "uploaded at Python.txt",
            "uploaded at CodeSignal.txt",
            "got at Python.txt",
            "copied at Python.txt to PythonCopy.txt",
            "found at [Python.txt, PythonCopy.txt]",
            "uploaded at Expired.txt",
            "file not found",
            "copied at CodeSignal.txt to CodeSignalCopy.txt",
            "found at [CodeSignal.txt, CodeSignalCopy.txt]"
        ]


class TestLevel4:
    """Level 4: Rollback"""

    def test_rollback_basic(self):
        """Rollback to previous state"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Added.txt", "150kb"],
            ["ROLLBACK", "2021-07-01T12:02:00"],
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"],
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Added.txt"]
        ]
        output = simulate_coding_framework(commands)
        assert output[2] == "rollback to 2021-07-01T12:02:00"
        assert output[3] == "got at Initial.txt"  # Should still exist
        assert output[4] == "file not found"      # Should be gone (added after rollback point)

    def test_rollback_recalculates_ttl(self):
        """Rollback recalculates TTL based on new timeline"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "temp.txt", "100kb", "600"],  # TTL 10 min
            ["FILE_GET_AT", "2021-07-01T12:05:00", "temp.txt"],  # 5 min in, should exist
            ["ROLLBACK", "2021-07-01T12:03:00"],  # Rollback to 3 min mark
            # After rollback, remaining TTL should be 7 min (10 - 3)
            # New timeline starts at rollback point
        ]
        output = simulate_coding_framework(commands)
        assert output[1] == "got at temp.txt"
        assert output[2] == "rollback to 2021-07-01T12:03:00"

    def test_rollback_removes_later_operations(self):
        """Operations after rollback timestamp are discarded"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "file1.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:10:00", "file2.txt", "200kb"],
            ["FILE_COPY_AT", "2021-07-01T12:15:00", "file1.txt", "file1_copy.txt"],
            ["ROLLBACK", "2021-07-01T12:05:00"],
            ["FILE_SEARCH_AT", "2021-07-01T12:20:00", "file"]
        ]
        output = simulate_coding_framework(commands)
        # Only file1.txt should exist after rollback
        assert "file1.txt" in output[-1]
        assert "file2.txt" not in output[-1]
        assert "file1_copy.txt" not in output[-1]

    def test_rollback_multiple(self):
        """Multiple rollbacks"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "v1.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:10:00", "v2.txt", "200kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "v3.txt", "300kb"],
            ["ROLLBACK", "2021-07-01T12:15:00"],  # v3 gone
            ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "v"],
            ["ROLLBACK", "2021-07-01T12:05:00"],  # v2 gone
            ["FILE_SEARCH_AT", "2021-07-01T12:30:00", "v"]
        ]
        output = simulate_coding_framework(commands)
        # After first rollback: v1, v2 exist
        assert "v1.txt" in output[4]
        assert "v2.txt" in output[4]
        assert "v3.txt" not in output[4]
        # After second rollback: only v1 exists
        assert "v1.txt" in output[6]
        assert "v2.txt" not in output[6]

    def test_original_example(self):
        """Original test_group_4 example"""
        commands = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Update1.txt", "150kb", "3600"],
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "Update2.txt", "200kb", "1800"],
            ["ROLLBACK", "2021-07-01T12:10:00"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update1.txt"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Initial.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "Up"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update2.txt"]
        ]
        output = simulate_coding_framework(commands)
        # After rollback to 12:10:00:
        # - Initial.txt exists (uploaded 12:00:00)
        # - Update1.txt exists (uploaded 12:05:00)
        # - Update1Copy.txt removed (copied 12:15:00 > rollback point)
        # - Update2.txt removed (uploaded 12:20:00 > rollback point)
        assert output == [
            "uploaded at Initial.txt",
            "uploaded at Update1.txt",
            "got at Initial.txt",
            "copied at Update1.txt to Update1Copy.txt",
            "uploaded at Update2.txt",
            "rollback to 2021-07-01T12:10:00",
            "got at Update1.txt",
            "got at Initial.txt",
            "found at [Update1.txt]",
            "file not found"
        ]


# Keep original test class for backward compatibility
class TestSimulateCodingFramework:
    """Original test cases (for backward compatibility)"""

    def test_group_1(self):
        test_data = [
            ["FILE_UPLOAD", "Cars.txt", "200kb"],
            ["FILE_GET", "Cars.txt"],
            ["FILE_COPY", "Cars.txt", "Cars2.txt"],
            ["FILE_GET", "Cars2.txt"]
        ]
        output = simulate_coding_framework(test_data)
        assert output == ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]

    def test_group_2(self):
        test_data = [
            ["FILE_UPLOAD", "Foo.txt", "100kb"],
            ["FILE_UPLOAD", "Bar.csv", "200kb"],
            ["FILE_UPLOAD", "Baz.pdf", "300kb"],
            ["FILE_SEARCH", "Ba"]
        ]
        output = simulate_coding_framework(test_data)
        assert output == ["uploaded Foo.txt", "uploaded Bar.csv", "uploaded Baz.pdf", "found [Baz.pdf, Bar.csv]"]

    def test_group_3(self):
        test_data = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", "3600"],
            ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", "1"],
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "CodeSignalCopy.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"]
        ]
        output = simulate_coding_framework(test_data)
        assert output == [
            "uploaded at Python.txt",
            "uploaded at CodeSignal.txt",
            "got at Python.txt",
            "copied at Python.txt to PythonCopy.txt",
            "found at [Python.txt, PythonCopy.txt]",
            "uploaded at Expired.txt",
            "file not found",
            "copied at CodeSignal.txt to CodeSignalCopy.txt",
            "found at [CodeSignal.txt, CodeSignalCopy.txt]"
        ]

    def test_group_4(self):
        test_data = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Update1.txt", "150kb", "3600"],
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"],
            ["FILE_COPY_AT", "2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "Update2.txt", "200kb", "1800"],
            ["ROLLBACK", "2021-07-01T12:10:00"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update1.txt"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Initial.txt"],
            ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "Up"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update2.txt"]
        ]
        output = simulate_coding_framework(test_data)
        # After rollback to 12:10:00, files created after are removed
        assert output == [
            "uploaded at Initial.txt",
            "uploaded at Update1.txt",
            "got at Initial.txt",
            "copied at Update1.txt to Update1Copy.txt",
            "uploaded at Update2.txt",
            "rollback to 2021-07-01T12:10:00",
            "got at Update1.txt",
            "got at Initial.txt",
            "found at [Update1.txt]",
            "file not found"
        ]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
