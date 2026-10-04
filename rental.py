from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .customer import Customer
    from .movie import Movie


class Rental:
    def __init__(self, customer: 'Customer', movie: 'Movie', rental_date: datetime = None):
        self.customer = customer
        self.movie = movie
        self.rental_date = rental_date or datetime.now()
        self.return_due_date = self.rental_date + timedelta(weeks=4)  # 4 weeks maximum
        self.return_date: Optional[datetime] = None
        self.penalty_amount = 0.0
        self.is_returned = False

    def calculate_penalty(self) -> float:
        if self.return_date and self.return_date > self.return_due_date:
            overdue_days = (self.return_date - self.return_due_date).days
            return overdue_days * 1.0  # €1 per day
        elif not self.is_returned and datetime.now() > self.return_due_date:
            overdue_days = (datetime.now() - self.return_due_date).days
            return overdue_days * 1.0
        return 0.0

    def return_movie(self):
        self.return_date = datetime.now()
        self.penalty_amount = self.calculate_penalty()
        self.is_returned = True
        self.movie.is_rented = False
        self.movie.rented_by = None

        # Move from current rentals to history
        if self in self.customer.current_rentals:
            self.customer.current_rentals.remove(self)
        self.customer.rental_history.append(self)

        return self.penalty_amount

    def __str__(self):
        status = "Returned" if self.is_returned else f"Due: {self.return_due_date.strftime('%Y-%m-%d')}"
        return f"{self.movie.title} - Rented: {self.rental_date.strftime('%Y-%m-%d')} - {status}"

    def to_dict(self):
        return {
            'customer_id': self.customer.id_card_number,
            'movie_title': self.movie.title,
            'rental_date': self.rental_date.isoformat(),
            'return_due_date': self.return_due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'penalty_amount': self.penalty_amount,
            'is_returned': self.is_returned
        }
