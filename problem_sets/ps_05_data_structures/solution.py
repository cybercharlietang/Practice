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
    new_head=head.next
    new_val=head.val
    head.val=new_head
    head.val=new_val
    return head.val



class SortedList:
    """
    A list that maintains elements in sorted order and supports range queries.
    Duplicates are allowed.
    """

    def __init__(self):
        # TODO: Implement
        pass

    def insert(self, val: int) -> None:
        """
        Inserts val into the list, maintaining sorted order.

        :param val: int
        """
        # TODO: Implement
        pass

    def remove(self, val: int) -> bool:
        """
        Removes the first occurrence of val from the list.

        :param val: int
        :return: True if val was found and removed, False otherwise.
        """
        # TODO: Implement
        pass

    def count_range(self, low: int, high: int) -> int:
        """
        Counts elements in the inclusive range [low, high].

        :param low: int, lower bound (inclusive)
        :param high: int, upper bound (inclusive)
        :return: Number of elements x where low <= x <= high.
        """
        # TODO: Implement
        pass

    def get_all(self) -> list:
        """
        Returns all elements as a sorted list.

        :return: List of all elements in sorted order.
        """
        # TODO: Implement
        pass


class RecentCounter:
    """
    Counts the number of requests received in the last 3000 milliseconds.
    """

    def __init__(self):
        # TODO: Implement
        pass

    def ping(self, t: int) -> int:
        """
        Records a new request at time t and returns the number of requests
        in the time range [t - 3000, t] (inclusive).

        :param t: int, timestamp in milliseconds. Calls are strictly increasing.
        :return: Number of requests in the last 3000ms window.
        """
        # TODO: Implement
        pass
