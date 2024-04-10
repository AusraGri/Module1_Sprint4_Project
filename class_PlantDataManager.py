from class_data_handler import DataHandler
from command_tables import tabulate
from class_plants import Plant, PlantInfo


class PlantDataManager:
    def __init__(self, data:list[dict]=None) -> None:
        if data is None:
            self.file = DataHandler("plants.json")
            self.data = self.file.load_data()
        else:
            self.file = DataHandler("plants.json")
            self.data: list[dict] = data

    def show_plants(self, data:list[dict]=None, full=False) -> None:
        if data is None:
            data = self.data
        if len(data) == 0:
            print("No data to show")
            return
        number = 0
        data_list = []
        add_list=[]
        for item in data:
            number += 1
            plant = Plant(item)
            info = {
                "No.:" : number,
                "Plant ID" : plant.id,
                "Name, Variety" : f"{plant.name}, {plant.variety}",
                "Scientific Name" : plant.scientific_name,
                "Type" : plant.type,
                "Height (cm)" : plant.height,
                "Sowing" : plant.sowing,
                "Flowering" : plant.flowering,
                "Color" : plant.color,
                "Light" : plant.light, 
            }
            data_list.append(info)      
        print(tabulate(data_list, headers = "keys", tablefmt="grid", maxcolwidths=35))
        if len(data) == 1 and full is True:
            info: str = f"Additional information for ID:{plant.id}: {plant.name}, {plant.variety} "
            add_info = {
                info : plant.additional_information
            }
            add_list.append(add_info)
            print(tabulate(add_list, headers = "keys", tablefmt="grid", maxcolwidths=150))  
    
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
                if key in getattr(plant, plant_attribute.lower(), None).lower():
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
    
    def existing_data_attributes(self, key:str, data=None) -> str|None:
        if data is None:
            data = self.data
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
                    actual_filters.append(str(i).lower())
            else:
                actual_filters.append(str(attr).lower())
        filters = set(actual_filters)
        # if len(filters) > 1:
        if filters:
            unique_attr = PlantDataManager.set_to_string(filters)
            return unique_attr
        else:
            return None
        
    def get_actual_filters(self, data=None) -> dict[str, str]:
        if data is None:
            data:list[dict]  = self.data
        types: str = self.existing_data_attributes("type", data)
        height: str = self.existing_data_attributes("height", data)
        sowing: str = self.existing_data_attributes("sowing", data)
        flower:str = self.existing_data_attributes("flowering", data)
        color:str = self.existing_data_attributes("color", data)
        light:str = self.existing_data_attributes("light", data)
        
        filters:dict[str,str] = {
            "name" : "type plant name",
            "type" : types,
            "height" : height,
            "sowing" : sowing,
            "flowering": flower,
            "color" : color,
            "light": light,
        }    
        return filters          
            
    
    def edit_plant_info(self, plant:dict,  key:str) -> dict:
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
            self.file.text_editor(updated_plant.additional_information)
            if PlantDataManager.editing_text():
                new_add_info:str = self.file.read_text()
                updated_plant.additional_information = new_add_info
                return updated_plant.to_dict()
                
                    

        
    
    def delete_plant(self, plant_id) -> None | bool: 
        plant = self.search_plants(plant_id)
        if not plant:
            print(f"Plant with id {plant_id} does not exist")
            return False
        self.show_plants([plant], full=True)
        if PlantDataManager.ask_for_action("Do you want to delete this plant?"):
            if PlantDataManager.ask_for_action("Confirm: DELETE the plant permanently?"):
                print(f"Plant with id {plant_id} was deleted")
                self.file.remove_entry(plant)
                return True
        else:
            print("No changes were made")
            return False
        
                    
    def search_plants(self, plant_id, data=None) -> dict :
        if data is None:
            data = self.data
        sorted_id: list[dict] = self.sort_by_key("id")
        result: dict = PlantDataManager.binary_search(sorted_id, plant_id)
        if result:
            return result     
                
    @staticmethod       
    def set_to_string(set_list):
        if all(isinstance(x, (int, float)) for x in set_list):
            string: str = f" {min(set_list)} - {max(set_list)}"
            return string   
        string = []
        sorted_list = sorted(set_list)
        for item in sorted_list:
            string.append(item)
        return string
    
    @staticmethod
    def editing_text():
        print("""
            Make changes to additional information and SAVE the file. 
            Did you make any changes in the editor?    
        """)
        while True:
            ask = input("Press Enter to continue... ")
            if ask == "":
                return True
          
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
                
                
        
    
                        
# p_data = {'id': '00044', 'name': 'Marigold', 'variety': 'Geisha Girl', 'scientific_name': 'Calendula officinalis L', 'type': 'Annual', 'height': 50, 'sowing': 'May, June', 'flowering': 'July, August, September', 'color': 'Orange', 'light': 'Full Sun', 'additional_information': 'Grown in groups with other annual flowers, in beds, balconies, pots. The flowers can be picked, the dried flowers are used for medicinal teas. Marigolds can be sown between vegetables and flowers. Their neighborhood can protect nearby plants from diseases and pests. It grows best in a sunny place, in fertile soil. It blooms all summer.'}
# plant = PlantDataManager([p_data])   
# filt: dict[str, str] = plant.get_actual_filters()
# print(filt)
# plant.show_plants(full=True)
# new_plant = plant.edit_plant_info(p_data, "additional information")
# print(new_plant)
# plant.show_plants([new_plant], full=True)
        
# v = PlantDataManager()
# v.show_plants(full=True)
# atrr: str = v.existing_data_attributes("height")
# attr2: dict[str, str] = v.get_actual_filters()
# print(atrr)
# v.show_plants()
# plant = v.search_plants("044")
# v.edit_plant_info(plant, "additional information")




    