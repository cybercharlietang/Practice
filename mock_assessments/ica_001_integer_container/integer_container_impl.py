"""
Your implementation of IntegerContainer.
EDIT THIS FILE to implement the required functionality.
"""
from integer_container import IntegerContainer


class IntegerContainerImpl(IntegerContainer):
    """
    Implement a simple container of integer numbers.
    
    Level 1: Implement add() and delete()
    Level 2: Implement get_median()
    """
    
    def __init__(self):
        # TODO: Initialize your data structure(s) here
        pass
    
    def add(self, value: int) -> int:
        """
        Add the specified integer value to the container.
        
        Args:
            value: The integer to add to the container.
            
        Returns:
            The number of integers in the container after the addition.
        """
        # TODO: Implement this method
        pass
    
    def delete(self, value: int) -> bool:
        """
        Attempt to remove the specified integer value from the container.
        
        Args:
            value: The integer to remove from the container.
            
        Returns:
            True if the value was present and removed, False otherwise.
        """
        # TODO: Implement this method
        pass
    
    def get_median(self) -> float:
        """
        Get the median of all integers currently in the container.
        
        Returns:
            The median value. If even number of elements, return average of
            the two middle elements. If container is empty, return -1.
        """
        # TODO: Implement this method (Level 2)
        pass
