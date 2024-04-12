from typing import Literal
from class_data_handler import DataHandler
from class_PlantDataManager import PlantDataManager
from class_plants import Plant
import re
import copy
from all_commands import data_commands, editing_commands
from create_garden import activated_garden, active_garden

"""This file manages over actions with plant database
"""

def plant_data(garden=False) -> None | Literal['done']:
    """initializes manipulation with database

    Returns:
        "done":str: when all operations are done succesfully
    """
    if garden is False:
        file = DataHandler("plants.json")
        data = file.load_data()
        action = manipulate_database(data)
    elif garden is True:
        action = manipulate_database(data, garden=True)
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
    

        
def manipulate_database(data, garden=False) -> Literal[0]:
    while True:
        plant_data = PlantDataManager(data)
        filters: dict[str, str] = plant_data.get_actual_filters()
        if garden is True:
            command = ask_for_action(filters, garden=True)
        else:
            command: str|list = ask_for_action(filters)
        if command == "exit":
            return 0
        elif command == "mdata":
            data = reload_data()
        elif command == "adata":
            data = reload_data()
            plant_data.show_plants(data)
        elif command[0] == "sort":
            new_data = plant_data.sort_by_key(command[1])
            plant_data.show_plants(new_data)
            data = new_data
        elif command[0] == "filter":
            new_data = plant_data.filter_by_attribute_key(command[1], command[2])
            plant_data.show_plants(new_data)
            data = new_data
        elif command[0] == "edit":
            actual_data = reload_data()
            plant_to_edit = plant_data.search_plants(command[1], actual_data)
            if plant_to_edit:
                outcome: Literal['exit'] = edit_plant_info(plant_to_edit)
                if outcome == "exit":
                    data == reload_data()
            else:
                print(f"Plant with ID :{command[1]} does not exist")
        elif command[0] == "delete":
            plants = PlantDataManager()
            if plants.delete_plant(command[1]):
                data == reload_data
        elif command[0] == "full":
            plants = PlantDataManager()
            full_plant = plants.search_plants(command[1])
            if full_plant:
                plants.show_plants([full_plant], full=True)
            else:
                print(f"No plant with ID: {command[1]} exist") 
        elif command[0] == "add":
            if garden := add_plant_to_garden(command[1]):
                print(f"Plant with id {command[1]} was succesfully added to {garden} garden") 
        else:
            print("Invalid command")
            break
                             
        
def ask_for_action(actual_filters:dict, garden=False):
    while True:
        try:
            user_command: str = input("Give command: ")
            command = data_commands(user_command, actual_filters)
            if command == 1:
                raise ValueError("Invalid command")
            print(f"Command is {command}")
            return command
        except ValueError as e:
            print(e)   

def edit_plant_info(edit_plant:dict) -> Literal['exit']:
    old_version = copy.deepcopy(edit_plant)
    new_plant = {}
    while True:
        plant = PlantDataManager([edit_plant])
        print(">>>>>> Plant you want to edit:")
        plant.show_plants(full=True)
        user = input("Editing command: ")
        command = editing_commands(user)
        print(command)
        if command == 1:
            pass
        elif command == "exit":
            if new_plant:
                file = DataHandler("plants.json")
                file.remove_entry(old_version)
                file.update_data(new_plant) 
                print("Changes succesfully saved")
            return "exit"
        elif command == "abort":
            edit_plant = old_version
            print("All changes discarded")
        else:
            edit_plant = plant.edit_plant_info(edit_plant, command)
            new_plant = edit_plant
        
def add_plant_to_garden(plant_id) -> str:
    try:
        plants = PlantDataManager()
        plant_to_add = plants.search_plants(plant_id)
        if plant_to_add:
            garden = active_garden()
            if garden:
                garden.add_plant(plant_to_add)
            else:
                raise ValueError("No active garden to add to")  
        else:
            raise ValueError(f"No plant with ID {plant_id} was found")
        return garden.name
    except (ValueError, Exception) as e:
        print(e)
        raise

            
                      
  
# plant_data()
# srt = sorting_menu()
# ot = other_commands()             
# big = command_panel(filters, srt, ot)

# print(tabulate([srt], headers="keys", tablefmt="grid"))


