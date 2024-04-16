from tabulate import tabulate
from typing import Literal
from datetime import datetime
from class_DataToPDF import DataToPDF
from class_garden import Garden
from class_DataHandler import DataHandler
from class_PlantDataManager import PlantDataManager
from add_plant import add_new_plant, ask_for_next
from plant_database import plant_data
from garden_visual_table import garden_visual
from all_commands import all_garden_commands

"""Garden data managing. Creating /showing / editing / deleting gardens.
    """

def garden_menu() -> Literal["out"]:
    """ Main Garden menu"""
    print(">>>>>>> GARDEN MENU <<<<<<<<")
    menu: dict[str,list] = {
        "Create new Garden": [1, "create"],
        "All Gardens": [2, "all"],
        "Exit Gardens": [3, "out"],
    }
    while True:
        action: str = get_menu_answer(menu)
        if action == "create":
            create_garden()
            break
        elif action == "all":
            all_gardens_menu()
            break
        elif action == "out":
            return "out"


def create_garden() -> None:
    """Creates new garden object"""
    print(">>>>> NEW GARDEN <<<<<")
    name: str = get_name("Garden name:")
    create_garden = Garden(name)
    new_garden: Garden = add_plant_to_garden(create_garden)
    if new_garden:
        add_notes: Garden = add_garden_notes(new_garden)
        if add_notes:
            confirmed_garden: Garden | False = confirm_garden(create_garden)
            if confirmed_garden:
                save_garden(confirmed_garden)
            elif not confirmed_garden:
                print("Garden discarded")
                


def check_if_data_exists(filename: str) -> list[dict] | Literal[False]:
    """Checks if data file exists
    Args:
        filename (str): filename of the data file
    Returns:
        list[dict] | False: returns data in the file
        or False if file is not found
    """
    try:
        file = DataHandler(filename)
        data: list[dict] = file.load_data()
        if data:
            return data
    except FileNotFoundError:
        print("No gardens. Please create at least one.")
        return False


def all_gardens_menu() -> None:
    """Shows all existing gardens and accepts commands for interaction with gardens"""
    data: list[dict] | False = check_if_data_exists("gardens.json")
    if not data:
        print("No data in gardens. Please create garden first")
    while data and True:
        print(">>>>>>ALL GARDENS<<<<<<<")
        data = show_all_gardens(data)
        command: str | list[str] = get_garden_command()
        if command == 1:
            pass
        elif command[0] == "exit":
            break
        elif command[0] == "open":
            if garden := find_garden(data, command[1].strip()):
                garden_data_manipulation(garden)
                data = check_if_data_exists("gardens.json")
            else:
                print(f"No garden with ID: {command[1]} was found")
        elif command[0] == "sort":
            data = sort_garden(data, command[1])
        elif command[0] == "search":
            if found := search_for_garden_name(data, command[1]):
                print(">>>>>>>>> FOUND <<<<<<<<")
                show_all_gardens(found)
                print(">>>>>>>>> FOUND <<<<<<<<")
            else:
                print(f"No garden with the name {command[1]} was found")


def find_garden(gardens: list[dict], garden_id: str) -> Garden | None:
    """Searched for garden by id in garden data
    Args:
        gardens (list[dict]): data to search in
        garden_id (str): garden id to search for

    Returns:
        Garden | None: returns Garden object if found
        if not found returns None
    """
    for garden in gardens:
        if garden_id == garden["garden_id"]:
            return Garden(garden)


def search_for_garden_name(gardens: list[dict], name: str) -> list | Literal[False]:
    """Seach for garden by garden name
    Args:
        gardens (list[dict]): garden data to search in
        name (str): garden name to search for
    Returns:
        list[dict] | False: returns list of gardens or False if no match found
    """
    garden_found: list = []
    for garden in gardens:
        if name.lower() in garden["name"].lower():
            garden_found.append(garden)
    if garden_found:
        return garden_found
    elif not garden_found:
        return False


def print_gardens(gardens: list[dict]) -> None:
    """Prints given gardens as table"""
    enumerated_gardens: list[list[int]] = [
        [i + 1] + list(row.values()) for i, row in enumerate(gardens)
    ]
    headers: list[str] = ["No."] + list(gardens[0].keys())
    print(
        tabulate(enumerated_gardens, headers=headers, tablefmt="grid", maxcolwidths=130)
    )


def sort_garden(gardens: list[dict], attribute: str) -> list[dict]:
    """Sorts gardens by given attribute
    Args:
        gardens (list[dict]): data to sort
        attribute (str): garden data attribute as key in dictionary
    Returns:
        list[dict]: sorted data by given attribute
    """
    if attribute == "date":
        sorted_garden: list[dict] = sorted(gardens, key=lambda x: x["date"])
    elif attribute == "name":
        sorted_garden: list[dict] = sorted(gardens, key=lambda x: x["name"])
    return sorted_garden


