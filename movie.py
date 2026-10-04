from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .actor import Actor
    from .customer import Customer


class Movie(ABC):
    def __init__(self, title: str, genre: str, main_actor: 'Actor', duration: int, production_year: int):
        self.title = title
        self.genre = genre
        self.main_actor = main_actor
        self.duration = duration  # in minutes
        self.production_year = production_year
        self.is_rented = False
        self.rented_by: Optional['Customer'] = None

    @abstractmethod
    def get_format_info(self) -> str:
        pass

    def __str__(self):
        status = "RENTED" if self.is_rented else "AVAILABLE"
        return f"{self.title} ({self.production_year}) - {self.genre} - {self.duration}min - Starring: {self.main_actor} - [{status}]"

    def to_dict(self):
        base_dict = {
            'title': self.title,
            'genre': self.genre,
            'main_actor_id': self.main_actor.actor_id,
            'duration': self.duration,
            'production_year': self.production_year,
            'is_rented': self.is_rented,
            'movie_type': self.__class__.__name__
        }
        return base_dict


class VHSMovie(Movie):
    def __init__(self, title: str, genre: str, main_actor: 'Actor', duration: int, production_year: int, vhs_type: str):
        super().__init__(title, genre, main_actor, duration, production_year)
        self.vhs_type = vhs_type  # e.g., "Super-VHS", "VHS-C"

    def get_format_info(self) -> str:
        return f"VHS ({self.vhs_type})"

    def to_dict(self):
        data = super().to_dict()
        data['vhs_type'] = self.vhs_type
        return data


class DVDMovie(Movie):
    def __init__(self, title: str, genre: str, main_actor: 'Actor', duration: int, production_year: int,
                 number_of_layers: int):
        super().__init__(title, genre, main_actor, duration, production_year)
        self.number_of_layers = number_of_layers

    def get_format_info(self) -> str:
        return f"DVD ({self.number_of_layers} layers)"

    def to_dict(self):
        data = super().to_dict()
        data['number_of_layers'] = self.number_of_layers
        return data


class CompactMemoryMovie(Movie):
    def __init__(self, title: str, genre: str, main_actor: 'Actor', duration: int, production_year: int,
                 encoding_type: str):
        super().__init__(title, genre, main_actor, duration, production_year)
        self.encoding_type = encoding_type  # e.g., "MP4", "MPEG-1"

    def get_format_info(self) -> str:
        return f"Compact Memory ({self.encoding_type})"

    def to_dict(self):
        data = super().to_dict()
        data['encoding_type'] = self.encoding_type
        return data