import sys
from typing import Literal
from class_Garden import Garden
from plant_database import plant_data
from add_plant import add_new_plant
from garden_database import garden_menu

"""Main file of the program where navigation for the program starts>
    """

def main()-> None:
    program_menu()
    
def program_menu() -> None:
    """Main Program menu
    """
    print(">>>>>>> MAIN MENU <<<<<<<<")
    menu: list[str] = [
        "Add Plants",
        "Garden Menu",
        "Plants Database",
        "Exit"
    ]

    for index, option in enumerate(menu, start=1):
        print(f"{index}. {option}")
    print(f"{"-"*40}")

    menu_actions: dict = {
        "1": add_plants,
        "2": garden,
        "3": plant_database,
        "4": exit_program,
        "exit": exit_program,
    }
    while True:
        user_input: str = input("Enter menu navigation: ").strip().lower()
        action = menu_actions.get(user_input)
        if action:
            action()
            break
        else:
            print("Invalid menu option. Please try again.")
    action()
    
def add_plants() -> None:
    """Navigates for adding new plants to the database"""
    action: None | Garden = add_new_plant()
    if action == "done":
        program_menu()

def garden() -> None:
    """Navigates to Garden related menu and actions"""
    action: Literal['out'] = garden_menu()
    if action == "out":
        program_menu()
    
    
def plant_database() -> None:
    """Navigates to plant database actions"""
    action: Garden | Literal['done'] = plant_data()
    if action == "done":
        program_menu()
    
    
def exit_program() -> sys.NoReturn:
    """Exit the program"""
    print("Thank you for using this program")
    sys.exit()
    
    
if __name__ == "__main__":
    main()
    
    
