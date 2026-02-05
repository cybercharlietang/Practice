# PS-05: Data Structures
# Target: 45-60 minutes for all 5 problems
# Priority: Correctness > Speed > Elegance

from collections import deque
import bisect
from webbrowser import open_new
from collections import defaultdict

# Provided for linked list problems
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def valid_parentheses(s: str) -> bool:
    """
    Checks if a string containing only '(', ')', '[', ']', '{', '}' is valid.
    A string is valid if every opening bracket has a matching closing bracket
    of the same type, closed in the correct order.

    :param s: str containing only bracket characters
    :return: True if valid, False otherwise. Empty string is valid.
    """
    if not s:
        return True
    stack=[]
    d={')': '(', ']': '[', '}': '{'}
    for string in s:
        if string in set("({["):
            stack.append(string)
        elif string in set(")}]"):
            if stack.pop() != d[string]:
                return False
    if stack:
        return False
    return True



class MinStack:
    """
    A stack that supports push, pop, top, and retrieving the minimum element,
    all in O(1) time.
    """

    def __init__(self):
        self.stack=[]

    def push(self, val: int) -> None:
        """
        Pushes the value onto the stack.

        :param val: int
        """
        self.stack.append(val)

    def pop(self) -> None:
        """
        Removes the top element from the stack.
        """
        self.stack.pop()

    def top(self) -> int:
        """
        Returns the top element without removing it.

        :return: The top element.
        """
        return self.stack[-1]

    def get_min(self) -> int:
        """
        Returns the minimum element currently in the stack.

        :return: The minimum element.
        """
        return min(self.stack)


def reverse_linked_list(head: ListNode) -> ListNode:
    """
    Reverses a singly linked list in-place.

    :param head: The head node of the list, or None if empty.
    :return: The new head of the reversed list, or None if empty.
    """
    prev = None                                                                                                            
    curr = head                                                                                                            
    while curr:                                                                                                            
        next_node = curr.next                                                                                              
        curr.next = prev                                                                                                   
        prev = curr                                                                                                        
        curr = next_node                                                                                                   
    return prev



class SortedList:
    """
    A list that maintains elements in sorted order and supports range queries.
    Duplicates are allowed.
    """

    def __init__(self):
        self.list=[]

    def insert(self, val: int) -> None:
        """
        Inserts val into the list, maintaining sorted order.

        :param val: int
        """
        bisect.insort(self.list, val)
        
            

    def remove(self, val: int) -> bool:
        """
        Removes the first occurrence of val from the list.

        :param val: int
        :return: True if val was found and removed, False otherwise.
        """
        for i in range(len(self.list)):
            if self.list[i]==val:
                self.list.pop(i)
                return True
        return False

    def count_range(self, low: int, high: int) -> int:
        """
        Counts elements in the inclusive range [low, high]
        :param low: int, lower bound (inclusive)
        :param high: int, upper bound (inclusive)
        :return: Number of elements x where low <= x <= high.
        """
        left=bisect.bisect_left(self.list, low)
        right=bisect.bisect_right(self.list, high)
        return right-left
            

    def get_all(self) -> list:
        """
        Returns all elements as a sorted list.

        :return: List of all elements in sorted order.
        """
        return self.list


class RecentCounter:
    """
    Counts the number of requests received in the last 3000 milliseconds.
    """

    def __init__(self):
        self.requests=[]

    def ping(self, t: int) -> int:
        """
        Records a new request at time t and returns the number of requests
        in the time range [t - 3000, t] (inclusive).

        :param t: int, timestamp in milliseconds. Calls are strictly increasing.
        :return: Number of requests in the last 3000ms window.
        """
        
        self.requests.append(t)
        while self.requests[0]<t-3000:
            self.requests.pop(0)
        return len(self.requests)