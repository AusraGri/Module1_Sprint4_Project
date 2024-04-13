from typing import Literal
from class_data_handler import DataHandler
from class_PlantDataManager import PlantDataManager
import copy
from all_commands import data_commands, editing_commands

"""This file manages over actions with plant database
"""

def plant_data(garden=False) -> None | Literal['done']:
    """initializes manipulation with database

    Returns:
        "done":str: when all operations are done succesfully
    """
    file = DataHandler("plants.json")
    data = file.load_data()
    if garden is False:
        action = manipulate_database(data)
    elif garden is True:
        garden_plants = manipulate_database(data, garden=True)
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
    

        
def manipulate_database(data, garden=False) -> Literal[0]:
    plants_for_garden = []
    while True:
        plant_data = PlantDataManager(data)
        filters: dict[str, str] = plant_data.get_actual_filters()
        if garden is True:
            command = ask_for_action(filters, garden=True)
        else:
            command: str|list = ask_for_action(filters)
        if command == "exit" and garden is False:
            return 0
        elif command == "exit" and garden is True:
            return plants_for_garden
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
            plant_to_garden = add_plant_to_garden(command[1])
            plants_for_garden.append(plant_to_garden)
            print(f"Plant {plant_to_garden["name"]} succesfully added to garden")
        else:
            print("Invalid command")
            break
                             
        
def ask_for_action(actual_filters:dict, garden=False):
    while True:
        try:
            user_command: str = input("Give command: ")
            if garden is False:
                command = data_commands(user_command, actual_filters)
            elif garden is True:
                command = data_commands(user_command, actual_filters, garden=True)
            if command == 1:
               pass
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
        
def add_plant_to_garden(plant_id) -> dict:
    try:
        plants = PlantDataManager()
        plant_to_add = plants.search_plants(plant_id)
        if plant_to_add:
            return plant_to_add   
        else:
            raise ValueError(f"No plant with ID {plant_id} was found")
    except (ValueError, Exception) as e:
        print(e)
        raise

            
                      
  
# plant_data()
# srt = sorting_menu()
# ot = other_commands()             
# big = command_panel(filters, srt, ot)

# print(tabulate([srt], headers="keys", tablefmt="grid"))


