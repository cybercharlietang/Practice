"""
Level 2 Tests - DO NOT MODIFY
Tests for get_median() operation.
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


class TestLevel2(unittest.TestCase):
    """Level 2: Median operations."""
    
    def setUp(self):
        """Create a fresh container for each test."""
        self.container = IntegerContainerImpl()
    
    @timeout(0.5)
    def test_median_empty(self):
        """Median of empty container returns -1."""
        self.assertEqual(self.container.get_median(), -1)
    
    @timeout(0.5)
    def test_median_single(self):
        """Median of single element."""
        self.container.add(5)
        self.assertEqual(self.container.get_median(), 5.0)
    
    @timeout(0.5)
    def test_median_two_elements(self):
        """Median of two elements (average)."""
        self.container.add(5)
        self.container.add(10)
        self.assertEqual(self.container.get_median(), 7.5)
    
    @timeout(0.5)
    def test_median_three_elements(self):
        """Median of three elements (middle)."""
        self.container.add(5)
        self.container.add(10)
        self.container.add(3)
        self.assertEqual(self.container.get_median(), 5.0)
    
    @timeout(0.5)
    def test_median_four_elements(self):
        """Median of four elements (average of middle two)."""
        self.container.add(1)
        self.container.add(2)
        self.container.add(3)
        self.container.add(4)
        self.assertEqual(self.container.get_median(), 2.5)
    
    @timeout(0.5)
    def test_median_with_duplicates(self):
        """Median with duplicate values."""
        self.container.add(5)
        self.container.add(5)
        self.container.add(5)
        self.assertEqual(self.container.get_median(), 5.0)
    
    @timeout(0.5)
    def test_median_after_delete(self):
        """Median after deleting elements."""
        self.container.add(5)
        self.container.add(10)
        self.container.add(3)
        self.container.delete(5)
        # Remaining: [10, 3] -> median = 6.5
        self.assertEqual(self.container.get_median(), 6.5)
    
    @timeout(0.5)
    def test_median_after_delete_to_empty(self):
        """Median after deleting all elements."""
        self.container.add(5)
        self.container.delete(5)
        self.assertEqual(self.container.get_median(), -1)
    
    @timeout(0.5)
    def test_median_negative_numbers(self):
        """Median with negative numbers."""
        self.container.add(-5)
        self.container.add(-10)
        self.container.add(-3)
        # Sorted: [-10, -5, -3] -> median = -5
        self.assertEqual(self.container.get_median(), -5.0)
    
    @timeout(0.5)
    def test_median_mixed_signs(self):
        """Median with positive and negative numbers."""
        self.container.add(-10)
        self.container.add(0)
        self.container.add(10)
        self.assertEqual(self.container.get_median(), 0.0)
    
    @timeout(0.5)
    def test_median_example_sequence(self):
        """Test the example sequence from the problem."""
        self.container.add(5)
        self.container.add(10)
        self.assertEqual(self.container.get_median(), 7.5)
        
        self.container.add(3)
        self.assertEqual(self.container.get_median(), 5.0)
        
        self.container.delete(5)
        self.assertEqual(self.container.get_median(), 6.5)
    
    @timeout(0.5)
    def test_median_does_not_modify(self):
        """Calling get_median should not modify the container."""
        self.container.add(1)
        self.container.add(2)
        self.container.add(3)
        
        self.container.get_median()
        self.container.get_median()
        
        # Container should still have 3 elements
        self.assertEqual(self.container.add(4), 4)
    
    @timeout(0.5)
    def test_median_large_values(self):
        """Median with large values."""
        self.container.add(10**9)
        self.container.add(-10**9)
        # Median of [10^9, -10^9] = 0.0
        self.assertEqual(self.container.get_median(), 0.0)
    
    @timeout(2.0)
    def test_median_many_elements(self):
        """Median with many elements for performance."""
        for i in range(1001):
            self.container.add(i)
        
        # Sorted: [0, 1, 2, ..., 1000] -> median = 500
        self.assertEqual(self.container.get_median(), 500.0)
    
    @timeout(2.0)
    def test_median_many_operations(self):
        """Interleaved add, delete, median operations."""
        for i in range(100):
            self.container.add(i)
        
        self.assertEqual(self.container.get_median(), 49.5)
        
        for i in range(50):
            self.container.delete(i)
        
        # Remaining: [50, 51, ..., 99] -> median = 74.5
        self.assertEqual(self.container.get_median(), 74.5)


if __name__ == '__main__':
    unittest.main()
