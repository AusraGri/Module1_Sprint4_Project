from typing import Literal
from class_DataHandler import DataHandler
from class_plants import Plant, PlantInfo
from tabulate import tabulate

"""For working with plant database: soting/ filterins / editing data in plant database
"""

class PlantDataManager:
    def __init__(self, data: list[dict] = None) -> None:
        """Takes a list of dictionaries of plant data
        Args:
            data (list[dict], optional): Plant data stored as a list of dictionaries
            If no data given, retrieves data from default plant data file
            Defaults to None.
        """
        if data is None:
            self.file = DataHandler("plants.json")
            self.data = self.file.load_data()
        else:
            self.file = DataHandler("plants.json")
            self.data: list[dict] = data

    def show_plants(self, data: list[dict] = None, full=False, printed=True) -> None | list[dict]:
        """Prints out or returns data in the given plant data
        Args:
            data (list[dict], optional): if no data given, 
            data will be retrieved from default plant data file. 
            Defaults to None.
            full (bool, optional): To include additional information from plant data, set to True. 
            Defaults to False.
            printed (bool, optional): To disable printing data, set to False. 
            Defaults to True.

        Returns:
            list[dict]: returns plant data as list of dictionaries
        """
        if data is None:
            data = self.data
        if len(data) == 0:
            print("No data to show")
            return
        number = 0
        plants_to_show: list = []
        for item in data:
            number += 1
            plant = Plant(item)
            info: dict[str, str | int] = {
                "No.:": number,
                "Plant ID": plant.id,
                "Name, Variety": f"{plant.name}, {plant.variety}",
                "Scientific Name": plant.scientific_name,
                "Type": plant.type,
                "Height (cm)": plant.height,
                "Sowing": plant.sowing,
                "Flowering": plant.flowering,
                "Color": plant.color,
                "Light": plant.light,
            }
            if full is True:
                if printed is True:
                    print(tabulate([info], headers="keys", tablefmt="grid", maxcolwidths=35))
                infor: str = (
                    f"Additional information for ID:{plant.id}: {plant.name}, {plant.variety} "
                )
                add_info: dict[str] = {infor: plant.additional_information}
                if printed is True:
                    print(tabulate([add_info],headers="keys",tablefmt="grid",maxcolwidths=170,))
                    print("=" * 20)
                if printed is False:
                    info["Additional Information"] = plant.additional_information
                plants_to_show.append(info)
            else:
                plants_to_show.append(info)
        if full is False and printed is True:
            print(tabulate(plants_to_show, headers="keys", tablefmt="grid", maxcolwidths=35))
        else:
            return plants_to_show

    def filter_by_attribute_key(self, plant_attribute: str, key: str, data=None) -> list[dict]:
        """Filted given plant database by plant atrribute and feature
        Args:
            plant_attribute (str): Plant atrribute saved as dictioanry keys
            key (str): Saved plant features in attribute key
            data (list[dict], optional): Plant data to filter. 
            If None, takes all data from default plant data file.
            Defaults to None.

        Returns:
            list[dict]: returns filtered data by given plant attribute and feature
        """
        if data is None:
            data: list[dict] = self.data
        filtered_data: list[dict] = []
        if plant_attribute.split(" "):
            plant_attribute: str = plant_attribute.replace(" ", "_")
        for item in data:
            plant = Plant(item)
            if isinstance(key, int):
                mini: int = key - 10
                maxi: int = key + 10
                if maxi >= getattr(plant, plant_attribute.lower(), None) >= mini:
                    filtered_data.append(item)
            else:
                if key in getattr(plant, plant_attribute.lower(), None).lower():
                    filtered_data.append(item)
        if not filtered_data:
            print(f"No data was found by {plant_attribute} and {key}")
        else:
            return filtered_data

    def sort_by_key(self, key:str, data=None) -> list[dict]:
        """Sorts plant data by given plant attribute, saved as plant dictionary key
        Args:
            key (str): Key from plant information dictionary keys
            data (list[dict], optional): Plant data to sort. 
            If None, takes all data from default plant data file.
            Defaults to None.
        Returns:
            list[dict]: returns sorted data
        """
        if data is None:
            data: list[dict] = self.data
        sorted_data: list[dict] = sorted(data, key=lambda x: x[f"{key.lower()}"])
        return sorted_data

    def existing_data_attributes(self, key: str, data=None) -> str| None:
        """Reads given plant data and collects possible features saved in plant key attributes
        Args:
            key (str): Plant attribute saved as key in plant data dictionary
            data (list[dict], optional): Plant data to work with. 
            If None, takes all data from default plant data file. 
            Defaults to None.
        Returns:
            list | None: If there are features in key, returns a list of features, 
            else returns None
        """
        if data is None:
            data: list[dict] = self.data
        actual_filters: list = []
        if key.split(" "):
            key: str = key.replace(" ", "_")
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
        if filters:
            unique_attr: str = PlantDataManager.set_to_string(filters)
            return unique_attr
        else:
            return None

    def get_actual_filters(self, data=None) -> dict[str, str]:
        """Collects all actual plant attributes and features from plant database
        Args:
            data (list[dict], optional): Plant data to work with. 
            If None, takes all data from default plant data file. 
            Defaults to None.
        Returns:
            dict[str, str]: Returns dictionary of plant attributes as keys
            and features as values
        """
        if data is None:
            data: list[dict] = self.data
        types: str = self.existing_data_attributes("type", data)
        height: str = self.existing_data_attributes("height", data)
        sowing: str = self.existing_data_attributes("sowing", data)
        flower: str = self.existing_data_attributes("flowering", data)
        color: str = self.existing_data_attributes("color", data)
        light: str = self.existing_data_attributes("light", data)

        filters: dict[str, str] = {
            "name": "type plant name",
            "type": types,
            "height": height,
            "sowing": sowing,
            "flowering": flower,
            "color": color,
            "light": light,
        }
        return filters

    def edit_plant_info(self, plant: dict, key: str) -> dict:
        """Edits plant information by given attribute key
        Args:
            plant (dict): plant information saved as dictionary
            key (str): plant attrinbute saved as dictionary key
        Returns:
            dict: returns edited plant information saved as dictionary
        """
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
                new_add_info: str = self.file.read_text()
                updated_plant.additional_information = new_add_info
                return updated_plant.to_dict()

    def delete_plant(self, plant_id: str) -> bool:
        """Deletes plant from plant databse by plant ID
        Args:
            plant_id (str): plant ID of plant to delete
        Returns:
            bool: If deletion is succesful return True.
            If deletion in not done, returns False
        """
        plant: dict = self.search_plants(plant_id)
        if not plant:
            print(f"Plant with id {plant_id} does not exist")
            return False
        PlantDataManager.search_plant_in_gardens(plant_id)
        self.show_plants([plant], full=True)
        if PlantDataManager.ask_for_action("Do you want to delete this plant?"):
            if PlantDataManager.ask_for_action(
                "Confirm: DELETE the plant permanently?"
            ):
                self.file.remove_entry(plant)
                print(f"Plant with id {plant_id} was deleted")
                return True
        else:
            print("No changes were made")
            return False

    def search_plants(self, plant_id: str, data=None) -> dict:
        """Searches for plant in plant database by plant ID
        Args:
            plant_id (str): ID of plant to search
            data (list[dict], optional): Plant data to work with. 
            If None, takes all data from default plant data file.
            Defaults to None.
        Returns:
            dict: return found plant information as dictionary
        """
        if data is None:
            data: list[dict] = self.data
        sorted_id: list[dict] = self.sort_by_key("id")
        result: dict = PlantDataManager.binary_search(sorted_id, plant_id)
        if result:
            return result

    @staticmethod
    def search_plant_in_gardens(plant_id:str) -> None:
        """Searches if plant is a part of any Garden before deleting plant
        If plant is found in any Garden, informs about it
        Args:
            plant_id (str): plant id to search for
        """
        garden_file = DataHandler("gardens.json")
        gardens: list[dict] = garden_file.load_data()
        plant_in_gardens: str = ""
        for garden in gardens:
            if plant_id in garden["garden"]:
                plant_in_gardens += garden["name"] + ", "
        if plant_in_gardens:
            print(
                f"ATTENTION: This plant is included in gardens: {plant_in_gardens[:-2]}"
            )
            print(
                "If You will delete this plant from database it will be also deleted from Gardens"
            )

    @staticmethod
    def set_to_string(set_list: set) -> str:
        """Used to convert a set to string. 
        Args:
            set_list (set): set to convert

        Returns:
            str: returns items in set as in a single string, 
            separated by commas
        """
        if all(isinstance(x, (int, float)) for x in set_list):
            string: list = [min(set_list), max(set_list)]
            return string
        string = []
        sorted_list: list = sorted(set_list)
        for item in sorted_list:
            string.append(item)
        return string

    @staticmethod
    def editing_text() -> Literal[True]:
        """When edititng text in text editor, prompts user
        to confirm when editing is finished and text file is saved
        """
        print(
            """
            Make changes to additional information and SAVE the file. 
            Did you make any changes in the editor?    
        """
        )
        while True:
            ask: str = input("Press Enter to continue... ")
            if ask == "":
                return True

    @staticmethod
    def ask_for_action(action: str) -> bool:
        """To get a YES or NO answer for given question to user
        Args:
            action (str): Question to ask for

        Returns:
            bool: if answer is YES, returns Tue, 
            if NO, return False
        """
        while True:
            ask: str = input(f"{action} (Y/N): ").lower()
            if ask == "y":
                return True
            elif ask == "n":
                return False
            else:
                print("Wrong input: 'Y' for 'YES' and 'N' for 'NO'")

    @staticmethod
    def binary_search(data: list, plant_id: str,) -> dict | None:
        """Searching algorithm fro finding plant 
        in plant databse by pland ID
        Args:
            data (list): Sorted plant data by plant ID to work with. 
            plant_id (str): plant Id to search for
        Returns:
            dict | None: returns dictionary of plant data if found
            Returns none if plant is not found
        """
        x = int(plant_id)
        low = 0
        high: int = len(data) - 1
        while low <= high:
            mid: int = low + (high - low) // 2
            if int(data[mid]["id"]) == x:
                return data[mid]
            elif int(data[mid]["id"]) < x:
                low: int = mid + 1
            else:
                high = mid - 1
        return None
