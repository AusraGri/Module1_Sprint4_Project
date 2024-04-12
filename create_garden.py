from mailbox import MaildirMessage
from typing import Literal
from class_PlantDataManager import PlantDataManager
from class_garden import Garden
from class_data_handler import DataHandler
from class_plants import Plant

"""
when in gardens:
show statistics for how many gardens are created
commands: 
1. list existing
2. show garden by ID
3. Edit garden. 
4. add comment for garden (optional)

Prompt for garden name, add data of creation:
prompt is you want to add plants to the garden from database or create new plants?
give to Manipulate plant database to search for plants / add new plants
Database:
add additional command -> add to garden
add comand to show garden
show how many plants are in the garden, garden name and data.

when finished -> comand to finish
show all data for a garden
ask if you cant to save, export or edit.




"""
def garden_menu() -> Literal['create'] | Literal['show']:
    menu = {
        "Create new Garden": [1, "create"],
        "Show Gardens": [2, "show"],
    }
    action = get_menu_answer(menu)
    return action


def create_garden():
    name: str = get_garden_name()
    new_garden = Garden(name)
    active_garden = activate_garden(new_garden)
    
def show_all_gardens():
    
    
   
    
def activate_garden(garden: Garden):
    activation = DataHandler("active.json")
    activation.store_data(garden.to_dict())
    return garden

def active_garden():
    file = DataHandler("active.json")
    active_garden = file.load_data()
    active_garden = Garden(active_garden[0])
    return active_garden
    
    
def get_menu_answer(menu):
    for key, value in menu.items():
        print(f"{value[0]} - {key}")
    while True:
        ask: str = input("Menu: ")
        for key, value in menu.items():
            if ask == value[0]:
                return value[1]
        else:
            print("Invalid Menu input. Please choose Menu number.")
         

def add_plant_to_garden(garden):
    adding_plants = {
        "Create New Plant" : [1, "create"],
        "Add plants from database" : [2, "add"]
    }
    action = get_menu_answer(adding_plants)
    return action
    
        
def get_garden_name() -> str:
    while True:
        name: str = input("Garden name: ")
        if len(name) > 1 and len(name) < 100:
            return name
        else:
            print("Invalid name.")
              
    

    