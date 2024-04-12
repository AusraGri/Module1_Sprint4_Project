from re import A
from class_PlantDataManager import PlantDataManager
from class_plants import Plant
from datetime import datetime


class Garden:
    def __init__(self, data:str|dict) -> None:
        if isinstance(data, str):
            self.garden_id: str = datetime.now().strftime("%d%H%M%S")
            self.name: str = data
            self.date: str = datetime.now().strftime("%Y-%m-%d")
            self.garden: list = []
        elif isinstance(data, dict):
            required_keys: set[str] = {"garden_id", "name", "date", "garden"}
            if required_keys.issubset(data.keys()):
                try:
                    self.garden_id = data["garden_id"]
                    self.name = data["name"]
                    self.date = data["date"]
                    self.garden = data["garden"]
                except KeyError as e:
                    print(f"Invalid dictionary key for: {e}")
            else:
                    print("Required keys are missing in the dictionary.")
        else:
            print("Invalid data for Garden")
       
        
    def to_dict(self) -> dict:
        return self.__dict__
        
    def add_plant(self, plant: dict) -> None:
        plant = Plant(plant)
        self.garden.append(plant.id)
        
    def remove_plant(self, plant_id: str) -> None:
        for plant in self.garden:
            if plant.id in self.garden:
                self.garden.remove(plant)
                print(f"{plant.name} was removed from the garden")
            else:
                print("Plant not found in the garden.")
            
    def display_garden(self) -> None:
        print("Plants in the garden: ")
        garden_plants =[]
        for plant_id in self.garden:
            data = PlantDataManager()
            plant = data.search_plants(plant_id)
            if plant:
                garden_plants.append(plant)
        data.show_plants(garden_plants, full=True)
        
    def garden_information_dict(self):
        garden = {
            "garden id" : self.garden_id,
            "garden name" : self.name,
            "created" : self.date,
            "garden plants" : self.garden,
        }
        return garden
            

one = {
        "id": "00044",
        "name": "Marigold",
        "variety": "Geisha Girl",
        "scientific_name": "Calendula officinalis L",
        "type": "Annual",
        "height": 50,
        "sowing": "May, June",
        "flowering": "July, August, September",
        "color": "Orange",
        "light": "Full Sun",
        "additional_information": "Grown in groups with other annual flowers, in beds, balconies, pots. The flowers can be picked, the dried flowers are used for medicinal teas. Marigolds can be sown between vegetables and flowers. Their neighborhood can protect nearby plants from diseases and pests. It grows best in a sunny place, in fertile soil. It blooms all summer."
    }

two = {
        "id": "00043",
        "name": "Zinnia",
        "variety": "Envy",
        "scientific_name": "Zinnia elegans dahlienflora",
        "type": "Annual",
        "height": 90,
        "sowing": "May, June",
        "flowering": "June, July, August, September",
        "color": "Green, Yellow",
        "light": "Full Sun",
        "additional_information": "Annual, 90 cm high, fast-growing flowers. Planted in flower gardens, picked for bouquets. The flowers are large, 8-10 cm in diameter, semi-full. It grows and blooms well in a sunny, warm place, in light soil. Seedlings are planted in flower beds after the end of frost. Watering is not necessary, but the inflorescences of irrigated plants are larger and bloom longer. Inflorescences that have bloomed are cut off so that new ones can form faster."
    }
info = {"garden_id": "11105525", "name": "new", "date": "2024-04-11", "garden": ["something"]}
# gard = Garden(info)
# print(gard.name, gard.garden)
# garden.add_plant(one)
# garden.add_plant(two)
# garden.display_garden()

