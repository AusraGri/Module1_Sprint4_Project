import json
import os
from typing import Any
import webbrowser

"""Handles operations: saving data / updating / retrieving to/from jason file
    Opens text editor for text editing

    Returns:
        list[dict] | str: return data from json files or txt file
    """

class DataHandler:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self._delete_allowed: bool = False

    def store_data(self, data: dict) -> None:
        """Stores data to the file. If file does not exist, creates the file
        If file exists, appends data
        Args:
            data (dict): data to store
        """
        file_path: str = os.path.join(os.getcwd(), self.filename)
        if os.path.exists(file_path):
            self.add_data(data)
        else:
            with open(self.filename, "w") as json_file:
                json.dump([data], json_file)

    def load_data(self)-> Any: 
        """Reads data from json file and returns it
        Returns:
            Any: returns data from json file
        """
        with open(self.filename, "r") as file:
            return json.load(file)

    def remove_entry(self, entry: dict) -> None:
        """Removes given data from a list of dictioanries saved in json file

        Args:
            entry (dict): dictionary to remove from file
        """
        data: list[dict] = self.load_data()
        for item in data:
            if entry == item:
                data.remove(entry)
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_data(self, new_data: dict) -> None:
        """Appends data to existing json file as list of dictionaries
        Args:
            new_data (dict): new dictionary to save in json file
        """
        with open(self.filename, "r") as file:
            data = json.load(file)
        data.append(new_data)
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def update_file(self, entry: dict) -> None:
        """For updating plant database and dargen databe files
        Args:
            entry (dict): plant data as dictionary or garden data as dictionary
        """
        with open(self.filename, "r") as file:
            data: list[dict] = json.load(file)
        updated_data: list = []
        for item in data:
            if "id" in entry and item.get("id") == entry.get("id"):
                item.update(entry)
                break
            elif "garden_id" in entry and item.get("garden_id") == entry.get(
                "garden_id"
            ):
                item.update(entry)
                break
            updated_data.append(item)
        with open(self.filename, "w") as file:
            json.dump(updated_data, file, indent=4)

    @property
    def delete_allowed(self) -> bool:
        return self._delete_allowed

    @delete_allowed.setter
    def delete_allowed(self, value: bool) -> None:
        self._delete_allowed = value

    def delete_all(self) -> None:
        """To delete any file from project folder
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def text_editor(self, text: str) -> None:
        """Opens given text in text editor for editing
        Args:
            text (str): text to open in text editor
        """
        with open("edit.txt", "w") as file:
            file.write(text + "\n")
            webbrowser.open("edit.txt")

    def read_text(self) -> str:
        """Reads text from from file where text was edited
        Returns:
            str: return text from editing file
        """
        with open("edit.txt", "r") as file:
            data: str = file.read()
        return data