def garden_data_manipulation(garden: Garden) -> None:
    """Editing / showing / deleting given garden data
    Args:
        garden (Garden): Garden object to manipulate
    """
    while True:
        garden.full_info()
        command: str | list[str] = get_garden_command(open_garden=True)
        if command == 1:
            pass
        elif command[0] == "back":
            break
        elif command[0] == "visual":
            visualize_garden(garden)
        elif command[0] == "export":
            name: str = get_name("Name PDF file: ")
            export_garden_pdf(garden, name)
            print("Garden was succesfuly exported")
        elif command[0] == "add":
            updated_garden: Garden = add_plant_to_garden(garden)
            garden = updated_garden
        elif command[0] == "delete":
            if confirm_to_delete(garden):
                all_gardens_menu()
                break
            else:
                print("No changes were made")
        elif command[0] == "edit":
            edited_garden: Garden = edit_garden_data(garden, command[1])
            garden = edited_garden
        elif command[0] == "remove":
            garden.garden = garden.remove_plant(command[1])


def confirm_to_delete(garden: Garden) -> True | Literal[None]:
    """Confirmation for deleting the garden from database
    Args:
        garden (Garden): Garden object to delete
    Returns:
        True | None: Returns True if deletion was confirmed
    """
    if PlantDataManager.ask_for_action(
        f"Do you really want to permanently delete - {garden.name}?"
    ):
        if PlantDataManager.ask_for_action("CONFIRM: DELETE?"):
            file = DataHandler("gardens.json")
            file.remove_entry(garden.to_dict())
            print("Garden was succesfuly deleted")
            return True


def edit_garden_data(garden: Garden, data_name: str) -> Garden:
    """Edit garden information: name / garden description
    Args:
        garden (Garden): Garden object data to edit
        data_name (str): data name to edit
    Returns:
        Garden: returns edited Garden object
    """
    garden_file = DataHandler("gardens.json")
    if data_name == "name":
        new_name: str = get_name("New Garden name:")
        garden.name = new_name
    if data_name == "info":
        text = DataHandler("edit.txt")
        text.text_editor(garden.notes)
        if editing_text():
            new_notes: str = text.read_text()
            garden.notes = new_notes
    updated_garden: dict = garden.to_dict()
    garden_file.update_file(updated_garden)
    return garden


def get_garden_command(open_garden=False) -> str | list[str]:
    """Calls commands from all_commands to process user input
    and return actions
    Args:
        open_garden (bool, optional): True, if need commands on opened Garden. 
        Defaults to False.

    Returns:
        str | list[str]: return user input as command
    """
    while True:
        try:
            user_command: str = input("Garden command: ")
            if open_garden is False:
                command: str | list[str] = all_garden_commands(user_command)
            elif open_garden is True:
                command: str | list[str] = all_garden_commands(
                    user_command, open_garden=True
                )
            if command == 1:
                pass
            if command:
                return command
        except ValueError as e:
            print(e)


def show_all_gardens(gardens=None) -> list[dict] | Literal[False]:
    """Print all gardens in the database in table format
    Args:
        gardens (list[dict], optional): Garden data to show. 
        If None, garden data loaded from default garden data file.
        Defaults to None.
    Returns:
        list[dict] | False: returns all gardens or False if no gardens found in data
    """
    if gardens is None:
        file = DataHandler("gardens.json")
        gardens: list[dict] = file.load_data()
    all_gardens: list[dict] = []
    gardens_list: list[dict] = []
    if gardens:
        for garden in gardens:
            gardens_list.append(garden)
            garden = Garden(garden)
            all_gardens.append(garden.full_info(plants=False, visual=False))
        sorted_gardens: list[dict] = sorted(
            all_gardens,
            key=lambda x: datetime.strptime(x["Created"], "%Y-%m-%d"),
            reverse=True,
        )
        enumerated_gardens: list[list[int]] = [
            [i + 1] + list(row.values()) for i, row in enumerate(sorted_gardens)
        ]
        headers: list[str] = ["No."] + list(all_gardens[0].keys())
        print(
            tabulate(
                enumerated_gardens, headers=headers, tablefmt="grid", maxcolwidths=130
            )
        )
    else:
        print("There are no gardens in the database")
        return False
    return gardens_list


