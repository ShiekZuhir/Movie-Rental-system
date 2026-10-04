from services.cinema_system import CinemaAtHomeSystem
from .utils import get_user_input


def validate_number(number_str, field_name):
    """Validate that a number string has at least 8 digits"""
    # Remove any non-digit characters for validation
    digits_only = ''.join(char for char in number_str if char.isdigit())

    if len(digits_only) < 8:
        print(f"Invalid {field_name}! Must contain at least 8 digits.")
        return False
    return True


def validate_name(name_str, field_name):
    """Validate that a name has at least 4 letters"""
    # Remove any non-letter characters for validation
    letters_only = ''.join(filter(str.isalpha, name_str))

    if len(letters_only) < 4:
        print(f"Invalid {field_name}! Must contain at least 4 letters.")
        return False
    return True


def manage_customers_menu(system: CinemaAtHomeSystem):
    """Customer management submenu"""
    while True:
        print("\n" + "=" * 50)
        print("CUSTOMER MANAGEMENT")
        print("=" * 50)
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Delete Customer")
        print("4. Back to Main Menu")

        choice = get_user_input("\nEnter your choice (1-4): ")

        if choice == "1":
            print("\n--- ADD NEW CUSTOMER ---")

            # Validate first name
            while True:
                name = get_user_input("Enter first name: ")
                if validate_name(name, "first name"):
                    break

            # Validate surname
            while True:
                surname = get_user_input("Enter surname: ")
                if validate_name(surname, "surname"):
                    break

            # Validate ID card number
            while True:
                id_card = get_user_input("Enter ID card number: ")
                if validate_number(id_card, "ID card number"):
                    break

            # Validate phone number
            while True:
                phone = get_user_input("Enter phone number: ")
                if validate_number(phone, "phone number"):
                    break

            email = get_user_input("Enter email address: ")

            if all([name, surname, id_card, phone, email]):
                system.add_customer(name, surname, id_card, phone, email)
            else:
                print("All fields are required!")

        elif choice == "2":
            system.view_customers()

        elif choice == "3":
            system.view_customers()
            if system.customers:
                # Validate ID card number for deletion
                while True:
                    id_card = get_user_input("\nEnter ID card number to delete: ")
                    if validate_number(id_card, "ID card number"):
                        break
                system.delete_customer(id_card)

        elif choice == "4":
            break

        else:
            print("Invalid choice! Please enter 1-4.")