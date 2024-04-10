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

def add_plant_to_garden():
    plants = PlantDataManager()
    for _ in plants:
        plant = Plant(_)
        
    
    

        
    