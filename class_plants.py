import re

"""Plant class to manage individual plant data

    Raises:
        ValueError: If given parameter to class is not valid

    Returns:
        dict: dictionary of collected plant data
    """
class Plant:
     VALID_KEYS: set[str] = {
        "id", "name", "variety", "scientific name", "type", 
        "height", "sowing", "flowering", "color", "light", 
        "additional information", "scientific_name", "additional_information"
    }

     def __init__(self, dictionary: dict[str, str]) -> None:
        """Takes plant information created with PlantInfo
        and converts to Plant object.
        Args:
            dictionary (dict[str, str]): Dictionary where plant data is collected.
        """
        self.validate_dictionary(dictionary)
        for key, value in dictionary.items():
            attr_name: str = self.format_attribute_name(key)
            setattr(self, attr_name, value)

     def validate_dictionary(self, dictionary: dict[str, str]) -> None:
        """Validates if the dictionary keys match the expected keys for plant information."""
        if not set(map(str.lower, dictionary.keys())).issubset(map(str.lower, self.VALID_KEYS)):
            invalid_keys: set[str] = set(dictionary.keys()) - self.VALID_KEYS
            raise ValueError(f"Invalid keys found: {', '.join(invalid_keys)}")

     @staticmethod
     def format_attribute_name(key: str) -> str:
        """Formats the dictionary key to a valid attribute name."""
        return key.replace(" ", "_").lower()

     def to_dict(self) -> dict:
        """Converts Plant data to dictioanry
        Returns:
            dict: plant data as dictioanry
        """
        return self.__dict__

     def print_plant(self) -> None:
        """Prints Plant object 
        """
        plant: dict[str, str] = {
            "Name": self.name,
            "Variety": self.variety,
            "Scientific Name": self.scientific_name,
            "Type": self.type,
            "Height": self.height,
            "Sowing": self.sowing,
            "Flowering": self.flowering,
            "Color": self.color,
            "Light": self.light,
            "Additional Information": self.additional_information,
        }
        for key, value in plant.items():
            print(f"{key} - {value}")

"""Initiates creation of Plant by collecting all necessary data from user
    and stored data as a collenction of plant attributes in dictionary

    Raises:
        ValueError: if user chooses wrong attribute for plant
        FileNotFoundError: if plant counting file for plant ID is missing
    Returns:
        object: Plant object
    """
