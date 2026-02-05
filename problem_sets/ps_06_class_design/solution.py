# PS-06: Class Design
# Target: 60-90 minutes for all 5 problems
# Priority: Correctness > Speed > Elegance

from collections import OrderedDict, defaultdict
from re import T


class Counter:
    """
    A counter that tracks increments/decrements and provides statistics.
    """

    def __init__(self):
        """Initialize the counter with value 0."""
        self.counter=0
        self.increments=0
        self.decrements=0
        self.counter_value=[0]

    def increment(self, amount: int = 1) -> int:
        """
        Increment the counter by amount (default 1).

        :param amount: Positive integer to add
        :return: New counter value
        """
        self.counter+=amount
        self.increments+=1
        self.counter_value.append(self.counter)
        return self.counter

    def decrement(self, amount: int = 1) -> int:
        """
        Decrement the counter by amount (default 1).

        :param amount: Positive integer to subtract
        :return: New counter value
        """
        self.counter-=amount
        self.decrements+=1
        self.counter_value.append(self.counter)
        return self.counter

    def get_value(self) -> int:
        """Return the current counter value."""
        return self.counter

    def get_stats(self) -> dict:
        """
        Return statistics about counter usage.

        :return: Dict with keys "total_increments", "total_decrements", "max_value", "min_value"
        """
        statistics={}
        statistics["total_increments"]=self.increments
        statistics["total_decrements"]=self.decrements
        statistics["max_value"]=max(self.counter_value)
        statistics["min_value"]=min(self.counter_value)
        return statistics

    def reset(self) -> None:
        """Reset counter to 0 but keep statistics."""
        self.counter=0


class LRUCache:
    """
    Least Recently Used (LRU) cache with fixed capacity.
    When capacity is exceeded, the least recently used item is evicted.
    """

    def __init__(self, capacity: int):
        """
        Initialize the cache with given capacity.

        :param capacity: Maximum number of items to store (>= 1)
        """
        self.cache={}
        self.capacity=capacity
        self.usage=[]

    def get(self, key: str) -> int:
        """
        Get the value for key. Returns -1 if key doesn't exist.
        Accessing a key makes it most recently used.

        :param key: The key to look up
        :return: The value, or -1 if not found
        """
        if key in self.cache:
            self.usage.remove(key)
            self.usage.append(key)
            return self.cache[key]
        return -1

    def put(self, key: str, value: int) -> None:
        """
        Insert or update key-value pair.
        If cache is at capacity, evict the least recently used item first.

        :param key: The key
        :param value: The value
        """
        if key in self.cache:
            self.usage.remove(key)
            self.usage.append(key)
            self.cache[key]=value
        else:
            self.usage.append(key)
            self.cache[key]=value
        if len(self.cache)>self.capacity:
            self.cache.pop(self.usage.pop(0))

    def size(self) -> int:
        """Return current number of items in cache."""
        return len(self.cache)


class RateLimiter:
    """
    Sliding window rate limiter.
    Allows up to `max_requests` in any `window_seconds` period.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize rate limiter.

        :param max_requests: Maximum requests allowed in window
        :param window_seconds: Size of sliding window in seconds
        """
        self.max_requests=max_requests
        self.window_seconds=window_seconds
        self.record=[]

    def allow_request(self, timestamp: int) -> bool:
        """
        Check if a request at given timestamp should be allowed.
        If allowed, record the request.

        :param timestamp: Current timestamp in seconds
        :return: True if request is allowed, False if rate limited
        """
        record_new=self.record[:]
        record_new.append(timestamp)
        while record_new[0]<timestamp-self.window_seconds:
            record_new.pop(0)
        if len(record_new)>self.max_requests:
            return False
        self.record.append(timestamp)
        return True


    def get_remaining(self, timestamp: int) -> int:
        """
        Get number of requests remaining in current window.

        :param timestamp: Current timestamp in seconds
        :return: Number of requests still allowed
        """
        record_new=self.record[:]
        record_new.append(timestamp)
        while record_new[0]<timestamp-self.window_seconds:
            record_new.pop(0)
        return self.max_requests-len(record_new)+1


