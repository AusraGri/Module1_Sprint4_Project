import json
import os
# Sample data
# data = [
#     {"id": 1, "name": "John", "age": 30, "city": "New York"},
#     {"id": 2, "name": "Alice", "age": 25, "city": "Los Angeles"},
#     {"id": 3, "name": "Bob", "age": 35, "city": "Chicago"}
# ]

# data1 = {"id": 1, "name": "John", "age": 30, "city": "New York"}


class DataHandler:
    def __init__(self, filename) -> None:
        self.filename = filename
    
    def store_data(self, data) -> None:
        file_path: str = os.path.join(os.getcwd(), self.filename)
        if os.path.exists(file_path):
            self.update_data(data)
        else:
            with open(self.filename, "w") as json_file:
                json.dump([data], json_file)
        
    def load_data(self):
        with open(self.filename, "r") as file:
            return json.load(file)
        
    def update_data(self, new_data: dict) -> None:
        with open(self.filename, 'r') as file:
            data = json.load(file)
        data.append(new_data)
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
 
# d = DataHandler("data.json")
# d.update_data(data1)
# file_data = d.load_data()
# print(file_data)
        


def create_indexes(dictionary):
    id_index = {}
    name_index = {}
    type_index = {}
    height_index = {}
    color_index = {}
    flowering_index = {}
    
    for item in dictionary:
        id_index.setdefault(item["id"], []).append(item)
        name_index.setdefault(item["name"], []).append(item)
        type_index.setdefault(item["type"], []).append(item)
        height_index.setdefault(item["height"], []).append(item)
        color_index.setdefault(item["color"], []).append(item)
        flowering_index.setdefault(item["flowering"], []).append(item)


# Perform search
def search_by_name(indexes, desired_name):
    if desired_name in indexes["name"]:
        print("Found:", indexes["name"][desired_name])
    else:
        print("Name not found.")
