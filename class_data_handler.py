import json
import os
import webbrowser
import time
# Sample data
# data = [
#     {"id": 1, "name": "John", "age": 30, "city": "New York"},
#     {"id": 2, "name": "Alice", "age": 25, "city": "Los Angeles"},
#     {"id": 3, "name": "Bob", "age": 35, "city": "Chicago"}
# ]

# data1 = {"id": 1, "name": "John", "age": 30, "city": "New York"}


class DataHandler:
    def __init__(self, filename:str) -> None:
        self.filename: str = filename
        self._delete_allowed: bool = False
    
    def store_data(self, data) -> None:
        file_path: str = os.path.join(os.getcwd(), self.filename)
        if os.path.exists(file_path):
            self.add_data(data)
        else:
            with open(self.filename, "w") as json_file:
                json.dump([data], json_file)
        
    def load_data(self):
        with open(self.filename, "r") as file:
            return json.load(file)
        
    def remove_entry(self, entry) -> None:
        data = self.load_data()
        for item in data:
            if entry == item:
                 data.remove(entry)
            else:
                print("Entry not found.")
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
    
        
    def add_data(self, new_data: dict) -> None:
        with open(self.filename, 'r') as file:
            data = json.load(file)
        data.append(new_data)
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
            
    def update_file(self, entry: dict):
        with open(self.filename, 'r') as file:
            data = json.load(file)
        updated_data = []  
        for item in data:
            if entry["id"]:
                if item["id"] == entry["id"]:
                    item = entry
            elif entry["garden_id"]:
                if item["garden_id"] == entry["garden_id"]:
                    item = entry
            else:
                break
            updated_data.append(item)
        with open(self.filename, 'w') as file:
            json.dump(updated_data, file, indent=4)
            
    @property
    def delete_allowed(self) -> bool:
        return self._delete_allowed

    @delete_allowed.setter
    def delete_allowed(self, value):
        self._delete_allowed = value          
                
    def delete_all(self):       
        if os.path.exists(self.filename):
            os.remove(self.filename)
        
     
    def text_editor(self, text) -> None:
         with open("edit.txt", "w") as file:
            file.write(text + "\n")
            webbrowser.open("edit.txt")
            
    def read_text(self):
        with open("edit.txt", "r") as file:
            data: str = file.read()
        return data
        
        
 
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
