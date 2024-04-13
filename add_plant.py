from class_plants import PlantInfo, Plant
from class_data_handler import DataHandler
from helpers import Sep
import sys
from class_garden import Garden

# def add_new_plant() -> None:
#     s = Sep()
#     while True:
#         plant_data = DataHandler("plants.json")
#         plant_info = PlantInfo()
#         s.line(35)
#         plant_info.plant.print_plant()
#         s.line(35)
#         if confirm_plant():
#             print("Plant was saved succesfully")
#             plant:dict = plant_info.plant.to_dict()
#             plant_data.store_data(plant)
#         if not ask_for_next():
def add_new_plant(garden=False) -> None:
    s = Sep()
    while True:
        plant_data = DataHandler("plants.json")
        plant_info = PlantInfo()
        s.line(35)
        plant_info.plant.print_plant()
        s.line(35)
        plant_list = []
        saving: bool = confirm_plant()
        if saving and garden is False:
            print("Plant was saved succesfully")
            plant:dict = plant_info.plant.to_dict()
            plant_data.store_data(plant)
        elif saving and garden is True:
            print("Plant was saved succesfully and added to the garden")
            plant:dict = plant_info.plant.to_dict()
            plant_list.append(plant)
            plant_data.store_data(plant)
        continue_adding: bool = ask_for_next()
        if not continue_adding and garden is False:
            return "done" 
        if not continue_adding and garden is True:
            return plant_list

def ask_for_next(question="Do you want to continue? ") -> bool:
    while True:
        ask: str = input(f"{question}")
        ask = ask.strip().lower()
        if ask == "y":
            return True
        elif ask == "n":
            return False
        else:
            print("Invalid input. Please type 'Y' for Yes or 'N' for No.")
              
    
def confirm_plant() -> bool:
    while True:
        ask: str = input("Do you want to save this plant (Y/N)?: ")
        if ask.strip().lower() == "y":
            return True
        elif ask.strip().lower() == "n":
            return False
        else:
            print("Invalid input")
    
  