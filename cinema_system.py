from typing import Dict, List, Optional
from datetime import datetime
from models.actor import Actor
from models.customer import Customer
from models.movie import Movie, VHSMovie, DVDMovie, CompactMemoryMovie
from models.rental import Rental
from utils.data_manager import DataManager


class CinemaAtHomeSystem:
    def __init__(self):
        self.actors: Dict[str, Actor] = {}
        self.customers: Dict[str, Customer] = {}
        self.movies: List[Movie] = []
        self.rentals: List[Rental] = []
        self.next_actor_id = 1
        self.data_manager = DataManager()

    # Actor Management
    def add_actor(self, name: str, surname: str, nationality: str) -> str:
        actor_id = f"A{self.next_actor_id:04d}"
        self.next_actor_id += 1
        actor = Actor(actor_id, name, surname, nationality)
        self.actors[actor_id] = actor
        print(f"Actor added: {actor}")
        return actor_id

    def view_actors(self):
        print("\n=== ACTORS CATALOGUE ===")
        if not self.actors:
            print("No actors in the system.")
            return
        for actor in self.actors.values():
            print(f"ID: {actor.actor_id} | {actor}")

    def delete_actor(self, actor_id: str) -> bool:
        if actor_id not in self.actors:
            print("Actor not found!")
            return False

        # Check if actor is referenced by any movie
        for movie in self.movies:
            if movie.main_actor.actor_id == actor_id:
                print(f"Cannot delete actor. Referenced by movie: {movie.title}")
                return False

        actor = self.actors.pop(actor_id)
        print(f"Actor deleted: {actor}")
        return True

    # Customer Management
    def add_customer(self, name: str, surname: str, id_card_number: str, phone_number: str, email_address: str) -> bool:
        if id_card_number in self.customers:
            print("Customer with this ID already exists!")
            return False

        customer = Customer(name, surname, id_card_number, phone_number, email_address)
        self.customers[id_card_number] = customer
        print(f"Customer added: {customer}")
        return True

    def view_customers(self):
        print("\n=== CUSTOMER BASE ===")
        if not self.customers:
            print("No customers in the system.")
            return
        for customer in self.customers.values():
            rentals_count = len(customer.current_rentals)
            print(
                f"{customer} | Phone: {customer.phone_number} | Email: {customer.email_address} | Current Rentals: {rentals_count}/3")

    def delete_customer(self, id_card_number: str) -> bool:
        if id_card_number not in self.customers:
            print("Customer not found!")
            return False

        customer = self.customers[id_card_number]
        if customer.current_rentals:
            print("Cannot delete customer with active rentals!")
            return False

        del self.customers[id_card_number]
        print(f"Customer deleted: {customer}")
        return True

    # Movie Management
    def add_vhs_movie(self, title: str, genre: str, main_actor_id: str, duration: int, production_year: int,
                      vhs_type: str) -> bool:
        if main_actor_id not in self.actors:
            print("Main actor not found!")
            return False

        actor = self.actors[main_actor_id]
        movie = VHSMovie(title, genre, actor, duration, production_year, vhs_type)
        self.movies.append(movie)
        print(f"VHS Movie added: {movie} | Format: {movie.get_format_info()}")
        return True

    def add_dvd_movie(self, title: str, genre: str, main_actor_id: str, duration: int, production_year: int,
                      number_of_layers: int) -> bool:
        if main_actor_id not in self.actors:
            print("Main actor not found!")
            return False

        actor = self.actors[main_actor_id]
        movie = DVDMovie(title, genre, actor, duration, production_year, number_of_layers)
        self.movies.append(movie)
        print(f"DVD Movie added: {movie} | Format: {movie.get_format_info()}")
        return True

    def add_compact_memory_movie(self, title: str, genre: str, main_actor_id: str, duration: int, production_year: int,
                                 encoding_type: str) -> bool:
        if main_actor_id not in self.actors:
            print("Main actor not found!")
            return False

        actor = self.actors[main_actor_id]
        movie = CompactMemoryMovie(title, genre, actor, duration, production_year, encoding_type)
        self.movies.append(movie)
        print(f"Compact Memory Movie added: {movie} | Format: {movie.get_format_info()}")
        return True

    def view_movies(self):
        print("\n=== MOVIE CATALOGUE ===")
        if not self.movies:
            print("No movies in the system.")
            return
        for i, movie in enumerate(self.movies):
            print(f"{i + 1}. {movie} | Format: {movie.get_format_info()}")

    def view_available_movies(self):
        print("\n=== AVAILABLE MOVIES FOR RENT ===")
        available_movies = [movie for movie in self.movies if not movie.is_rented]
        if not available_movies:
            print("No movies available for rent.")
            return []

        for i, movie in enumerate(available_movies):
            print(f"{i + 1}. {movie} | Format: {movie.get_format_info()}")
        return available_movies

    def delete_movie(self, movie_index: int) -> bool:
        if movie_index < 0 or movie_index >= len(self.movies):
            print("Invalid movie index!")
            return False

        movie = self.movies[movie_index]
        if movie.is_rented:
            print("Cannot delete movie that is currently rented!")
            return False

        removed_movie = self.movies.pop(movie_index)
        print(f"Movie deleted: {removed_movie.title}")
        return True

    # Rental Management
    def rent_movie_interactive(self) -> bool:
        """Interactive movie rental process"""
        if not self.customers:
            print("No customers in the system. Please add customers first.")
            return False

        if not self.movies:
            print("No movies in the system. Please add movies first.")
            return False

        # Show available customers
        print("\n=== SELECT CUSTOMER ===")
        customer_list = list(self.customers.values())
        for i, customer in enumerate(customer_list):
            rentals_count = len(customer.current_rentals)
            can_rent = "✓" if customer.can_rent_more() else "✗ (Limit reached)"
            print(f"{i + 1}. {customer} | Current Rentals: {rentals_count}/3 | {can_rent}")

        try:
            customer_choice = int(input("\nEnter customer number: ")) - 1
            if customer_choice < 0 or customer_choice >= len(customer_list):
                print("Invalid customer selection!")
                return False

            selected_customer = customer_list[customer_choice]

            if not selected_customer.can_rent_more():
                print(
                    f"Customer {selected_customer.name} {selected_customer.surname} has reached the rental limit (3 movies)!")
                return False

            # Show available movies
            available_movies = self.view_available_movies()
            if not available_movies:
                return False

            movie_choice = int(input("\nEnter movie number to rent: ")) - 1
            if movie_choice < 0 or movie_choice >= len(available_movies):
                print("Invalid movie selection!")
                return False

            selected_movie = available_movies[movie_choice]

            # Create rental
            rental = Rental(selected_customer, selected_movie)
            selected_movie.is_rented = True
            selected_movie.rented_by = selected_customer
            selected_customer.current_rentals.append(rental)
            self.rentals.append(rental)

            print(f"\n✓ Movie rented successfully!")
            print(f"Customer: {selected_customer}")
            print(f"Movie: {selected_movie.title}")
            print(f"Rental Date: {rental.rental_date.strftime('%Y-%m-%d')}")
            print(f"Due Date: {rental.return_due_date.strftime('%Y-%m-%d')}")

            return True

        except ValueError:
            print("Please enter a valid number!")
            return False
        except Exception as e:
            print(f"Error during rental process: {e}")
            return False

    def rent_movie(self, customer_id: str, movie_index: int) -> bool:
        """Direct rental method (for API use)"""
        if customer_id not in self.customers:
            print("Customer not found!")
            return False

        customer = self.customers[customer_id]

        if not customer.can_rent_more():
            print(f"Customer {customer.name} {customer.surname} has reached the rental limit (3 movies)!")
            return False

        if movie_index < 0 or movie_index >= len(self.movies):
            print("Invalid movie index!")
            return False

        movie = self.movies[movie_index]
        if movie.is_rented:
            print(f"Movie '{movie.title}' is already rented out!")
            return False

        rental = Rental(customer, movie)
        movie.is_rented = True
        movie.rented_by = customer
        customer.current_rentals.append(rental)
        self.rentals.append(rental)

        print(f"Movie rented successfully!")
        print(f"Customer: {customer}")
        print(f"Movie: {movie.title}")
        print(f"Rental Date: {rental.rental_date.strftime('%Y-%m-%d')}")
        print(f"Due Date: {rental.return_due_date.strftime('%Y-%m-%d')}")

        return True

    # Returns Management
    def get_customer_rentals(self, customer_id: str) -> List[Rental]:
        if customer_id not in self.customers:
            print("Customer not found!")
            return []

        customer = self.customers[customer_id]
        return customer.current_rentals

    def return_movie_interactive(self) -> bool:
        """Interactive movie return process"""
        # Find customers with active rentals
        customers_with_rentals = [(customer, customer.current_rentals)
                                  for customer in self.customers.values()
                                  if customer.current_rentals]

        if not customers_with_rentals:
            print("No active rentals found.")
            return False

        print("\n=== SELECT CUSTOMER TO RETURN MOVIE ===")
        for i, (customer, rentals) in enumerate(customers_with_rentals):
            print(f"{i + 1}. {customer} | Active Rentals: {len(rentals)}")

        try:
            customer_choice = int(input("\nEnter customer number: ")) - 1
            if customer_choice < 0 or customer_choice >= len(customers_with_rentals):
                print("Invalid customer selection!")
                return False

            selected_customer, rentals = customers_with_rentals[customer_choice]

            print(f"\n=== ACTIVE RENTALS FOR {selected_customer.name} {selected_customer.surname} ===")
            for i, rental in enumerate(rentals):
                penalty = rental.calculate_penalty()
                penalty_info = f" | Penalty: €{penalty:.2f}" if penalty > 0 else ""
                print(f"{i + 1}. {rental}{penalty_info}")

            rental_choice = int(input("\nEnter rental number to return: ")) - 1
            if rental_choice < 0 or rental_choice >= len(rentals):
                print("Invalid rental selection!")
                return False

            rental = rentals[rental_choice]
            penalty = rental.return_movie()

            print(f"\n✓ Movie returned successfully!")
            print(f"Movie: {rental.movie.title}")
            print(f"Return Date: {rental.return_date.strftime('%Y-%m-%d')}")
            if penalty > 0:
                print(f"Penalty Amount: €{penalty:.2f}")
            else:
                print("No penalty charges.")

            return True

        except ValueError:
            print("Please enter a valid number!")
            return False
        except Exception as e:
            print(f"Error during return process: {e}")
            return False

    def return_movie(self, customer_id: str, rental_index: int) -> Optional[float]:
        """Direct return method (for API use)"""
        customer_rentals = self.get_customer_rentals(customer_id)
        if not customer_rentals:
            print("No active rentals for this customer.")
            return None

        if rental_index < 0 or rental_index >= len(customer_rentals):
            print("Invalid rental selection!")
            return None

        rental = customer_rentals[rental_index]
        penalty = rental.return_movie()

        print(f"Movie returned successfully!")
        print(f"Movie: {rental.movie.title}")
        print(f"Return Date: {rental.return_date.strftime('%Y-%m-%d')}")
        if penalty > 0:
            print(f"Penalty Amount: €{penalty:.2f}")
        else:
            print("No penalty charges.")

        return penalty

    def show_customer_rentals(self, customer_id: str):
        customer_rentals = self.get_customer_rentals(customer_id)
        if not customer_rentals:
            print("No active rentals for this customer.")
            return

        print(f"\n=== ACTIVE RENTALS FOR CUSTOMER {customer_id} ===")
        for i, rental in enumerate(customer_rentals):
            penalty = rental.calculate_penalty()
            penalty_info = f" | Penalty: €{penalty:.2f}" if penalty > 0 else ""
            print(f"{i + 1}. {rental}{penalty_info}")

    def show_transaction_history(self):
        """Show all rental transactions (both active and returned)"""
        print("\n=== TRANSACTION HISTORY ===")
        if not self.rentals:
            print("No transactions found.")
            return

        all_rentals = []
        # Include active rentals and rental history from all customers
        for customer in self.customers.values():
            all_rentals.extend(customer.current_rentals)
            all_rentals.extend(customer.rental_history)

        if not all_rentals:
            print("No transactions found.")
            return

        # Sort by rental date (newest first)
        all_rentals.sort(key=lambda x: x.rental_date, reverse=True)

        for rental in all_rentals:
            status = "RETURNED" if rental.is_returned else "ACTIVE"
            penalty_info = f" | Penalty: €{rental.penalty_amount:.2f}" if rental.penalty_amount > 0 else ""
            print(f"{rental.customer.name} {rental.customer.surname} | {rental.movie.title} | "
                  f"Rented: {rental.rental_date.strftime('%Y-%m-%d')} | "
                  f"Due: {rental.return_due_date.strftime('%Y-%m-%d')} | "
                  f"Status: {status}{penalty_info}")

    # Data Persistence
    def save_data(self):
        data = {
            'actors': {k: v.to_dict() for k, v in self.actors.items()},
            'customers': {k: v.to_dict() for k, v in self.customers.items()},
            'movies': [self._movie_to_dict(movie) for movie in self.movies],
            'rentals': [rental.to_dict() for rental in self.rentals],
            'next_actor_id': self.next_actor_id
        }
        return self.data_manager.save_data(data)

    def load_data(self):
        data = self.data_manager.load_data()
        if not data:
            return False

        # Load actors first
        self.actors = {}
        for actor_data in data.get('actors', {}).values():
            actor = Actor.from_dict(actor_data)
            self.actors[actor.actor_id] = actor

        # Load customers
        self.customers = {}
        for customer_data in data.get('customers', {}).values():
            customer = Customer.from_dict(customer_data)
            self.customers[customer.id_card_number] = customer

        # Load movies
        self.movies = []
        for movie_data in data.get('movies', []):
            movie = self._dict_to_movie(movie_data)
            if movie:
                self.movies.append(movie)

        # Load other data
        self.next_actor_id = data.get('next_actor_id', 1)
        return True

    def _movie_to_dict(self, movie: Movie) -> dict:
        data = movie.to_dict()
        if isinstance(movie, VHSMovie):
            data['vhs_type'] = movie.vhs_type
        elif isinstance(movie, DVDMovie):
            data['number_of_layers'] = movie.number_of_layers
        elif isinstance(movie, CompactMemoryMovie):
            data['encoding_type'] = movie.encoding_type
        return data

    def _dict_to_movie(self, movie_data: dict) -> Optional[Movie]:
        try:
            actor = self.actors.get(movie_data['main_actor_id'])
            if not actor:
                print(f"Warning: Actor {movie_data['main_actor_id']} not found for movie {movie_data['title']}")
                return None

            movie_type = movie_data['movie_type']
            if movie_type == 'VHSMovie':
                movie = VHSMovie(
                    movie_data['title'], movie_data['genre'], actor,
                    movie_data['duration'], movie_data['production_year'],
                    movie_data['vhs_type']
                )
            elif movie_type == 'DVDMovie':
                movie = DVDMovie(
                    movie_data['title'], movie_data['genre'], actor,
                    movie_data['duration'], movie_data['production_year'],
                    movie_data['number_of_layers']
                )
            elif movie_type == 'CompactMemoryMovie':
                movie = CompactMemoryMovie(
                    movie_data['title'], movie_data['genre'], actor,
                    movie_data['duration'], movie_data['production_year'],
                    movie_data['encoding_type']
                )
            else:
                print(f"Unknown movie type: {movie_type}")
                return None

            movie.is_rented = movie_data.get('is_rented', False)
            return movie
        except Exception as e:
            print(f"Error loading movie {movie_data.get('title', 'Unknown')}: {e}")
            return None