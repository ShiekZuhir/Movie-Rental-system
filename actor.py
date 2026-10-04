class Actor:
    def __init__(self, actor_id: str, name: str, surname: str, nationality: str):
        self.actor_id = actor_id
        self.name = name
        self.surname = surname
        self.nationality = nationality

    def __str__(self):
        return f"{self.name} {self.surname} ({self.nationality})"

    def to_dict(self):
        return {
            'actor_id': self.actor_id,
            'name': self.name,
            'surname': self.surname,
            'nationality': self.nationality
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['actor_id'], data['name'], data['surname'], data['nationality'])