def visualize_garden(garden: Garden) -> None:
    """Shows table of garden plants represented as visual indicator
    for garden height, colors, flowering and sowing times
    Args:
        garden (Garden): Garden object to visualize
    """
    garden_plants: list[dict] = garden.display_garden_plants(display=False)
    garden_visual(garden_plants)


def get_menu_answer(menu:dict) -> str:
    """Prompts user for option, given as dictionary
    Args:
        menu (dict): options as dictionary keys
    Returns:
        str: option
    """
    print("-" * 30)
    for keys, index in menu.items():
        print(f"{index[0]} - {keys}")
    print("-" * 30)
    while True:
        try:
            ask: int = int(input("Menu: "))
            for _, value in menu.items():
                if ask == value[0]:
                    return value[1]
        except ValueError:
            print("Invalid Menu input. Please choose Menu number.")


def add_plant_to_garden(garden: Garden) -> Garden:
    """Prompts user to add plants to the Garden by:
    creating new plant in database or by adding existing plant
    from plant database
    Args:
        garden (Garden): Garden to add plants to
    Returns:
        Garden: Garden object with added plants
    """
    print("=" * 30)
    adding_plants: dict[str, list] = {
        "Create New Plant": [1, "create"],
        "Add plants from database": [2, "add"],
        "Rewiew Garden Visual": [3, "review"],
        "Done adding plants": [4, "done"],
    }
    while True:
        action: str = get_menu_answer(adding_plants)
        if action == "create":
            updated_garden: Garden | None = add_new_plant(garden)
            if updated_garden:
                garden = updated_garden
        elif action == "add":
            garden_from_database: None | Literal['done'] = plant_data(garden)
            if garden_from_database:
                garden = garden_from_database
        elif action == "done":
            if not garden.garden:
                print(f"Therea are no plants in the '{garden.name}'")
                print("You need to add plants to the garden")
            if garden.garden:
                return garden
        elif action == "review":
            if not garden.garden:
                print(
                    f"The are no plants in the {garden.name}. Please first add some plants."
                )
            else:
                visualize_garden(garden)


def save_garden(garden: Garden) -> None:
    """Saves Garden object as a dictionary in 
    Garden data json file
    Args:
        garden (Garden): _description_
    """
    file = DataHandler("gardens.json")
    file.store_data(garden.to_dict())
    print(f"Garden - {garden.name} succesfuly saved!")


def confirm_garden(garden: Garden) -> Garden | Literal[False]:
    """Prompt user for saving new created Garden
    Args:
        garden (Garden): Garden to save
    Returns:
        Garden | False: returns confirmed Garden 
        or False if Garden was discarded by user
    """
    garden.full_info()
    save_garden: bool = ask_for_next(f"Do you want to save {garden.name}? ")
    if save_garden:
        return garden
    if not save_garden:
        print(f"Garden {garden.name} was discarded")
        return False


def get_name(text:str) -> str:
    """Prompt user for a new garden name
    Args:
        text (str): Question to ask the user
    Returns:
        str: garden name
    """
    while True:
        name: str = input(f"{text} ")
        if len(name) > 1 and len(name) < 100:
            return name
        else:
            print("Invalid name.")


def add_garden_notes(garden: Garden) -> Garden:
    """Prompt user for additional information about garden
    Args:
        garden (Garden): Garden for information to store to
    Returns:
        Garden: garden with added additional information
    """
    while True:
        notes: str = input(f"Additional information about {garden.name}: ")
        if notes and len(notes.split(" ")) < 200:
            garden.notes = notes
            return garden
        else:
            print("Please briefly describe your garden")


def editing_text() -> Literal[True]:
    """When editing garden additional information
    Prompt user to confirm he edited the text and saved the file
    Returns:
        True : when user confirms he finished editing
    """
    print(
        """
            Make changes to additional information and SAVE the file. 
            Did you make any changes in the editor?    
        """
    )
    while True:
        ask: str = input("Press Enter to continue... ")
        if ask == "":
            return True


def export_garden_pdf(garden: Garden, name:str) -> Garden:
    """Exports opened garden information in table to a pdf file 
    Args:
        garden (Garden): garden object to export
        name (str): name for the pdf file where data will be exported
    Returns:
        Garden: returns Garden that was exported
    """
    try:
        garden_info: dict[str, str] | None = garden.full_info(plants=False, visual=False)
        garden_plants: list[dict] | None = garden.display_garden_plants(display=False)
        plants = PlantDataManager(garden_plants)
        plants_pdf: list[dict] = plants.show_plants(full=True, printed=False)
        garden_pdf = DataToPDF([garden_info], plants_pdf, filename=name)
        garden_pdf.save_data_to_pdf()
    except Exception as e:
        print(e)
    return garden
