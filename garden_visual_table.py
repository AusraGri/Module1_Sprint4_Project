from class_PlantDataManager import PlantDataManager
from class_plants import Plant
from tabulate import tabulate
from colorist import BgColorRGB

# garden = {"garden_id": "11105525", "name": "Testing Garden", "date": "2024-04-11", "garden": ["00044","00043"]}
def garden_visual(plants_visual:list[dict]):
    all_months = set()
    for plant in plants_visual:
        sowing_months = plant["sowing"].split(", ")
        all_months.update(sowing_months)
        flowering_months = plant["flowering"].split(", ")
        all_months.update(flowering_months)

    month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_table = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    table_header = ["Name", "Color", "Height", "cm"] + month_table
    table = []
    flow = BgColorRGB(255, 204, 209)
    sow = BgColorRGB(204, 255, 204)
    seedling =  "☑"
    blossom = "✿"
    for plant in plants_visual:
        row = [f"{plant["name"]} ({plant["variety"]})", colorize(plant["color"]), height_representation(plant["height"]), plant["height"]]
        flowering_months = set(plant["flowering"].split(", "))
        sowing_months = set(plant["sowing"].split(", "))
        for month in month_names:
            if month in flowering_months and month in sowing_months:
                row.append(f"{sow}{seedling} {sow.OFF}{flow}{blossom} {flow.OFF}")
            elif month in flowering_months:
                row.append(f"{flow}{blossom}{" "*3}{flow.OFF}")
            elif month in sowing_months:
                row.append(f"{sow}{seedling}{" "*3}{sow.OFF}")
            else:
                row.append("")
        table.append(row)

    print(tabulate(table, headers=table_header, tablefmt="grid"))

def garden_plants_for_visual(garden):
    plants = PlantDataManager()
    garden_plants = []
    for item in garden["garden"]:
        plant = plants.search_plants(item)
        if plant:
            garden_plant = Plant(plant)
            visual_info = {
                "Name": f"{garden_plant.name} ({garden_plant.variety})",
                "Sowing" : garden_plant.sowing,
                "Flowers": garden_plant.flowering,
                "Color" : garden_plant.color,
                "Height" : garden_plant.height,
            }
            garden_plants.append(visual_info)
    return garden_plants

def colorize(colors):
    colors = colors.split(", ")
    plant_color = ""
    white = BgColorRGB(255, 255, 255)
    orange = BgColorRGB(255, 165, 0)
    blue = BgColorRGB(0, 0, 255)
    red = BgColorRGB(255, 0, 0)
    yellow = BgColorRGB(255, 255, 0)
    purple = BgColorRGB(255, 0, 255)
    green = BgColorRGB(0, 153, 0)
    color_match = {
        "Orange": get_color(orange),
        "Red" : get_color(red),
        "White": get_color(white),
        "Blue" : get_color(blue),
        "Yellow" : get_color(yellow),
        "Purple" : get_color(purple),
        "Green" : get_color(green),
    }
    for key, value in color_match.items():
        for color in colors:
            if key == color:
                plant_color += value
    return plant_color

def get_color(color):
    colorized = f"{color}   {color.OFF}"
    return colorized
        

# plants = [
#     {'Name': 'Marigold (Geisha Girl)', 'Sowing': 'May, June', 'Flowers': 'July, August, September', 'Color': 'Orange', 'Height': 50},
#     {'Name': 'Zinnia (Envy)', 'Sowing': 'May, June', 'Flowers': 'June, July, August, September', 'Color': 'Green, Yellow', 'Height': 90}
# ]



def height_representation(height):
    height_ = height // 10
    column = f"{"|" * height_}"
    return column
