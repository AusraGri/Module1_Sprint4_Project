import json

# Sample data
data = [
    {"id": 1, "name": "John", "age": 30, "city": "New York"},
    {"id": 2, "name": "Alice", "age": 25, "city": "Los Angeles"},
    {"id": 3, "name": "Bob", "age": 35, "city": "Chicago"}
]

class DataHandler:
    def __init__(self, filename) -> None:
        self.
    
def store_data():
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

# Create indexes
def create_indexes():
    indexes = {
        "id": {item["id"]: item for item in data},
        "name": {},
        "age": {},
        "city": {}
    }

    for item in data:
        indexes["name"].setdefault(item["name"], []).append(item)
        indexes["age"].setdefault(item["age"], []).append(item)
        indexes["city"].setdefault(item["city"], []).append(item)

    return indexes

# Perform search
def search_by_name(indexes, desired_name):
    if desired_name in indexes["name"]:
        print("Found:", indexes["name"][desired_name])
    else:
        print("Name not found.")

# Main function
def main():
    store_data()
    indexes = create_indexes()

    desired_name = "John"
    print(f"Searching for '{desired_name}':")
    search_by_name(indexes, desired_name)

    # You can perform other searches here

if __name__ == "__main__":
    main()


# Load existing data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Append new dictionary to the list
new_entry = {
    "id": 4,
    "name": "Eve",
    "age": 28,
    "city": "Boston"
}
data.append(new_entry)

# Write updated data back to JSON file
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)