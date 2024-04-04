from class_plants import Plant


class Garden:
    def __init__(self) -> None:
        self.garden: list = []    
        
    def add_plant(self, plant: Plant) -> None:
        self.garden.append(plant)
        
    def remove_plant(self, plant: Plant) -> None:
        if plant in self.garden:
            self.garden.remove(plant)
            print(f"{plant.name} was removed from the garden")
        else:
            print("Plant not found in the garden.")
            
    def display_garden(self) -> None:
        print("Plants in the garden: ")
        for plant in self.garden:
            print(plant.name)
            
    