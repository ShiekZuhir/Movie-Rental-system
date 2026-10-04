from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .rental import Rental


class Customer:
    def __init__(self, name: str, surname: str, id_card_number: str, phone_number: str, email_address: str):
        self.name = name
        self.surname = surname
        self.id_card_number = id_card_number
        self.phone_number = phone_number
        self.email_address = email_address
        self.current_rentals: List['Rental'] = []
        self.rental_history: List['Rental'] = []

    def can_rent_more(self) -> bool:
        return len(self.current_rentals) < 3

    def __str__(self):
        return f"{self.name} {self.surname} (ID: {self.id_card_number})"

    def to_dict(self):
        return {
            'name': self.name,
            'surname': self.surname,
            'id_card_number': self.id_card_number,
            'phone_number': self.phone_number,
            'email_address': self.email_address,
            'current_rentals': [rental.to_dict() for rental in self.current_rentals],
            'rental_history': [rental.to_dict() for rental in self.rental_history]
        }

    @classmethod
    def from_dict(cls, data):
        customer = cls(
            data['name'], data['surname'], data['id_card_number'],
            data['phone_number'], data['email_address']
        )
        return customer