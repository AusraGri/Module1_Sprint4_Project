import re
from helpers import Sep

class Plant:
    def __init__(self, dictionary:dict[str,str]) -> None:
        for key, value in dictionary.items():
            attr_name: str = key.replace(" ", "_").lower()
            setattr(self, attr_name, value)
            
    def to_dict(self) -> dict:
        return self.__dict__
    
    
    def print_plant(self) -> None:
        plant: dict[str,str] = {
            "Name" : self.name,
            "Scientific Name" : self.scientific_name,
            "Type" : self.type,
            "Height" : self.height,
            "Sowing" : self.sowing,
            "Flowering" : self.flowering,
            "Color" : self.color,
            "Light" : self.light,
            "Additional Information" : self.additional_information,
        }
        for key, value in plant.items():
            print(f"{key} - {value}")
        
        
    


class PlantInfo:
    s: str = "=" * 36
    c: str = "- " * 18
    def __init__(self) -> None:
        self.plant: Plant = self.create()
    
    @classmethod
    def create(cls) -> Plant:
        plant_count: int = cls.get_plant_count()
        plant_id: str = f"{plant_count + 1:03d}"
        cls.save_plant_count(plant_count + 1)
        name: str = PlantInfo.get_common_name()
        scient_name: str = PlantInfo.get_scientific_name()
        plant_type: str = PlantInfo.get_plant_type()
        height: int = PlantInfo.get_plant_height()
        sowing_time: str = PlantInfo.get_sowing_time()
        flowering_time: str = PlantInfo.get_flowering_time()
        plant_color: str = PlantInfo.get_color()
        light: str = PlantInfo.get_lighting()
        add_info: str = PlantInfo.get_additional_info()
        plant_info: dict = {
            "Id": plant_id,
            "Name" : name,
            "Scientific Name" : scient_name,
            "Type" : plant_type,
            "Height" : height,
            "Sowing" : sowing_time,
            "Flowering" : flowering_time,
            "Color" : plant_color,
            "Light" : light,
            "Additional Information" : add_info,
        }
        return Plant(plant_info)

    @staticmethod
    def get_common_name() -> str:
        print(PlantInfo.s)
        print("Please enter your plants common name")
        print(PlantInfo.c)
        while True:
            c_name: str = input("Plant common name: ")
            if len(c_name) > 1 and re.match(r"^(\w+ ?)+$", c_name):
                return c_name.strip()

    @staticmethod
    def get_scientific_name() -> str:
        print(PlantInfo.s)
        print(
            "Please enter your plants scientific (latin) name \n"
            "If you don't know scientific name, just press 'Enter'"
        )
        print(PlantInfo.c)
        while True:
            s_name: str = input("Plant scientific name: ")
            if s_name and re.match(r"^(\w+ ?)+$", s_name):
                return s_name.strip()
            else:
                return None

    @staticmethod
    def get_plant_type() -> str:
        print(PlantInfo.s)
        print("Choose the plant type")
        plant_types: dict[str, int] = {
            "Annual": 1,
            "Biennial": 2,
            "Perennial": 3,
            "Shrub": 4,
            "Tree": 5,
            "Climber": 6,
            "Bulb": 7,
            "Bedding plant": 8,
            "Alpine": 9,
            "Grass": 10,
        }
        PlantInfo.print_listed(plant_types)
        while True:
            try:
                plant_type: int = int(input("Choose plant type by number: "))
                if plant_type not in range(1, 11):
                    raise ValueError("Invalid number")
                for p_type, value in plant_types.items():
                    if plant_type == value:
                        return p_type
            except ValueError as e:
                print(e)

    @staticmethod
    def get_plant_height() -> int:
        print(PlantInfo.s)
        print(
            "Please enter your plants height in centimeters \n"
            "If you have range of height, e.g. 20 - 30, \n"
            "enter both values separated by space, e.g. '20 30' and program \n"
            "will calculate average height"
        )
        print(PlantInfo.c)
        while True:
            try:
                height: str = input("Plant height: ")
                if not re.match(r"^(\d+) ?(\d+)?$", height):
                    raise ValueError("Invalid input")
                heights: re.Match[str] | None = re.match(r"^(\d+) ?(\d+)?$", height)
                if heights.group(2):
                    first_value: int = int(heights.group(1))
                    second_value: int = int(heights.group(2))
                    if second_value > first_value:
                        average: int = second_value - first_value
                        return average
                    else:
                        raise ValueError("Invalid height values")
                return int(height)
            except ValueError as e:
                print(e)

    @staticmethod
    def get_sowing_time() -> str:
        print(PlantInfo.s)
        print(
            "Please enter month's number for the plant's sowing time, e.g. '2' \n"
            "or if more months are awailable, numbers separated by space"
        )
        print(PlantInfo.c)
        sowing_months: str = PlantInfo.get_month()
        return sowing_months

    @staticmethod
    def get_flowering_time() -> str:
        print(PlantInfo.s)
        print(
            "Please enter month's number for the plant's blooming time, e.g. '2' \n"
            "or if more months are awailable, numbers separated by space"
            "If plant is non-flowering, type 'None' and hit 'Enter'"
        )
        flowering_months: list[str] = PlantInfo.get_month()
        return flowering_months

    @staticmethod
    def get_color() -> str:
        print(PlantInfo.s)
        print(
            "choose the color that best describes the color of the bloom \n"
            "or the plant itself \n"
            "You can choose more than one color by typing numbers separated by space \n"
            "e.g. '2 4'"
        )
        plant_colors: dict[str, int] = {
            "White": 1,
            "Blue": 2,
            "Green": 3,
            "Yellow": 4,
            "Orange": 5,
            "Red": 6,
            "Purple": 7,
        }
        PlantInfo.print_listed(plant_colors)
        patt = r"^^(?!.*\b(\d)\s*\1\b)(?:[1-7]\s?){1,7}$"
        plant_colors = PlantInfo.get_answer(plant_colors, patt, "Color")
        return plant_colors

    @staticmethod
    def get_lighting() -> str:
        print(PlantInfo.s)
        print(
            "Choose fitting light conditions for the plant \n"
            "e.g. '2' or for multiple, numbers separated by space '2 3'"
        )
        light_conditions: dict[str, int] = {
            "Full Sun": 1,
            "Part Sun": 2,
            "Part Shade": 3,
            "Full Shade": 4,
        }
        PlantInfo.print_listed(light_conditions)
        patt = r"^(?!.*\b(\d)\s*\1\b)(?:[1-4]\s?){1,4}$"
        plant_lighting: str = PlantInfo.get_answer(
            light_conditions, patt, "Light condition"
        )
        return plant_lighting

    @staticmethod
    def get_additional_info() -> str:
        print(PlantInfo.s)
        print("Write here any additional informationa bout the plant if needed")
        print(PlantInfo.c)
        info: str = input("Additional information: ")
        return info

    @staticmethod
    def get_answer(dictionary: dict[str, int], pattern: str, question: str) -> str:
        patt: str = pattern
        final_list: str = ""
        numbers = []
        while True:
            try:
                ask: str = input(f"{question}: ")
                if not re.match(patt, ask):
                    raise ValueError("Invalid input")
                if spl := ask.split(" "):
                    numbers: list[int] = [int(num_str) for num_str in spl]
                    break
                else:
                    numbers.append(ask)
                    break
            except ValueError as e:
                print(e)
        for key, value in dictionary.items():
            for n in numbers:
                if n == value:
                    final_list += key + ", "
        final_list = final_list[:-2]
        return final_list

    @staticmethod
    def get_month() -> str:
        months: dict[str, int] = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12,
        }
        PlantInfo.print_listed(months)
        patt = r"^(?:(?!(\b\d+\b).*\b\1\b)(1[0-2]|[1-9])\b(?:\s|$)){1,12}$"
        month_list: str = PlantInfo.get_answer(months, patt, "Number")
        return month_list
    
    @staticmethod
    def get_plant_count() -> int:
        try:
            with open("plant_count.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0  # If the file doesn't exist, start from 0

    @staticmethod
    def save_plant_count(count: int) -> None:
        with open("plant_count.txt", "w") as file:
            file.write(str(count))
            
            
    @staticmethod      
    def print_listed(dictionary) -> None:
        print(PlantInfo.c)
        for name, value in dictionary.items():
            print(f"{value} - {name}")
        print(PlantInfo.c)
        
    # def print_plant(self, dictionary) -> None:
    #     print(PlantInfo.c)
    #     for name, value in dictionary.items():
    #         print(f"{name} - {value}")
    #     print(PlantInfo.c)
        

# p: Plant = PlantInfo.create()
# print(p.id)
# print(p.color)
# print(p.name)
# print(p.flowering)
# print(p.height)
# print(p.type)
# print(p.scientific_name)
# print(p.sowing)
# print(p.additional_information)
