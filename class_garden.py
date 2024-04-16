from class_PlantDataManager import PlantDataManager
from class_plants import Plant
from datetime import datetime
from tabulate import tabulate

"""Class to create/ store / edit information about the Garden
    Returns:
        object|dict : returns Garden object or Garden inforamtion as dictionary
    """

class Garden:
    def __init__(self, data:str|dict) -> None:
        """Takes parameter and if it is a string initializzes new Garden object
        If it is a given dictionary of converted Garden object to dictionary
        takes parameters from dictionary

        Args:
            data (str | dict): string for new Garden object, 
            dictionary for getting parameters from dictionary
        """
        if isinstance(data, str):
            self.garden_id: str = datetime.now().strftime("%d%H%M%S")
            self.name: str = data
            self.date: str = datetime.now().strftime("%Y-%m-%d")
            self.garden: list = []
            self.notes = None
        elif isinstance(data, dict):
            required_keys: set[str] = {"garden_id", "name", "date", "garden"}
            if required_keys.issubset(data.keys()):
                try:
                    self.garden_id = data["garden_id"]
                    self.name = data["name"]
                    self.date = data["date"]
                    self.garden = data["garden"]
                    self.notes = data["notes"]
                except KeyError as e:
                    print(f"Invalid dictionary key for: {e}")
            else:
                    print("Required keys are missing in the dictionary.")
        else:
            print("Invalid data for Garden")
       
        
    def to_dict(self) -> dict:
        """Converts object to dictionary

        Returns:
            dict: returns dictionary
        """
        return self.__dict__
        
    def add_plant(self, plant: dict) -> None:
        """adds plant id to the Garden
        Args:
            plant (dict): plant object as dictionary
        """
        plant = Plant(plant)
        self.garden.append(plant.id)
    
    def add_notes(self, text:str) -> None:
        """Adds additional information about Garden
        Args:
            text (str): text
        """
        self.notes: str = text
        
    def remove_plant(self, plant_id: str) -> None:
        """Removes plant id from Garden plants list
        Args:
            plant_id (str): Plant id to remove
        Returns:
            list: returns updated garden list of plants
        """
        if plant_id in self.garden:
            self.garden.remove(plant_id)
            print("Plant was removed from the garden")
        else:
            print("Plant not found in the garden.")
        return self.garden
    
    def plant_names_in_garden(self) -> str:
        """Retrieves plant names that are in the Garden list
        Returns:
            str: plant name and variety in a single string
        """
        garden_plant_names: str =""
        for plant_id in self.garden:
            data = PlantDataManager()
            plant: dict = data.search_plants(plant_id)
            if plant:
                plant = Plant(plant)
                garden_plant_names += f"{plant.name} ({plant.variety}), "
            if not plant:
                del plant_id
        garden_plant_names = garden_plant_names[:-2]
        return garden_plant_names
            
    def display_garden_plants(self, display=True) -> list[dict]:
        """Retrieve or print all plants that are in the Garden with full information
        Args:
            display (bool, optional): To enable(True)/disable(False) printing. 
            Defaults to True.
        Returns:
            list[dict]: returns information as list of plant dictionaries
        """
        if display is True:
            print("Plants in the garden: ")
        garden_plants: list =[]
        for plant_id in self.garden:
            data = PlantDataManager()
            plant: dict = data.search_plants(plant_id)
            if plant:
                garden_plants.append(plant)
            if not plant:
                del plant_id
        if display is True:
            data.show_plants(garden_plants)
        return garden_plants
    
    def full_info(self, plants=True, visual=True) -> dict[str, str] | None:
        """Prints out or returns information about the Garden
        Args:
            plants (bool, optional): To exclude plants names and variety set to False. 
            Defaults to True.
            visual (bool, optional): To disable printing set to False. 
            Defaults to True.
        Returns:
            dict[str, str] | None: returns informations about Garden as dictionary 
            or prints it out
        """
        info: dict[str, str] = {
                "Garden ID": self.garden_id,
                "Garden Name" : self.name,
                "Created" : self.date,
                "Garden Description" : self.notes,
            }
        if visual is True:
            print(tabulate([info], headers = "keys", tablefmt="grid", maxcolwidths=100))
        if plants is True and visual is True:
            self.display_garden_plants()
        if plants is True and visual is False:
            plants: list[dict] = self.display_garden_plants(display=False)
            info.update({"Garden Plants" : f"{plants["name"]} ({plants["variety"]})"})
            return info
        if plants is False and visual is False:
            return info
  
