from typing import Literal
from class_DataHandler import DataHandler
from class_PlantDataManager import PlantDataManager
import copy
from all_commands import data_commands, editing_commands
from class_Garden import Garden
from class_DataToPDF import DataToPDF

"""Manages over actions with plant database
"""

def plant_data( garden=None, )-> Garden | Literal['done']:
    """Starting plant database function to differenciate actions
    needed if plant data will be used for adding plants to Garden
    or for viewing / editing plant database
    Args:
        garden (Garden obj.): Garden object when dtabase is used for 
        adding plants to garden
    Returns:
        str: return "done" when all user actions on database are finished
    """
    print(">>>>>>>> PLANTS DATABASE <<<<<<<<<<")
    file = DataHandler("plants.json")
    data: list[dict] = file.load_data()
    if garden is None:
        action: Garden|0 = manipulate_database(data)
    elif garden:
        garden_plants: Garden | 0 = manipulate_database(data, garden )
        if garden_plants:
            return garden_plants
    if action == 0:
            return "done" 

def reload_data() -> list[dict]:
    """Retrieves data from database json file
    Returns:
        list[dict]: plants data from json file
    """
    file = DataHandler("plants.json")
    data: list[dict] = file.load_data()
    return data
    
        
def manipulate_database(data: list[dict], garden=None) -> Garden | int:
    """Proceeds commands for editing / filtering / sorting / deleting
    plant data in database
    Args:
        data (list[dict]): data for actions
        garden (Garden, optional): Garden object for adding plants.
        Defaults to None.
    Returns:
        Garden | 0: returns Garden or 0 when finished working with plant database
    """
    print("To see all commands, type '-h' or '--help'")
    while True:
        plant_data = PlantDataManager(data)
        filters: dict[str, str] = plant_data.get_actual_filters()
        if garden:
            command = ask_for_action(filters, garden=True)
        else:
            command: str|list = ask_for_action(filters)
        if command[0] == "exit" and garden is None:
            return 0
        elif command[0] == "exit" and garden:
            return garden
        elif command[0] == "mdata":
            data: list[dict] = reload_data()
        elif command[0] == "adata":
            data = reload_data()
            plant_data.show_plants(data)
        elif command[0] == "export":
            name: str = get_pdf_name()
            export_data_to_pdf(data, name)
            print(f"Your data was exported to {name}.pdf")
        elif command[0] == "sort":
            new_data: list[dict] = plant_data.sort_by_key(command[1])
            plant_data.show_plants(new_data)
            data = new_data
        elif command[0] == "filter":
            new_data = plant_data.filter_by_attribute_key(command[1], command[2])
            plant_data.show_plants(new_data)
            data = new_data
        elif command[0] == "edit":
            actual_data: list[dict] = reload_data()
            plant_to_edit: dict = plant_data.search_plants(command[1], actual_data)
            if plant_to_edit:
                outcome: Literal['exit'] = edit_plant_info(plant_to_edit)
                if outcome == "exit":
                    data = reload_data()
            else:
                print(f"Plant with ID :{command[1]} does not exist")
        elif command[0] == "delete":
            plants = PlantDataManager()
            if plants.delete_plant(command[1]):
                data == reload_data
        elif command[0] == "full":
            plants = PlantDataManager()
            full_plant: dict = plants.search_plants(command[1])
            if full_plant:
                plants.show_plants([full_plant], full=True)
            else:
                print(f"No plant with ID: {command[1]} exist") 
        elif command[0] == "add":
            try:
                plant_to_garden: Garden = add_plant_to_garden(command[1], garden)
                if plant_to_garden:
                    garden: Garden = plant_to_garden 
            except ValueError:
                pass
        else:
            print("Invalid command")
            break
                             
        
def ask_for_action(actual_filters:dict, garden=None) -> str | list[str]:
    """Prompts user input as command line for argarser and retieves
    coresponding command for action
    Args:
        actual_filters (dict): available filtering values from plant database
        garden (Garden, optional): Garden object to add plants to.
        Defaults to None.
    Raises:
        ValueError: if user input is invalid and argparser raises system exit error
    Returns:
        str | list[str]: returns formated command
    """
    while True:
        try:
            user_command: str = input("Database command: ")
            if garden is None:
                command: str | list[str] = data_commands(user_command, actual_filters)
            elif garden:
                command: str | list[str] = data_commands(user_command, actual_filters, garden=True)
            if command == 1:
               raise ValueError("Invalid command")
            return command
        except ValueError as e:
            print(e)   

def edit_plant_info(edit_plant:dict) -> Literal['exit']:
    """Plant editing commands are processed here
    Args:
        edit_plant(dict): plant information to edit
    Returns:
        str: returns "exit" when user finishes editing
    """
    old_version: dict = copy.deepcopy(edit_plant)
    new_plant: dict = {}
    while True:
        plant = PlantDataManager([edit_plant])
        print(">>>>>> Plant you want to edit:")
        plant.show_plants(full=True)
        user: str = input("Editing command: ")
        command: str | list[str] = editing_commands(user)
        if command == 1:
            pass
        elif command == "exit":
            if new_plant:
                file = DataHandler("plants.json")
                file.update_file(new_plant) 
                print("Changes succesfully saved")
            return "exit"
        elif command == "abort":
            edit_plant = old_version
            print("All changes discarded")
        else:
            edit_plant = plant.edit_plant_info(edit_plant, command)
            new_plant = edit_plant
            
        
def add_plant_to_garden(plant_id: str, garden: Garden) -> Garden:
    """Saves plant to Garden object data
    Args:
        plant_id (str): plant Id to save in Garden plants list
        garden (Garden): Garden to save to
    Raises:
        ValueError: if given plant id is not in plant database
    Returns:
        Garden: returns updated Garden data
    """
    try:
        plants = PlantDataManager()
        plant_to_add: dict = plants.search_plants(plant_id)
        if plant_to_add:
            if plant_to_add["id"] not in garden.garden:
                garden.add_plant(plant_to_add)
                print(f"Plant: {plant_to_add["name"]} was succesfully added to - {garden.name}")
                return garden
            else:
                print(f"Plant {plant_to_add["name"]} is alredy in the garden - {garden.name}")      
        else:
            raise ValueError(f"No plant with ID {plant_id} was found")
    except (ValueError, Exception) as e:
        print(e)

    
def get_pdf_name() -> str:
    """Prompt user for the pdf name, 
    before exporting data to pfd
    Returns:
        str: filename
    """
    while True:
        ask: str = input("Name for pdf file: ")
        if ask:
            return ask
    

def export_data_to_pdf(data:list[dict], name:str) -> None:
    """Exports users current filtered / sorted / all plant data
    to a table in pdf file 
    Args:
        data (list[dict]): data to export
        name (str): name for the pdf file
    """
    data = PlantDataManager(data)
    data_to_export: list[dict] = data.show_plants(full=True, printed=False)
    exp = DataToPDF(data_to_export, filename=name)
    exp.save_data_to_pdf()
