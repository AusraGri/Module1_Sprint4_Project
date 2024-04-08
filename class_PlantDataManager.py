from class_data_handler import DataHandler
from tabulate import tabulate
from class_plants import Plant, PlantInfo


class PlantDataManager:
    def __init__(self) -> None:
        self.file = DataHandler("plants.json")
        self.data: list[dict] = self.file.load_data()

    def show_plants(self, data=None) -> None:
        if data is None:
            data = self.data
        number = 0
        data_list = []
        for item in data:
            number += 1
            plant = Plant(item)
            info = {
                "No.:" : number,
                "Plant ID" : plant.id,
                "Name, Variety" : f"{plant.name}, {plant.variety}",
                "Scientific Name" : plant.scientific_name,
                "Type" : plant.type,
                "Height" : plant.height,
                "Sowing" : plant.sowing,
                "Flowering" : plant.flowering,
                "Color" : plant.color,
                "Light" : plant.light, 
            }
            data_list.append(info)
                
        print(tabulate(data_list, headers = "keys", tablefmt="grid", maxcolwidths=30))
    
    def filter_by_attribute_key(self, plant_attribute:str, key:str, data=None) -> list[dict]:
        if data is None:
            data = self.data
        filtered_data: list[dict] =[]
        if plant_attribute.split(" "):
            plant_attribute:str = plant_attribute.replace(" ", "_")
        for item in data:
            plant = Plant(item)
            if isinstance(key, int):
                mini: int = key - 10
                maxi: int = key + 10
                if  maxi >= getattr(plant, plant_attribute.lower(), None) >= mini:
                    filtered_data.append(item)
            else:
                if key in getattr(plant, plant_attribute.lower(), None):
                    filtered_data.append(item)
        if not filtered_data:
            print(f"No data was found by {plant_attribute} and {key}")
        else:
            return filtered_data
    
    def sort_by_key(self, key, data=None) -> list[dict]:
        if data is None:
            data: list[dict] = self.data
        sorted_data: list[dict] = sorted(data, key=lambda x: x[f"{key.lower()}"])
        return sorted_data
    
    def existing_data_attributes(self, attr:str, data=None) -> set:
        if data is None:
            data: list[dict] = self.data
        attributes:list = []
        for item in data:
            for key, value in item.items():
                if key == attr.lower():
                    attributes.append(value)
        unique_attr = set(attributes)
        return unique_attr
        
                    
            
        
        
    
    
    def edit_plant_info(self, plant:dict,  key:str) -> dict:
        self.show_plants([plant])
        updated_plant = Plant(plant)
        key = key.lower()
        if key == "type":
            new_type: str = PlantInfo.get_plant_type()
            updated_plant.type = new_type
            return updated_plant.to_dict()
        elif key == "height":
            new_height: int = PlantInfo.get_plant_height()
            updated_plant.height = new_height
            return updated_plant.to_dict()
        elif key == "sowing":
            new_sowing: str = PlantInfo.get_sowing_time()
            updated_plant.sowing = new_sowing
            return updated_plant.to_dict()
        elif key == "flowering":
            new_flowering: str = PlantInfo.get_flowering_time()
            updated_plant.flowering = new_flowering
            return updated_plant.to_dict()
        elif key == "color":
            new_color: str = PlantInfo.get_color()
            updated_plant.color = new_color
            return updated_plant.to_dict()
        elif key == "light":
            new_light: str = PlantInfo.get_lighting()
            updated_plant.light = new_light
            return updated_plant.to_dict()
        elif key == "name":
            new_name: str = PlantInfo.get_common_name()
            updated_plant.name = new_name
            return updated_plant.to_dict()
        elif key == "variety":
            new_variety: str = PlantInfo.get_variety_name()
            updated_plant.variety = new_variety
            return updated_plant.to_dict()
        elif key == "scientific name":
            new_scientific_name: str = PlantInfo.get_scientific_name()
            updated_plant.scientific_name = new_scientific_name
            return updated_plant.to_dict()
        elif key == "additional information":
            self.file.open_text_editor(updated_plant.additional_information)
            new_add_info:str = self.file.read_text()
            updated_plant.additional_information = new_add_info
            return updated_plant.to_dict()
                
        
    
    def delete_plant(self, plant_id) -> None: 
        plant = self.search_plants(plant_id)
        if not plant:
            print(f"Plant with id {plant_id} does not exist")
            return
        self.show_plants([plant])
        if PlantDataManager.ask_for_action("Do you want to delete this plant?"):
            if PlantDataManager.ask_for_action("Confirm: DELETE the plant permanently?"):
                print(f"Plant with id {plant_id} was deleted")
                self.file.remove_entry(plant)
        else:
            print("No changes were made")
        
                    
    def search_plants(self, plant_id) -> dict :
        sorted_id: list[dict] = self.sort_by_key("id")
        result: dict = PlantDataManager.binary_search(sorted_id, plant_id)
        if result:
            return result             
            
            
    @staticmethod       
    def ask_for_action(action:str) -> bool:
        while True:
            ask: str = input(f"{action} (Y/N): ").lower()
            if ask == "y":
                return True
            elif ask == "n":
                return False
            else:
                print("Wrong input: 'Y' for 'YES' and 'N' for 'NO'")        
                
    @staticmethod           
    def binary_search(data:list, id:str,):
        x = int(id)
        low = 0
        high: int = len(data) - 1
        while low <= high:
            mid: int = low + (high - low)//2
            if int(data[mid]["id"]) == x:
                return data[mid]
            elif int(data[mid]["id"]) < x:
                low: int = mid + 1
            else:
                high = mid - 1
        return None
                
                
        
    
                        
                
# v =PlantDataManager()
# v.show_plants()
# plant = v.search_plants("044")
# v.edit_plant_info(plant, "additional information")




    