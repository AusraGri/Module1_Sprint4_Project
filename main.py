import sys
from plant_data import plant_data


def main():
    ...
    
def program_menu() -> None:
    print("Main Menu")
    menu = [
        "Add Plants",
        "Create Garden",
        "Plants Database",
        "Exit"
    ]

    for index, option in enumerate(menu, start=0):
        print(f"{index}. {option}")
    print(f"{"-"*40}")

    menu_actions = {
        "1": add_plants,
        "2": create_garden,
        "3": plant_database,
        "4": exit_program,
        "exit": exit_program,
    }
    while True:
        user_input = input("Enter menu navigation: ").strip().lower()
        action = menu_actions.get(user_input)
        if action:
            break
        else:
            print("Invalid menu option. Please try again.")
    action()
    
def add_plants():
    ...

def create_garden():
    print("garden")
    
def plant_database():
    print("plant database")
    action = plant_data()
    if action == "done":
        program_menu()
    
    
def exit_program():
    print("goodbye")
    sys.exit()