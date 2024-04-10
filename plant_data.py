from typing import Literal
from class_data_handler import DataHandler
from class_PlantDataManager import PlantDataManager
from class_plants import Plant
import re
import copy
from command_tables import print_combined_command_tables

"""This file manages over actions with plant database
"""

def plant_data() -> None | Literal['done']:
    """initializes manipulation with database

    Returns:
        "done":str: when all operations are done succesfully
    """
    file = DataHandler("plants.json")
    data = file.load_data()
    action = manipulate_database(data)
    if action == 0:
        return "done"
    
    
        

def sorting_menu() -> dict[str, str]:
    """Menu for data sorting commands
    Returns:
        dict[str, str]: sorting menu
    """
    sorting: dict[str, str] = {
        "Plant Name": "s:name",
        "Plant Type":"s:type",
        "Plant Height":"s:height",
        "Plant Color":"s:color",
    }
    return sorting

def other_commands() -> dict[str, str]:
    """Menu for commands on data manipulation
    Returns:
        dict[str, str]: commands
    """
    other: dict[str, str] = {
        "Reset To Main Data": "mdata:",
        "Export Data To PDF file":"export:pdf",
        "Delete pland data": "delete:(plant id)",
        "Edit plant data" : "edit:(plant id)",
        "Exit to Main Menu":"exit",
        "Print all Data": "adata:",
        "Show full data" : "full:(plant id)"
    }
    return other

def reload_data() -> list[dict]:
    """Retrieves data from database json file
    Returns:
        list[dict]: plants data from json file
    """
    file = DataHandler("plants.json")
    data: list[dict] = file.load_data()
    return data
    

        
def manipulate_database(data) -> Literal[0]:
    while True:
        plant_data = PlantDataManager(data)
        filters: dict[str, str] = plant_data.get_actual_filters()
        print("COMMAND PANEL")
        print_combined_command_tables(filters, sorting_menu(), other_commands())
        command: str|list = ask_for_action(filters)
        if command == "exit":
            return 0
        elif command == "mdata:":
            data = reload_data()
        elif command == "adata:":
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
                print(f"Plant with ID:{command[1]} does not exist")
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
                print(f"No plant with ID:{command[1]} exist") 
        else:
            print("Invalid command")
            break
                             
        
def ask_for_action(actual_filters:dict):
    height = actual_filters["height"].split(" - ")
    while True:
        try:
            ask: str = input("Give command: ")
            if filt:=re.match(r"^(f:)(type|name|height|sowing|flowering|color|light):((?:\w+) ?(?:\w+))$", ask):
                filter_1 = filt.group(2)
                filter_2 = filt.group(3)
                if filter_1 == "name":
                    return ["filter", filter_1, filter_2.lower()]
                elif filter_2.isdigit() and  int(filter_2) in range(int(height[0].strip()), int(height[1].strip()) +1):
                    return ["filter", filter_1.lower(), int(filter_2)]
                elif filter_2 in actual_filters[f"{filter_1}"]:
                    return ["filter", filter_1.lower(), filter_2.lower()]
                else:
                    raise ValueError(f"Invalid filter:{filter_1}:{filter_2}")
            elif srt:=re.match(r"^(s:)(type|name|height|color)$", ask):
                srt_type = srt.group(2)
                return ["sort", srt_type]
            elif re.match(r"^mdata:$", ask):
                return "mdata:"
            elif re.match(r"^adata:$", ask):
                return "adata:"
            elif re.match(r"^exit$", ask, re.IGNORECASE):
                return "exit"
            elif e:=re.match(r"^edit:(\d{5})$", ask):
                plant_id = e.group(1)
                return ["edit", plant_id]
            elif d:=re.match(r"^delete:(\d{5})$", ask):
                plant_id = d.group(1)
                return ["delete", plant_id]
            elif f:=re.match(r"^full:(\d{5})$", ask):
                plant_id = f.group(1)
                return ["full", plant_id]
            else:
                raise ValueError(f"Invalid input: {ask}")
        except ValueError as e:
            print(e)   

def edit_plant_info(edit_plant:dict) -> Literal['exit']:
    old_version = copy.deepcopy(edit_plant)
    new_plant = {}
    while True:
        plant = PlantDataManager([edit_plant])
        plant.show_plants(full=True)
        command: str = get_editing_command()
        if command == "exit":
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
        
              
        
def get_editing_command() -> str:
    editing_options: dict[str, str] = {
        "Edit Name" : [1, "name"],
        "Edit Variety":[2, "variety"],
        "Edit Scientific Name": [3, "scientific name"], 
        "Edit Plant Type" : [4, "type"],
        "Edit Plant Height": [5, "height"], 
        "Edit Sowing Time" :[6, "sowing"],
        "Edit Flowering Time": [7, "flower"],
        "Edit Plant Color": [8, "color"],
        "Edit Plant Light Conditions": [9, "light"],
        "Edit Plant Additional Comments": [10, "additional information"],
    }
    number = 0
    for key, value in editing_options.items():
        number += 1
        print(f"{number} - {key}")
    print("To save and exit Editing Menu - exit")
    print("To discard any changes made - abort:")
    while True:
        ask: str = input("Choose what you want to EDIT: ")
        if re.match(r"^(10|[1-9]|exit|abort:)$", ask):
            if ask == "exit":
                return "exit"
            if ask == "abort:":
                return "abort"
            for key, value in editing_options.items():
                if int(ask) == value[0]:
                    return value[1]
        else:
            print("Invalid input. Please type number of your editing choice or commands: 'exit' , 'abort'")
                        
        
# def get_command(max:int) -> str:
#     while True:
#         try:
#             user_input: str = input("Command: ").strip()
#             if user_input.isdigit() and int(user_input) in range(1, max+1):
#                 return user_input
#             else:
#                 raise ValueError("Invalid menu option. Please try again.")
#         except ValueError as e:
#             print(e)


def numbered_list(name: str, items: dict) -> None:
    print(f"{name}")
    for key, index in items.items():
        print(f"{index} - {key}")
    print(f"{"-"*40}")
    
def numbered_dictionary(name:str, dictionary:dict) -> None:
    print(f"{name}")
    for key, value in dictionary.items():
        if isinstance(value, list):
            value_str = ', '.join(value)
            print(f"{key} - {value_str}")
        else:
            print(f"{key} - {value}")

            
# filters:dict[str,str] = {
#             "name" : "type plant name",
#             "type" : "types",
#             "height" : "height",
#             "sowing" : "sowing",
#             "flowering": "flower",
#             "color" : "color",
#             "light": "light",
#         } 

  
plant_data()
# srt = sorting_menu()
# ot = other_commands()             
# big = command_panel(filters, srt, ot)

# print(tabulate([srt], headers="keys", tablefmt="grid"))


