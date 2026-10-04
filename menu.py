from services.cinema_system import CinemaAtHomeSystem
from .customer_menu import manage_customers_menu
from .actor_menu import manage_actors_menu
from .movie_menu import manage_movies_menu
from .utils import get_user_input


def show_main_menu():
    """Main menu display and navigation"""
    system = CinemaAtHomeSystem()

    # Try to load existing data
    print("Loading system data...")
    system.load_data()

    # Add sample data if system is empty
    if not system.actors:
        print("Initializing system with sample data...")

        # Add sample actors
        actor1_id = system.add_actor("Keanu", "Reeves", "Canadian")
        actor2_id = system.add_actor("Uma", "Thurman", "American")
        actor3_id = system.add_actor("Robert", "De Niro", "American")
        actor4_id = system.add_actor("Leonardo", "DiCaprio", "American")
        actor5_id = system.add_actor("Morgan", "Freeman", "American")

        # Add sample movies
        system.add_dvd_movie("The Matrix", "Sci-Fi", actor1_id, 136, 1999, 2)
        system.add_vhs_movie("Pulp Fiction", "Crime", actor2_id, 154, 1994, "Super-VHS")
        system.add_compact_memory_movie("Taxi Driver", "Drama", actor3_id, 114, 1976, "MP4")
        system.add_dvd_movie("Inception", "Sci-Fi", actor4_id, 148, 2010, 2)
        system.add_vhs_movie("The Shawshank Redemption", "Drama", actor5_id, 142, 1994, "VHS")

        # Add sample customers
        system.add_customer("John", "Smith", "12345678", "555-1234", "john@email.com")
        system.add_customer("Maria", "Garcia", "87654321", "555-5678", "maria@email.com")
        system.add_customer("David", "Johnson", "11223344", "555-9999", "david@email.com")

    # Main menu loop
    while True:
        print("\n" + "=" * 60)
        print(" CINEMA AT HOME - MOVIE RENTAL SYSTEM ")
        print("=" * 60)
        print("1. Manage Customers")
        print("2. Manage Movie directors & Actors")
        print("3. Manage Movies")
        print("4. Rent")
        print("5. Return")
        print("6. Transaction History")
        print("7. Exit")

        choice = get_user_input("\nEnter your choice (1-7): ")

        if choice == "1":
            manage_customers_menu(system)

        elif choice == "2":
            manage_actors_menu(system)

        elif choice == "3":
            manage_movies_menu(system)

        elif choice == "4":
            print("\n" + "=" * 50)
            print("RENT MOVIE")
            print("=" * 50)
            if not system.customers:
                print("You need to register as a customer first!")
                print("Redirecting to customer registration...\n")
                manage_customers_menu(system)
                if not system.customers:
                    print("Registration required before renting.")
                elif not system.movies:
                    print("No movies in the system. Please add movies first.")
                else:
                    system.rent_movie_interactive()
            elif not system.movies:
                print("No movies in the system. Please add movies first.")
            else:
                system.rent_movie_interactive()
        elif choice == "5":
            print("\n" + "=" * 50)
            print("RETURN MOVIE")
            print("=" * 50)
            system.return_movie_interactive()

        elif choice == "6":
            system.show_transaction_history()

        elif choice == "7":
            print("\nSaving data...")
            system.save_data()
            print("\n🎬 Thank you for using Cinema at Home! 🎬")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please enter 1-7.")

        # Pause before showing menu again
        if choice != "7":
            input("\nPress Enter to continue...")


