"""Movie theater ticket booking and seating management module."""

import hashlib
import os
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve a seat for a customer.

    Returns True on success, False if the seat does not exist or is sold.
    If order_history (a list) is supplied, a log entry is appended to it.
    """
    seat = theater_seats.get(seat_id)
    if seat is None or seat["is_sold"]:
        return False
    seat["is_sold"] = True
    if order_history is None:
        order_history = []
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Release a sold seat. Returns True if a sale was cancelled."""
    seat = theater_seats.get(seat_id)
    if seat is None or not seat["is_sold"]:
        return False
    seat["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True if the seat exists and is still available."""
    seat = theater_seats.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Return the seat price after applying a discount rate (0.0 to 1.0).

    For example, discount_rate=0.20 gives 20% off.
    """
    if seat_id not in theater_seats:
        raise KeyError(f"Unknown seat: {seat_id}")
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("discount_rate must be between 0.0 and 1.0")
    return theater_seats[seat_id]["price"] * (1 - discount_rate)


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 hex digest for a ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a cryptographically secure 4-digit booking PIN."""
    return 1000 + secrets.randbelow(9000)


def export_seating_chart(filename="seating_chart.txt"):
    """Write one line per seat to a text file."""
    with open(filename, "w", encoding="utf-8") as chart_file:
        for seat_id, details in theater_seats.items():
            status = "SOLD" if details["is_sold"] else "FREE"
            chart_file.write(
                f"{seat_id}: {details['tier']} "
                f"${details['price']:.2f} {status}\n"
            )
    print("Seating chart exported to:", filename)


def get_theater_summary(seats):
    """Return the number of sold seats in the given seat mapping."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a short demonstration of the booking system."""
    box_office_key = os.environ.get("BOX_OFFICE_KEY")
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))
    print("Box office key configured:", box_office_key is not None)


if __name__ == "__main__":
    main()
