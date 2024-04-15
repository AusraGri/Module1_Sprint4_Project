from typing import LiteralString
from class_PlantDataManager import PlantDataManager
from class_Plants import Plant
from tabulate import tabulate
from colorist import BgColorRGB

"""Visualisation of garden information about plants height, blooming, sowing time, main colors in garden
    """
def garden_visual(plants_visual:list[dict]) -> None:
    """Prints out table of garden plants visualizig plant color, 
    flowering time, sowing time, height
    Args:
        plants_visual (list[dict]): plants to add in table
    """
    all_months = set()
    for plant in plants_visual:
        sowing_months:list[str] = plant["sowing"].split(", ")
        all_months.update(sowing_months)
        flowering_months:list[str] = plant["flowering"].split(", ")
        all_months.update(flowering_months)

    month_names: list[str] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_table: list[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    table_header: list[str] = ["Name", "Color", "Height", "cm"] + month_table
    table:list = []
    flow = BgColorRGB(255, 204, 209)
    sow = BgColorRGB(204, 255, 204)
    seedling =  "☑"
    blossom = "✿"
    for plant in plants_visual:
        row:list = [f"{plant["name"]} ({plant["variety"]})", colorize(plant["color"]), height_representation(plant["height"]), plant["height"]]
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
   

def garden_plants_for_visual(garden: dict) -> list[dict]:
    """Retrieves plants data that are in the garden as needed 
    for the visual table to be created
    Args:
        garden (dict): garden information
    Returns:
        list[dict]: plants in the garden with properly formatted information
    """
    plants = PlantDataManager()
    garden_plants:list[dict] = []
    for item in garden["garden"]:
        plant:dict = plants.search_plants(item)
        if plant:
            garden_plant = Plant(plant)
            visual_info:dict[str, str] = {
                "Name": f"{garden_plant.name} ({garden_plant.variety})",
                "Sowing" : garden_plant.sowing,
                "Flowers": garden_plant.flowering,
                "Color" : garden_plant.color,
                "Height" : garden_plant.height,
            }
            garden_plants.append(visual_info)
    return garden_plants

def colorize(colors:str) -> str:
    """Plant color data is converted to 
    a color box
    Args:
        colors (str): colors from plant data
    Returns:
        str: colored background (box)
    """
    colors:list[str] = colors.split(", ")
    plant_color:str = ""
    white = BgColorRGB(255, 255, 255)
    orange = BgColorRGB(255, 165, 0)
    blue = BgColorRGB(0, 0, 255)
    red = BgColorRGB(255, 0, 0)
    yellow = BgColorRGB(255, 255, 0)
    purple = BgColorRGB(255, 0, 255)
    green = BgColorRGB(0, 153, 0)
    color_match: dict[str, str] = {
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

def get_color(color) -> str:
    """Applies given color to background
    Args:
        color (BgColorRGB): color from colorist
    Returns:
        str: formatted color "box"
    """
    colorized: str = f"{color}   {color.OFF}"
    return colorized

def height_representation(height:int) -> LiteralString:
    """Converts plant hight to visual bars
    divides height by 10 and multiplies |
    Args:
        height (int): height of plant
    Returns:
        LiteralString: bars of height
    """
    height_: int = height // 10
    column: LiteralString = f"{"|" * height_}"
    return column