class PlantInfo:
    """Some spacers"""
    s: str = "=" * 36
    c: str = "- " * 18

    def __init__(self) -> None:
        """When class is initialized it starts collecting plant data"""
        self.plant: Plant = self.create()

    @classmethod
    def create(cls) -> Plant:
        """Collects all needed data for plant as dictioanry
        and creates Plant object
        Returns:
            Plant: object of plant data
        """
        plant_count: int = PlantInfo.get_plant_count()
        plant_id: str = f"{plant_count + 1:05d}"
        name: str = PlantInfo.get_common_name()
        variety: str = PlantInfo.get_variety_name()
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
            "Name": name,
            "Variety": variety,
            "Scientific Name": scient_name,
            "Type": plant_type,
            "Height": height,
            "Sowing": sowing_time,
            "Flowering": flowering_time,
            "Color": plant_color,
            "Light": light,
            "Additional Information": add_info,
        }
        return Plant(plant_info)

    @staticmethod
    def get_common_name() -> str:
        """Gets name for the plant from user
        Returns:
            str: name for plant
        """
        print(PlantInfo.s)
        print("Please enter your plants common name")
        print(PlantInfo.c)
        while True:
            c_name: str = input("Plant common name: ")
            if len(c_name) > 1 and re.match(r"^(\w+ ?)+$", c_name):
                return c_name.strip()

    @staticmethod
    def get_variety_name() -> str:
        """_Gets plant variety name from user
        Returns:
            str: plant variety name
        """
        print(PlantInfo.s)
        print("Please enter your variety name")
        print(PlantInfo.c)
        while True:
            c_name: str = input("Variety name: ")
            if len(c_name) > 1 and re.match(r"^(\w+ ?)+$", c_name):
                return c_name.strip()

    @staticmethod
    def get_scientific_name() -> str:
        """Gets scientific name for the plant from user
        Returns:
            str: scientific name
        """
        print(PlantInfo.s)
        print(
            "Please enter your plants scientific (latin) name \n"
            "If you don't know scientific name, just press 'Enter'"
        )
        print(PlantInfo.c)
        while True:
            s_name: str = input("Plant scientific name: ")
            if s_name and re.match(r"^(\w+\.?-? ?)+$", s_name):
                return s_name.strip()
            if not s_name:
                return s_name

    @staticmethod
    def get_plant_type() -> str:
        """Asks for user to choose plant type
        Raises:
            ValueError: if user choice is not from given choices
        Returns:
            str: plant type
        """
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
        """Asks user for plant height
        user can give two numbers and average will be stored
        Raises:
            ValueError: if no number is given or too many numbers
        Returns:
            int: plant height
        """
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
                    average: int = (second_value + first_value) // 2
                    return average
                return int(height)
            except ValueError as e:
                print(e)

    @staticmethod
    def get_sowing_time() -> str:
        """Prompt user to specify when it is time to sow the plant
        Returns:
            str: months to sow
        """
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
        """Prompt user to specify when plant is blooming
        If plant is not a flower, specify months when plant is in active stage
        Returns:
            str: months when flowering
        """
        print(PlantInfo.s)
        print(
            "Please enter month's number for the plant's blooming time, e.g. '2' \n"
            "or if more months are awailable, numbers separated by space"
            "If plant is non-flowering, type months when it is in active phase'"
        )
        flowering_months: list[str] = PlantInfo.get_month()
        return flowering_months

    @staticmethod
    def get_color() -> str:
        """Prompt user for plant color
        Returns:
            str: plant color
        """
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
        """Choose plant growing light conditions
        Returns:
            str: plant growing light conditions
        """
        print(PlantInfo.s)
        print(
            "Choose fitting growing light conditions for the plant \n"
            "e.g. '2' or for multiple, numbers separated by space '2 3'"
        )
        light_conditions: dict[str, int] = {
            "Full-Sun": 1,
            "Part-Sun": 2,
            "Part-Shade": 3,
            "Full-Shade": 4,
        }
        PlantInfo.print_listed(light_conditions)
        patt = r"^(?!.*\b(\d)\s*\1\b)(?:[1-4]\s?){1,4}$"
        plant_lighting: str = PlantInfo.get_answer(
            light_conditions, patt, "Light condition"
        )
        return plant_lighting

    @staticmethod
    def get_additional_info() -> str:
        """Provide additional information about the plant
        if needed
        Returns:
            str: plant description
        """
        print(PlantInfo.s)
        print("Write here any additional informationa bout the plant if needed")
        print(PlantInfo.c)
        info: str = input("Additional information: ")
        return info

    @staticmethod
    def get_answer(dictionary: dict[str, int], pattern: str, question: str) -> str:
        """Asks user for the given question as text and 
        gets correct answer from user for given options in dictionary
        and matches user answer to a given regular expresion pattern
        Args:
            dictionary (dict[str, int]): options given as dictionary
            pattern (str): regular expresion pattern to match user input
            question (str): question to ask for user
        Raises:
            ValueError: if user input is not from given dictionary
        Returns:
            str: returns chosen options values
        """
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
        """Dictionary of 12 months as keys and values
        Returns:
            str: user chosen month names
        """
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
        """Gets number for the plant ID
        Returns:
            int: number for ID
        """
        try:
            with open("plant_count.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0 

    @staticmethod
    def save_plant_count(count: int) -> None:
        """Saves updated number back to the plant counting file
        Args:
            count (int): next number to use when plant will be created
        """
        with open("plant_count.txt", "w") as file:
            file.write(str(count))
            
    @staticmethod
    def print_listed(dictionary: dict) -> None:
        """Print collected data as dictionary before confirming it
        Args:
            dictionary (dict): plant information
        """
        print(PlantInfo.c)
        for name, value in dictionary.items():
            print(f"{value} - {name}")
        print(PlantInfo.c)
