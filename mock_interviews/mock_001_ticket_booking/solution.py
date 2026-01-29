# Mock Assessment 001: Ticket Booking System
# Time Limit: 90 minutes
#
# Instructions: Implement the TicketSystem class below.
# Run tests with: python -m pytest test_solution.py -v
#
# Start your timer now!

from collections import defaultdict, deque


class TicketSystem:
    def __init__(self, venue_capacity: int):
        """Initialize the system with the venue's total seat capacity."""
        # TODO: Implement
        pass

    # ==================== LEVEL 1 ====================

    def book(self, event_date: str, customer_id: str, num_tickets: int, waitlist: bool = False) -> bool:
        """
        Attempt to book num_tickets for customer_id on event_date.

        Level 1: Basic booking (ignore waitlist parameter)
        Level 3: If waitlist=True and booking fails, add to waitlist

        Returns True if booking succeeds, False otherwise.
        """
        # TODO: Implement
        pass

    def cancel(self, event_date: str, customer_id: str) -> int:
        """
        Cancel ALL bookings for customer_id on event_date.

        Level 1: Return total tickets cancelled
        Level 3: After cancellation, process waitlist automatically

        Returns number of tickets cancelled (0 if no bookings found).
        """
        # TODO: Implement
        pass

    # ==================== LEVEL 2 ====================

    def get_available_seats(self, event_date: str) -> int:
        """Return the number of available seats for event_date."""
        # TODO: Implement
        pass

    def get_customer_bookings(self, customer_id: str) -> dict[str, int]:
        """
        Return dict mapping event_date to total tickets booked by customer.
        Only include dates with active bookings.
        """
        # TODO: Implement
        pass

    def get_top_customers(self, event_date: str, n: int) -> list[tuple[str, int]]:
        """
        Return top n customers by tickets booked for event_date.
        Sort by ticket count desc, then customer_id asc for ties.
        """
        # TODO: Implement
        pass

    # ==================== LEVEL 3 ====================

    def get_waitlist(self, event_date: str) -> list[tuple[str, int]]:
        """Return waitlist entries for event_date in FIFO order."""
        # TODO: Implement
        pass

    def remove_from_waitlist(self, event_date: str, customer_id: str) -> bool:
        """Remove customer from waitlist. Return True if removed."""
        # TODO: Implement
        pass

    # ==================== LEVEL 4 ====================

    def optimize_waitlist(self, event_date: str, ticket_price: int) -> list[str]:
        """
        Find optimal subset of waitlisted customers to maximize revenue.
        Does NOT modify system state.
        Return list of customer_ids to accept.
        """
        # TODO: Implement
        pass
