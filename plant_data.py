from numpy import append
from class_PlantDataManager import PlantDataManager
from class_plants import Plant

"""
Menu:
1. View and interact with data
2. edit/delete plants
3. export data to PDF
adata: -> prints all database
filter: (type, name, height, sowing, flowering, color, light) -> give actual suggestions from database
filter: (name) -> give promp for name
sort: type -> data sorted by type
mdata -> back to main data
delete:(id) -> delete plant
inf:(id) -> full info with comments
edit:(id)-> edit plant entry -> what to edit: 
help -> get all commands printed


Filter by:
1 - plant type:
    a. annual
    b. perrenial
2 - plant name
3 - plant height
4 - plant sowing
5 - plant flowering
6 - plant - color
7 - plant light

"""


def plant_data():
    plant_data = PlantDataManager()
    actual_filter_keys("light", plant_data.data)


def menu_filter():
    filters = [
        "Plant Name",
        "Plant Type",
        "Plant Height",
        "Plant Sowing Time",
        "Plant Flowering Time",
        "Plant Color",
        "Plant Lighting Conditions",
    ]
    numbered_list("Filters:", filters)
    option = get_command(7)
    
def actual_filter_keys(key:str, data: list) -> set:
    actual_filters:list = []
    if key.split(" "):
            key:str = key.replace(" ", "_")
    for item in data:
        plant = Plant(item)
        attr = getattr(plant, key.lower(), None)
        if key == "height":
            actual_filters.append(attr)
    
        elif s := attr.split(", "):
            for i in s:
                actual_filters.append(str(i))
        else:
            actual_filters.append(str(attr))
    filters = set(actual_filters)
    return filters

        
            
            
            
    
    # filter_actions = {
    #     "1": plants_database,
    #     "2": edit_database,
    #     "exit": exit_menu,
    # }
    # while True:
    #     user_input: str = input("Enter menu navigation: ").strip().lower()
    #     action = menu_actions.get(user_input)
    #     if action:
    #         break
    #     else:
    #         print("Invalid menu option. Please try again.")
    
    

def filter_data(filter, data):
    ...



def get_command(max:int) -> str:
    while True:
        try:
            user_input: str = input("Command: ").strip()
            if user_input.isdigit() and int(user_input) in range(1, max+1):
                return user_input
            else:
                raise ValueError("Invalid menu option. Please try again.")
        except ValueError as e:
            print(e)


def numbered_list(name: str, items: list) -> None:
    print(f"{name}")
    for index, option in enumerate(items, start=1):
        print(f"{index} - {option}")
    print(f"{"-"*40}")


def plant_data_menu() -> None:
    menu: list[str] = ["Filter / sort data", "Edit / Delete plants", "Exit"]
    numbered_list("Plant Database Menu:", menu)
    print(f"{"-"*40}")
    menu_actions = {
        "1": plants_database,
        "2": edit_database,
        "exit": exit_menu,
    }
    while True:
        user_input: str = input("Enter menu navigation: ").strip().lower()
        action = menu_actions.get(user_input)
        if action:
            break
        else:
            print("Invalid menu option. Please try again.")
            
            
plant_data()
