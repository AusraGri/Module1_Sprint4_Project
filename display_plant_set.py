
class VisualGarden:
    def __init__(self, list_of_plants):
        self.table = list_of_plants


    def months
    def add_person(self, name, months):
        if name not in self.table:
            self.table[name] = {month: "" for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
        for month in months.split(","):
            month = month.strip()  # Remove leading/trailing whitespaces
            if month in self.table[name]:
                self.table[name][month] = "❀"

    def display_table(self):
        # Print header
        print("{:<15}".format("Name"), end="")
        for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]:
            print("{:<10}".format(month), end="")
        print()

        # Print table data
        for name, months in self.table.items():
            print("{:<15}".format(name), end="")
            for month, mark in months.items():
                print("{:<10}".format(mark), end="")
            print()
            
    def display_garden(garden):
    pass



 plant_info: dict = {
            "Id": plant_id,
            "Name" : name,
            "Scientific Name" : scient_name,
            "Type" : plant_type,
            "Height" : height,
            "Sowing" : sowing_time,
            "Flowering" : flowering_time,
            "Color" : plant_color,
            "Additional Information" : add_info,
        }