class TodoManager:
    """
    Todo list manager with priorities and filtering.
    """

    def __init__(self):
        """Initialize empty todo list."""
        self.tasks=defaultdict(dict)

    def add_task(self, task_id: str, description: str, priority: int) -> bool:
        """
        Add a new task.

        :param task_id: Unique identifier
        :param description: Task description
        :param priority: Priority level (1=highest, larger=lower priority)
        :return: True if added, False if task_id already exists
        """
        if task_id in self.tasks:
            return False
        self.tasks[task_id]={"description":description, "priority": priority, "completed": False}
        return True

    def complete_task(self, task_id: str) -> bool:
        """
        Mark a task as completed.

        :param task_id: Task to complete
        :return: True if completed, False if not found or already complete
        """
        if task_id in self.tasks:
            if not self.tasks[task_id]["completed"]:
                self.tasks[task_id]["completed"]=True
                return True
        return False
        

    def get_task(self, task_id: str) -> dict:
        """
        Get task details.

        :param task_id: Task to look up
        :return: Dict with "description", "priority", "completed" or None if not found
        """
        if task_id not in self.tasks:
            return None
        return self.tasks[task_id]

    def get_pending(self) -> list:
        """
        Get all pending (not completed) tasks, sorted by priority (ascending),
        then by task_id alphabetically.

        :return: List of task_ids
        """
        res = [tid for tid, des in self.tasks.items() if not des["completed"]]
        sorted_res = sorted(res, key=lambda tid: (self.tasks[tid]["priority"], tid))
        return sorted_res

    def get_by_priority(self, priority: int) -> list:
        """
        Get all tasks with given priority, sorted by task_id.

        :param priority: Priority level to filter
        :return: List of task_ids
        """
        res = [tid for tid, des in self.tasks.items() if des["priority"]==priority]
        return sorted(res)


class EventScheduler:
    """
    Calendar event scheduler with conflict detection.
    Events have start time, end time, and cannot overlap.
    """

    def __init__(self):
        """Initialize empty calendar."""
        self.calendar=defaultdict(dict)

    def add_event(self, event_id: str, start: int, end: int) -> bool:
        """
        Add a new event if it doesn't conflict with existing events.
        An event occupies the interval [start, end) (end is exclusive).

        :param event_id: Unique identifier
        :param start: Start timestamp
        :param end: End timestamp (must be > start)
        :return: True if added, False if conflicts or event_id exists
        """
        if event_id in self.calendar:
            return False
        for event in self.calendar:
            if start>=self.calendar[event]["end"]:
                continue
            elif end<=self.calendar[event]["start"]:
                continue
            return False
        self.calendar[event_id]={"start":start, "end": end}
        return True
        

    def remove_event(self, event_id: str) -> bool:
        """
        Remove an event.

        :param event_id: Event to remove
        :return: True if removed, False if not found
        """
        if event_id in self.calendar:
            self.calendar.pop(event_id)
            return True
        return False

    def get_event(self, event_id: str) -> dict:
        """
        Get event details.

        :param event_id: Event to look up
        :return: Dict with "start", "end" or None if not found
        """
        if event_id not in self.calendar:
            return None
        return self.calendar[event_id]

    def get_events_in_range(self, start: int, end: int) -> list:
        """
        Get all events that overlap with [start, end).
        Sorted by start time, then by event_id.

        :param start: Range start
        :param end: Range end
        :return: List of event_ids
        """
        res=[]
        for event in self.calendar:
            if start>=self.calendar[event]["end"]:
                continue
            elif end<=self.calendar[event]["start"]:
                continue
            res.append(event)
        return sorted(res, key=lambda event:(self.calendar[event]["start"], event))

    def get_conflicts(self, start: int, end: int) -> list:
        """
        Get list of event_ids that would conflict with a new event [start, end).

        :param start: Proposed start
        :param end: Proposed end
        :return: List of conflicting event_ids, sorted by start time
        """
        res=[]
        for event in self.calendar:
            if start>=self.calendar[event]["end"]:
                continue
            elif end<=self.calendar[event]["start"]:
                continue
            res.append(event)
        return res
