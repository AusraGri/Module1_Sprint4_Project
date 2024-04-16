import argparse
from ast import arg
import re

def data_commands(user_input:str, filt_values: dict, garden=False) -> str|list[str]:
    """Converst user input to a command line commands
    Args:
        user_input (str): user input
        filt_values (dict): posible filtering values from plant database
        garden (bool, optional): If plant database is used for Garden database, set garden to True. Defaults to False.
    Returns:
        str|list[str]: returns commands to process and to be excecuted
    """
    command_line: list[str] = user_input.strip().lower().split()
    types:list[str] = filt_values["type"]
    sowing:list[str] = filt_values["sowing"]
    flowering:list[str] = filt_values["flowering"]
    colors:list[str] = filt_values["color"]
    lighting:list[str] = filt_values["light"]
    parser = argparse.ArgumentParser(description="Plant Database Command Line Interface")
    filt: argparse._ArgumentGroup = parser.add_argument_group("Data Filtering")
    
    # Options for Filtering
    # filt.add_argument("--filter", action="store_true", help="Enable filtering")
    filt.add_argument("--type",metavar=("TYPE"), choices=types,help="Filter plant data by plant type")
    filt.add_argument("--height",metavar=("VALUE"), help="Filter plant data by plant height (cm)",type=int,)
    filt.add_argument("--name", metavar=("NAME"), help="Filter plant data by plant name", type=str)
    filt.add_argument("--sowing",metavar=("SOW_MONTH"), choices=sowing, help="Filter plant data by plant sowing time")
    filt.add_argument("--flower",metavar=("MONTH"), choices=flowering, help="Filter plant data by plant flowering time")
    filt.add_argument("--color",metavar=("COLOR"), choices=colors, help="Filter plant data by plant color")
    filt.add_argument("--light",metavar=("LIGHT"), choices=lighting, help="Filter plant data by plant lighting requerements")
    

    # Options for sorting
    sort: argparse._ArgumentGroup = parser.add_argument_group("Data Sorting")
    sort.add_argument("--sort", choices=["type", "name", "height", "color"], help="Sort plant data by type, name, height, or color")

    if garden is False: # Options for editing
        edit: argparse._ArgumentGroup = parser.add_argument_group("Data Editing")
        edit.add_argument("--edit", nargs=1, metavar=("PLANT_ID"), help="Edit a plant by ID", type=validate_id)

    # Options for other commands
    other: argparse._ArgumentGroup = parser.add_argument_group("Data Commands")
    other.add_argument("--main", action="store_true", help="Return to main data")
    other.add_argument("--all", action="store_true", help="Show all data")
    other.add_argument("--export", action="store_true", help="Exports current data to PDF")
    other.add_argument("--full", metavar="PLANT_ID", help="Display full information about a plant by ID", type=validate_id)
    other.add_argument("--exit", action="store_true", help="Exit the program")
    
    if garden is False: #Option for delete
        delete: argparse._ArgumentGroup = parser.add_argument_group("Data Commands")
        delete.add_argument("--delete", metavar="PLANT_ID", help="Delete a plant by ID", type=validate_id)
        
    if garden is True: #Options for adding to garden
        adding: argparse._ArgumentGroup = parser.add_argument_group("Adding to Garden")
        adding.add_argument("--add", metavar="PLANT_ID", help="Add plant to garden by ID", type=validate_id)

    try:
        args: argparse.Namespace = parser.parse_args(command_line)
    except (SystemExit, Exception):
        return 1

    if args.type:
        return ["filter", "type", args.type]
    elif args.height:
        return ["filter", "height", args.height]
    elif args.name:
        return ["filter", "name", args.name]
    elif args.sowing:
        return ["filter", "sowing", args.sowing]
    elif args.flower:
        return ["filter", "flowering", args.flower]
    elif args.color:
        return ["filter", "color", args.color]
    elif args.light:
        return ["filter", "light", args.light]
    elif args.sort:
        return ["sort", args.sort]
    elif args.main:
        return ["mdata"]
    elif args.all:
        return ["adata"]
    elif args.full:
        return ["full", str(args.full)]
    elif args.exit:
        return ["exit"]
    elif args.export:
        return ["export"]

    if garden is False:
        if args.edit:
            return ["edit", str(args.edit[0])]
        elif args.delete:
            return ["delete", str(args.delete[0])]
  
    if garden is True:  
        if args.add:
            return ["add", str(args.add)]

