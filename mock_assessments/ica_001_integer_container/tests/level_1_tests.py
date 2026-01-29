"""
Level 1 Tests - DO NOT MODIFY
Tests for add() and delete() operations.
"""
import sys
import os
import unittest
from functools import wraps
import signal

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integer_container_impl import IntegerContainerImpl


class TimeoutError(Exception):
    pass


def timeout(seconds):
    """Decorator to add timeout to test methods."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise TimeoutError(f"Test timed out after {seconds} seconds")
            
            # Set the signal handler
            old_handler = signal.signal(signal.SIGALRM, handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, old_handler)
            
            return result
        return wrapper
    return decorator


class TestLevel1(unittest.TestCase):
    """Level 1: Basic add and delete operations."""
    
    def setUp(self):
        """Create a fresh container for each test."""
        self.container = IntegerContainerImpl()
    
    @timeout(0.5)
    def test_add_single(self):
        """Add a single element."""
        result = self.container.add(5)
        self.assertEqual(result, 1)
    
    @timeout(0.5)
    def test_add_multiple(self):
        """Add multiple different elements."""
        self.assertEqual(self.container.add(5), 1)
        self.assertEqual(self.container.add(10), 2)
        self.assertEqual(self.container.add(3), 3)
    
    @timeout(0.5)
    def test_add_duplicates(self):
        """Add duplicate elements - duplicates should be stored."""
        self.assertEqual(self.container.add(5), 1)
        self.assertEqual(self.container.add(5), 2)
        self.assertEqual(self.container.add(5), 3)
    
    @timeout(0.5)
    def test_add_negative(self):
        """Add negative numbers."""
        self.assertEqual(self.container.add(-5), 1)
        self.assertEqual(self.container.add(-10), 2)
        self.assertEqual(self.container.add(0), 3)
    
    @timeout(0.5)
    def test_add_zero(self):
        """Add zero."""
        self.assertEqual(self.container.add(0), 1)
        self.assertEqual(self.container.add(0), 2)
    
    @timeout(0.5)
    def test_delete_existing(self):
        """Delete an existing element."""
        self.container.add(5)
        self.container.add(10)
        result = self.container.delete(5)
        self.assertTrue(result)
    
    @timeout(0.5)
    def test_delete_nonexistent(self):
        """Delete a non-existent element."""
        self.container.add(5)
        result = self.container.delete(10)
        self.assertFalse(result)
    
    @timeout(0.5)
    def test_delete_from_empty(self):
        """Delete from empty container."""
        result = self.container.delete(5)
        self.assertFalse(result)
    
    @timeout(0.5)
    def test_delete_one_of_duplicates(self):
        """Delete only removes one instance of duplicates."""
        self.container.add(5)
        self.container.add(5)
        self.container.add(5)
        
        self.assertTrue(self.container.delete(5))
        # Should still have 2 fives, so add should return 3
        self.assertEqual(self.container.add(1), 3)
    
    @timeout(0.5)
    def test_delete_all_duplicates(self):
        """Delete all instances of a duplicate."""
        self.container.add(5)
        self.container.add(5)
        
        self.assertTrue(self.container.delete(5))
        self.assertTrue(self.container.delete(5))
        self.assertFalse(self.container.delete(5))
    
    @timeout(0.5)
    def test_example_sequence(self):
        """Test the example sequence from the problem."""
        self.assertEqual(self.container.add(5), 1)      # [5]
        self.assertEqual(self.container.add(10), 2)     # [5, 10]
        self.assertEqual(self.container.add(5), 3)      # [5, 10, 5]
        self.assertTrue(self.container.delete(10))      # [5, 5]
        self.assertFalse(self.container.delete(1))      # [5, 5]
        self.assertEqual(self.container.add(1), 3)      # [5, 5, 1]
    
    @timeout(0.5)
    def test_mixed_operations(self):
        """Mix of add and delete operations."""
        self.assertEqual(self.container.add(1), 1)
        self.assertEqual(self.container.add(2), 2)
        self.assertEqual(self.container.add(3), 3)
        self.assertTrue(self.container.delete(2))
        self.assertEqual(self.container.add(4), 3)
        self.assertTrue(self.container.delete(1))
        self.assertEqual(self.container.add(5), 3)
    
    @timeout(0.5)
    def test_large_values(self):
        """Test with large integer values."""
        self.assertEqual(self.container.add(10**9), 1)
        self.assertEqual(self.container.add(-10**9), 2)
        self.assertTrue(self.container.delete(10**9))
        self.assertFalse(self.container.delete(10**9))
    
    @timeout(2.0)
    def test_many_operations(self):
        """Test with many operations for performance."""
        for i in range(1000):
            self.assertEqual(self.container.add(i), i + 1)
        
        for i in range(500):
            self.assertTrue(self.container.delete(i))
        
        self.assertEqual(self.container.add(9999), 501)


if __name__ == '__main__':
    unittest.main()
