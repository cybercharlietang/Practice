"""
Abstract base class for IntegerContainer.
DO NOT MODIFY THIS FILE.
"""
from abc import ABC, abstractmethod


class IntegerContainer(ABC):
    """
    Abstract base class defining the interface for an integer container.
    
    Implement all abstract methods in IntegerContainerImpl.
    """
    
    @abstractmethod
    def add(self, value: int) -> int:
        """
        Add the specified integer value to the container.
        
        Args:
            value: The integer to add to the container.
            
        Returns:
            The number of integers in the container after the addition.
        """
        pass
    
    @abstractmethod
    def delete(self, value: int) -> bool:
        """
        Attempt to remove the specified integer value from the container.
        
        Args:
            value: The integer to remove from the container.
            
        Returns:
            True if the value was present and removed, False otherwise.
        """
        pass
    
    @abstractmethod
    def get_median(self) -> float:
        """
        Get the median of all integers currently in the container.
        
        Returns:
            The median value. If even number of elements, return average of
            the two middle elements. If container is empty, return -1.
        """
        pass