def editing_commands(user_input: str) -> str|list[str]:
    """Separate Command panel for editing plant data
    Args:
        user_input (str): user input as string
    Returns:
        str|list[str]: returns commands to process and to be excecuted
    """
    command_line:list[str] = user_input.strip().lower().split()

    parser = argparse.ArgumentParser(description="Editing Command Line Interface")
    edit: argparse._ArgumentGroup = parser.add_argument_group("Data Editing", "Commands to edit data")

    # Options for editing
    edit.add_argument( "--addinfo", action="store_true", help="Edit plant additional information")
    edit.add_argument("--type", action="store_true", help="Edit plant type")
    edit.add_argument("--height", action="store_true", help="Edit plant height (cm)")
    edit.add_argument("--name", action="store_true", help="Edit plant name")
    edit.add_argument("--sowing", action="store_true", help="Edit plant sowing time")
    edit.add_argument("--flower", action="store_true", help="Edit plant flowering time")
    edit.add_argument("--color", action="store_true", help="Edit plant color")
    edit.add_argument("--light", action="store_true", help="Edit plant lighting requerements")
    edit.add_argument("--exit", action="store_true", help="Save changes and exit / exit editing panel")
    edit.add_argument("--abort", action="store_true", help="Abort all changes")

    try:
        args: argparse.Namespace = parser.parse_args(command_line)
    except (SystemExit, Exception):
        print("Try '--help' for more information.")
        return 1

    if args.addinfo:
        return "additional information"
    elif args.type:
        return "type"
    elif args.name:
        return "name"
    elif args.height:
        return "height"
    elif args.sowing:
        return "sowing"
    elif args.flower:
        return "flowering"
    elif args.color:
        return "color"
    elif args.light:
        return "light"
    elif args.exit:
        return "exit"
    elif args.abort:
        return "abort"

def all_garden_commands(commands: str, open_garden=False) -> str|list[str]:
    """Command processor for Garden Database. Takes user input and returns correct commands.
    Args:
        commands (str): user input as string
        open_garden (bool, optional): Commands for opened Garden. Defaults to False.
    Returns:
        str|list[str]: returns commands to process and to be excecuted
    """
    command_line: list = commands.strip().lower().split()
    parser = argparse.ArgumentParser(description="Garden Menu Interface")
    
    if open_garden is False:
        all_gardens: argparse._ArgumentGroup = parser.add_argument_group("All Gardens Commands", "Commands")
        all_gardens.add_argument( "--open", metavar="GARDEN_ID", help="Open Garden")
        all_gardens.add_argument( "--search", metavar="NAME", help="Search by Garden name")
        all_gardens.add_argument( "--sort", metavar="ATTRIBUTE", choices= ["name", "date"], help="Sort Gardens by <name> or creation <date>")
        all_gardens.add_argument( "--exit", action="store_true", help="Exit to Main Menu")
    
    if open_garden is True:
        opened: argparse._ArgumentGroup = parser.add_argument_group("Garden Editing", "Commands to edit garden")
        opened.add_argument( "--edit", metavar="INFO", choices=["name", "info"], help="Edit Gardens <name> or <info> ('gardens description') information")
        opened.add_argument( "--remove", metavar="PLANT_ID", help="Remove plant from Garden", type=validate_id)
        opened.add_argument("--visual", action="store_true", help="Show Visual table")
        opened.add_argument("--delete", action="store_true", help="Delete current garden")
        opened.add_argument("--add", action="store_true", help="Add plants to current garden")
        opened.add_argument("--back", action="store_true", help="Back to All Gardens Menu")
        opened.add_argument("--export", action="store_true", help="Export garden to PDF file")
    
    try:
        args: argparse.Namespace = parser.parse_args(command_line)
    except (SystemExit, Exception):
        return 1
    
    if open_garden is False:
        if args.open:
            return ["open", args.open]
        elif args.sort:
            return ["sort", args.sort]
        elif args.search:
            return ["search", args.search]
        elif args.exit:
            return ["exit"]
    elif open_garden is True:
        if args.edit:
            return ["edit", args.edit]
        elif args.remove:
            return ["remove", args.remove]
        elif args.visual:
            return ["visual"]
        elif args.delete:
            return ["delete"]
        elif args.add:
            return ["add"]
        elif args.back:
            return ["back"]
        elif args.export:
            return ["export"]

def validate_id(arg_value, pat=re.compile(r"(\d{5})$"))-> int:
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError(
            "Invalid value. Expected a 5-character int string."
        )
    return arg_value