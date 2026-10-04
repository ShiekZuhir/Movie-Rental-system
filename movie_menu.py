from services.cinema_system import CinemaAtHomeSystem
from .utils import get_user_input


def manage_movies_menu(system: CinemaAtHomeSystem):
    """Movie management submenu"""
    while True:
        print("\n" + "=" * 50)
        print("MOVIE MANAGEMENT")
        print("=" * 50)
        print("1. Add VHS Movie")
        print("2. Add DVD Movie")
        print("3. Add Compact Memory Movie")
        print("4. View All Movies")
        print("5. Delete Movie")
        print("6. Back to Main Menu")

        choice = get_user_input("\nEnter your choice (1-6): ")

        if choice == "1":
            add_vhs_movie(system)
        elif choice == "2":
            add_dvd_movie(system)
        elif choice == "3":
            add_compact_memory_movie(system)
        elif choice == "4":
            system.view_movies()
        elif choice == "5":
            system.view_movies()
            if system.movies:
                try:
                    movie_index = int(get_user_input("\nEnter movie number to delete: ")) - 1
                    system.delete_movie(movie_index)
                except ValueError:
                    print("Please enter a valid number!")
        elif choice == "6":
            break
        else:
            print("Invalid choice! Please enter 1-6.")


def add_vhs_movie(system: CinemaAtHomeSystem):
    """Add VHS movie with user input"""
    if not system.actors:
        print("No actors in the system. Please add actors first.")
        return

    print("\n--- ADD NEW VHS MOVIE ---")
    system.view_actors()

    title = get_user_input("\nEnter movie title: ")
    genre = get_user_input("Enter genre: ")
    actor_id = get_user_input("Enter main actor ID: ")

    try:
        duration = int(get_user_input("Enter duration (minutes): "))
        production_year = int(get_user_input("Enter production year: "))
    except ValueError:
        print("Duration and production year must be numbers!")
        return

    vhs_type = get_user_input("Enter VHS type (e.g., Super-VHS, VHS-C): ")

    if all([title, genre, actor_id, vhs_type]) and duration > 0 and production_year > 0:
        system.add_vhs_movie(title, genre, actor_id, duration, production_year, vhs_type)
    else:
        print("All fields are required and must be valid!")


def add_dvd_movie(system: CinemaAtHomeSystem):
    """Add DVD movie with user input"""
    if not system.actors:
        print("No actors in the system. Please add actors first.")
        return

    print("\n--- ADD NEW DVD MOVIE ---")
    system.view_actors()

    title = get_user_input("\nEnter movie title: ")
    genre = get_user_input("Enter genre: ")
    actor_id = get_user_input("Enter main actor ID: ")

    try:
        duration = int(get_user_input("Enter duration (minutes): "))
        production_year = int(get_user_input("Enter production year: "))
        layers = int(get_user_input("Enter number of layers: "))
    except ValueError:
        print("Duration, production year, and layers must be numbers!")
        return

    if all([title, genre, actor_id]) and duration > 0 and production_year > 0 and layers > 0:
        system.add_dvd_movie(title, genre, actor_id, duration, production_year, layers)
    else:
        print("All fields are required and must be valid!")


def add_compact_memory_movie(system: CinemaAtHomeSystem):
    """Add Compact Memory movie with user input"""
    if not system.actors:
        print("No actors in the system. Please add actors first.")
        return

    print("\n--- ADD NEW COMPACT MEMORY MOVIE ---")
    system.view_actors()

    title = get_user_input("\nEnter movie title: ")
    genre = get_user_input("Enter genre: ")
    actor_id = get_user_input("Enter main actor ID: ")

    try:
        duration = int(get_user_input("Enter duration (minutes): "))
        production_year = int(get_user_input("Enter production year: "))
    except ValueError:
        print("Duration and production year must be numbers!")
        return

    encoding_type = get_user_input("Enter encoding type (e.g., MP4, MPEG-1): ")

    if all([title, genre, actor_id, encoding_type]) and duration > 0 and production_year > 0:
        system.add_compact_memory_movie(title, genre, actor_id, duration, production_year, encoding_type)
    else:
        print("All fields are required and must be valid!")