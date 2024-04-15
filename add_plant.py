from class_Plants import PlantInfo
from class_DataHandler import DataHandler
from helpers import Sep
from class_Garden import Garden

"""This program is for creation of new plants for databse
"""  

def add_new_plant(garden=None) -> None | Garden:
    """Add ne plant to database
    Args:
        garden (Garden, optional): Garden object, 
        if plant database is used for adding plant to the Garden. Defaults to None.
    Returns:
        None | Garden: Returns Garden object, when Garden is passed to the funtion
    """
    print(">>>>>>>>> ADD NEW PLANT <<<<<<<<<")
    s = Sep()
    while True:
        plant_data = DataHandler("plants.json")
        plant_info = PlantInfo()
        s.line(35)
        plant_info.plant.print_plant()
        s.line(35)
        saving: bool = ask_for_next("Do you want to save this plant?")
        if saving and garden is None:
            print("Plant was saved succesfully")
            plant:dict = plant_info.plant.to_dict()
            plant_data.store_data(plant)
        elif saving and garden:
            plant:dict = plant_info.plant.to_dict()
            plant_data.store_data(plant)
            garden.add_plant(plant)
            print("Plant was saved succesfully and added to the garden")
        continue_adding: bool = ask_for_next()
        if not continue_adding and garden is None:
            return "done" 
        if not continue_adding and garden:
            return garden

def ask_for_next(question="Do you want to continue? ") -> bool:
    """ Get user bool answerfor any question
    Args:
        question (str, optional): Optional question to ask. Defaults to "Do you want to continue? ".
    Returns:
        bool: Returns True is answer is YES, and False if answer is NO
    """
    while True:
        ask: str = input(f"{question} ")
        ask = ask.strip().lower()
        if ask == "y":
            return True
        elif ask == "n":
            return False
        else:
            print("Invalid input. Please type 'Y' for Yes or 'N' for No.")
              