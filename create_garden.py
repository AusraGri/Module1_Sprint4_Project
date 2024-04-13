
from tabulate import tabulate
from typing import Literal
from class_garden import Garden
from class_data_handler import DataHandler
from class_plants import Plant
from add_plant import add_new_plant, ask_for_next
from database import plant_data
from garden_visual_table import garden_visual

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
        "Exit Gardens" : [3, "exit"]
    }
    while True:
        action = get_menu_answer(menu)
        if action == "create":
            create_garden()
        if action == "show":
            pass
            

def create_garden():
    name: str = get_garden_name()
    create_garden = Garden(name)
    active_garden = activate_garden(create_garden)
    new_garden = add_plant_to_garden(create_garden)
    if new_garden == "done":
        confirmed_garden = confirm_garden(create_garden)
        if confirmed_garden:
            save_garden(confirmed_garden)
            deactivate()
        else:
            deactivate()
            
     
    
def show_all_gardens():
    file = DataHandler("gardens.json")
    gardens = file.load_data()
    number = 0
    for garden in gardens:
        garden = Garden(garden)
        info = {
            "No.:" : number + 1,
            "Garden ID": garden.garden_id,
            "Garden Name" : garden.name,
            "Created" : garden.date,
            "Plants in Garden" : garden.plant_names_in_garden()
        }
        print(tabulate([info], headers = "keys", tablefmt="grid", maxcolwidths=100))
        garden.display_garden_plants()
       
    

    
def visualize_garden(garden):
    garden_plants = garden.display_garden_plants(display=False) 
    garden_visual(garden_plants)  
    
   
    
def activate_garden(garden: Garden):
    activation = DataHandler("active.json")
    activation.store_data(garden.to_dict())
    garden = Garden(garden)
    return garden

# def active_garden():
#     file = DataHandler("active.json")
#     active_garden = file.load_data()
#     activated = Garden(active_garden[0])
#     return activated

def deactivate():
    file = DataHandler("active.json")   
    file.delete_allowed = True
    file.delete_all()
    
def get_menu_answer(menu):
    for keys, index in menu.items():
        print(f"{index[0]} - {keys}")
    while True:
        try:
            ask: int = int(input("Menu: "))
            for _ , value in menu.items():
                if ask == value[0]:
                    return value[1]
        except ValueError:
            print("Invalid Menu input. Please choose Menu number.")
         

def add_plant_to_garden(garden: Garden):
    adding_plants = {
        "Create New Plant" : [1, "create"],
        "Add plants from database" : [2, "add"],
        "Rewiew Garden" : [3, "review"],
        "Done adding plants" : [4, "done"],
    }
    while True:
        action = get_menu_answer(adding_plants)
        if action == "create":
            plants_to_add = add_new_plant(garden=True)
            if plants_to_add:
                for plant in plants_to_add:
                    garden.add_plant(plant)
            else:
                print(f"No new plants were added to {garden.name} garden")
        elif action == "add":
            plants_to_add = plant_data(garden=True)
            if plants_to_add:
                 for plant in plants_to_add:
                    garden.add_plant(plant)
        elif action == "done":
            if not garden.garden:
                print(f"Therea are no plants in the '{garden.name}'")
                print("You need to add plants to the garden")
            if garden.garden:
                return "done"
                
                
def save_garden(garden):
    file = DataHandler("gardens.json")   
    file.store_data(garden.to_dict()) 
    print(f"Garden - {garden.name} succesfuly saved!") 
        
                
        
def confirm_garden(garden):
    garden.display_garden_plants()
    save_garden = ask_for_next(f"Do you want to save {garden.name}? ")
    if save_garden:
        return garden
    if not save_garden:
        print(f"Garden {garden.name} was discarded")
        return False
        
       
        
def get_garden_name() -> str:
    while True:
        name: str = input("Garden name: ")
        if len(name) > 1 and len(name) < 100:
            return name
        else:
            print("Invalid name.")
              
  #suchekinti kad nedetu tu paciu augalu
  
  
    
# file = DataHandler("gardens.json")
# gardens = file.load_data()
# for garden in gardens:
#     garden = Garden(garden)
#     visualize_garden(garden)

    