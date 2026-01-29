"""
SOLUTIONS - DO NOT LOOK AT THIS FILE UNTIL YOU'VE ATTEMPTED THE PROBLEM!

This file contains reference solutions for the Integer Container problem.
"""
from integer_container import IntegerContainer


# =============================================================================
# SOLUTION 1: Simple List-based Solution (O(n) median)
# =============================================================================
class IntegerContainerSimple(IntegerContainer):
    """
    Simple solution using a list.
    
    Time Complexity:
    - add: O(1)
    - delete: O(n)
    - get_median: O(n log n) due to sorting
    
    This solution is sufficient to pass all tests.
    """
    
    def __init__(self):
        self.data = []
    
    def add(self, value: int) -> int:
        self.data.append(value)
        return len(self.data)
    
    def delete(self, value: int) -> bool:
        if value in self.data:
            self.data.remove(value)
            return True
        return False
    
    def get_median(self) -> float:
        if not self.data:
            return -1
        
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        
        if n % 2 == 1:
            return float(sorted_data[mid])
        else:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2


# =============================================================================
# SOLUTION 2: Two-Heap Solution (O(log n) median)
# =============================================================================
import heapq


class IntegerContainerOptimized(IntegerContainer):
    """
    Optimized solution using two heaps for O(log n) median access.
    
    Time Complexity:
    - add: O(log n)
    - delete: O(n) for finding + O(log n) for rebalancing
    - get_median: O(1)
    
    This is more efficient for frequent median queries.
    """
    
    def __init__(self):
        self.max_heap = []  # Left half (negated for max-heap behavior)
        self.min_heap = []  # Right half
        self.count = 0
    
    def add(self, value: int) -> int:
        # Add to appropriate heap
        if not self.max_heap or value <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -value)
        else:
            heapq.heappush(self.min_heap, value)
        
        # Rebalance
        self._rebalance()
        
        self.count += 1
        return self.count
    
    def delete(self, value: int) -> bool:
        # Try to remove from max_heap (left half)
        if -value in [-x for x in self.max_heap]:
            self.max_heap.remove(-value)
            heapq.heapify(self.max_heap)
            self._rebalance()
            self.count -= 1
            return True
        
        # Try to remove from min_heap (right half)
        if value in self.min_heap:
            self.min_heap.remove(value)
            heapq.heapify(self.min_heap)
            self._rebalance()
            self.count -= 1
            return True
        
        return False
    
    def get_median(self) -> float:
        if self.count == 0:
            return -1
        
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2
        else:
            return float(-self.max_heap[0])
    
    def _rebalance(self):
        # Ensure max_heap has at most 1 more element than min_heap
        while len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        while len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))


# =============================================================================
# Test the solutions
# =============================================================================
if __name__ == '__main__':
    print("Testing Simple Solution:")
    c1 = IntegerContainerSimple()
    print(f"add(5) = {c1.add(5)}")      # 1
    print(f"add(10) = {c1.add(10)}")    # 2
    print(f"get_median() = {c1.get_median()}")  # 7.5
    print(f"add(3) = {c1.add(3)}")      # 3
    print(f"get_median() = {c1.get_median()}")  # 5.0
    print(f"delete(5) = {c1.delete(5)}")  # True
    print(f"get_median() = {c1.get_median()}")  # 6.5
    
    print("\nTesting Optimized Solution:")
    c2 = IntegerContainerOptimized()
    print(f"add(5) = {c2.add(5)}")      # 1
    print(f"add(10) = {c2.add(10)}")    # 2
    print(f"get_median() = {c2.get_median()}")  # 7.5
    print(f"add(3) = {c2.add(3)}")      # 3
    print(f"get_median() = {c2.get_median()}")  # 5.0
    print(f"delete(5) = {c2.delete(5)}")  # True
    print(f"get_median() = {c2.get_median()}")  # 6.5
