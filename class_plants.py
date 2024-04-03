
import re

class Plant:
    def __init__(self, comm_name:str, scient_name:str, plant_type:str, height:int, sowing:list[str]) -> None:
        self.common_name = comm_name
        self.scientific_name = scient_name
        self.plant_type = plant_type
        self.height = height
        self.sowing_time = sowing


class GetPlantInfo:
    def __init__(self) -> None:
        self.common_name: str = self.get_common_name()
        self.scientific_name: str = self.get_scientific_name()
        self.type: str = self.get_plant_type()
        self.height: int = self.get_plant_height()
        self.sowing_time: list[str] = self.get_sowing_time()
        self.flowering_time: list[str] = self.get_flowering_time()
        self.plant_color: list[str] = self.get_color()
    
    def get_common_name(self) -> str:
        print("Please enter your plants common name")
        while True:
            c_name: str = input("Plant common name: ")
            if len(c_name) > 1 and re.match(r"^(\w+ ?)+$", c_name):
                return c_name.strip()
            
    def get_scientific_name(self) -> str:
        print(
            "Please enter your plants scientific (latin) name \n"
            "If don't know scientific name, just press 'Enter'"
            )
        while True:
            s_name: str = input("Plant scientific name: ")
            if s_name and re.match(r"^(\w+ ?)+$", s_name):
                return s_name.strip()
            else:
                return None
            
    def get_plant_type(self) -> str:
        plant_types: dict[str, int] = {
            "Annual" : 1,
            "Biennial" : 2,
            "Perennial" : 3,
            "Shrub" : 4,
            "Tree" : 5,
            "Climber" : 6,
            "Bulb" : 7,
            "Bedding plant" : 8,
            "Alpine": 9,
            "Grass" : 10,
        }
        print("Choose the plant type")
        for p_type, value in plant_types.items():
            print(f"{value} - {p_type}")
        while True:
            try:
                plant_type: int = int(input("Choose plant type by number: "))
                if plant_type not in range(1,11):
                    raise ValueError("Invalid number")
                for p_type, value in plant_types.items():
                    if plant_type == value:
                        return p_type
            except ValueError:
                pass
    
    def get_plant_height(self) -> int:
        print(
            "Please enter your plants height in centimeters \n"
            "If you have range of height, e.g. 20 - 30, \n"
            "enter both values separated by space, e.g. '20 30' and program \n"
            "will calculate average height"
            )
        while True:
            try:
                height: str = input("Plant height: ")
                if not re.match(r"^(\d+) ?(\d+)?$", height):
                    raise ValueError("Invalid input")
                heights = re.match(r"^(\d+) ?(\d+)?$", height)
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
    
    def get_sowing_time(self) -> list[str]:
        print(
            "Please enter month's number for the plant's sowing time, e.g. '2' \n"
            "or if more months are awailable, numbers separated by space"
            )
        sowing_months: list[str] = self.get_month()
        return sowing_months
    
    def get_flowering_time(self) -> list[str]:
        print(
            "Please enter month's number for the plant's blooming time, e.g. '2' \n"
            "or if more months are awailable, numbers separated by space"
            "If plant is non-flowering, type 'None' and hit 'Enter'"
            )
        flowering_months: list[str] = self.get_month()
        return flowering_months    
    
    def get_color(self) -> list[str]:
        print(
            "choose the color that best describes the color of the bloom \n"
            "or the plant itself \n"
            "You can choose more than one color by typing numbers separated by space \n"
            "e.g. '2 4'"
        )
        plant_colors: dict[str, int] = {
            "White" : 1,
            "Blue" : 2, 
            "Green" : 3,
            "Yellow" : 4, 
            "Orange" : 5,
            "Red" : 6, 
            "Purple" : 7,
        }
        for clr, value in plant_colors.items():
            print(f"{value} - {clr}")
        patt = r"^(?!([1-7])\s.*\1\s)(?:[1-7]\s){1,7}$"
        plant_colors = self.get_answer(plant_colors, patt, "Color")
        return plant_colors
                  
    def get_lighting(self) -> list[str]:
        print(
            "Choose fitting light conditions for the plant \n"
            "e.g. '2' or for multiple, numbers separated by space '2 3'"
        )
        light_conditions: dict[str, int] = {
            "Full Sun" : 1,
            "Part Sun" : 2, 
            "Part Shade": 3, 
            "Full Shade": 4,
        }
        for light, value in light_conditions.items():
            print(f"{value} - {light}")
        patt = r"^(?!([1-4])\s.*\1\s)(?:[1-4]\s){1,4}$"
        plant_lighting: list[str] = self.get_answer(light_conditions, patt, "Light conditions")
        return plant_lighting

    def get_soil_type(self) -> list[str]:
        
    
    @staticmethod
    def get_answer(self, dictionary: dict[str, int], pattern: str, question: str) -> list[str]:
        patt: str = pattern
        final_list: list[str] = []
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
                    final_list.append(key)
        return final_list
        
        
    @staticmethod
    def get_month(self) -> list[str]:
        months: dict[str, int] = {
            "January" : 1,
            "February" : 2, 
            "March" :3, 
            "April" : 4, 
            "May": 5,
            "June": 6, 
            "July": 7,
            "August" : 8,
            "September" : 9,
            "October" : 10,
            "November" :11,
            "December" : 12,
        } 
        for month, value in months.items():
            print(f"{value} - {month}")
        patt = r"^(?:(?!(\b\d+\b).*\b\1\b)(1[0-2]|[1-9])\b(?:\s|$)){1,12}$"
        month_list: list[str] = self.get_answer(months, patt, "Number")
        return month_list
    
        

p = GetPlantInfo()
print(p.common_name, p.scientific_name, p.type, p.sowing_time)       
    
    
            
            
