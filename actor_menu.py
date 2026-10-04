from services.cinema_system import CinemaAtHomeSystem
from .utils import get_user_input


def manage_actors_menu(system: CinemaAtHomeSystem):
    """Actor management submenu"""
    while True:
        print("\n" + "=" * 50)
        print("MOVIE DIRECTORS & ACTORS MANAGEMENT")
        print("=" * 50)
        print("1. Add Actor/Director")
        print("2. View All Actors/Directors")
        print("3. Delete Actor/Director")
        print("4. Back to Main Menu")

        choice = get_user_input("\nEnter your choice (1-4): ")

        if choice == "1":
            print("\n--- ADD NEW ACTOR/DIRECTOR ---")
            name = get_user_input("Enter first name: ")
            surname = get_user_input("Enter surname: ")
            nationality = get_user_input("Enter nationality: ")

            if all([name, surname, nationality]):
                system.add_actor(name, surname, nationality)
            else:
                print("All fields are required!")

        elif choice == "2":
            system.view_actors()

        elif choice == "3":
            system.view_actors()
            if system.actors:
                actor_id = get_user_input("\nEnter Actor ID to delete: ")
                system.delete_actor(actor_id)

        elif choice == "4":
            break

        else:
            print("Invalid choice! Please enter 1-4.")
