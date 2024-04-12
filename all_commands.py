import argparse
import re
from class_PlantDataManager import PlantDataManager

filters = {
    "name": "type plant name",
    "type": ["annual", "perennial"],
    "height": [15, 90],
    "sowing": ["april", "june", "may"],
    "flowering": ["august", "july", "june", "september"],
    "color": ["green", "orange", "red", "yellow"],
    "light": ["full sun", "part shade"],
}

user = "--help"


def data_commands(user_input, filt_values, garden=False):
    command_line = user_input.strip().lower().split()
    types = filt_values["type"]
    sowing = filt_values["sowing"]
    flowering = filt_values["flowering"]
    colors = filt_values["color"]
    lighting = filt_values["light"]
    parser = argparse.ArgumentParser(description="Garden Command Line Interface")
    filt = parser.add_argument_group("Data Filtering")
    # Options for Filtering

    filt.add_argument("--filter", action="store_true", help="Enable filtering")
    filt.add_argument("--type",metavar=("TYPE"), choices=types,help="Filter garden data by plant type")
    filt.add_argument("--height",metavar=("VALUE"), help="Filter garden data by plant height (cm)",type=int,)
    filt.add_argument("--name", metavar=("NAME"), help="Filter garden data by plant name", type=str)
    filt.add_argument("--sowing",metavar=("SOW_MONTH"), choices=sowing, help="Filter garden data by plant sowing time")
    filt.add_argument("--flower",metavar=("MONTH"), choices=flowering, help="Filter garden data by plant flowering time")
    filt.add_argument("--color",metavar=("COLOR"), choices=colors, help="Filter garden data by plant color")
    filt.add_argument("--light",metavar=("LIGHT"), choices=lighting, help="Filter garden data by plant lighting requerements")

    # Options for sorting
    sort = parser.add_argument_group("Data Sorting")
    sort.add_argument("--sort", choices=["type", "name", "height", "color"], help="Sort garden data by type, name, height, or color")

    if garden is False:# Options for editing
        edit = parser.add_argument_group("Data Editing")
        edit.add_argument("--edit", nargs=1, metavar=("PLANT_ID"), help="Edit a plant by ID", type=validate_id)

    # Options for other commands
    other = parser.add_argument_group("Data Commands")
    other.add_argument("-m", "--main", action="store_true", help="Return to main data")
    other.add_argument("-a", "--all", action="store_true", help="Show all data")
    other.add_argument("--exit", action="store_true", help="Exit the program")
    other.add_argument("--full", metavar="PLANT_ID", help="Display full information about a plant by ID", type=validate_id)
    
    if garden is False:#Option for delete
        delete = parser.add_argument_group("Data Commands")
        delete.add_argument("--delete", metavar="PLANT_ID", help="Delete a plant by ID", type=validate_id)
        
    if garden is True: #Options for adding to garden
        add = parser.add_argument_group("Adding to Garden")
        add.add_argument("--add", metavar="PLANT_ID", help="Add plant to garden by ID", type=validate_id)
        

    try:
        args: argparse.Namespace = parser.parse_args(command_line)
    except (SystemExit, Exception):
        print("Try '--help' for more information.")
        return 1

        # Check which option was provided and return the corresponding command
    if args.filter:
        if args.type:
            return ["filter", "type", args.type[0]]
        elif args.height:
            return ["filter", "height", args.height[0]]
        elif args.name:
            return ["filter", "name", args.name[0]]
        elif args.sowing:
            return ["filter", "sowing", args.sowing[0]]
        elif args.flower:
            return ["filter", "flowering", args.flower[0]]
        elif args.color:
            return ["filter", "color", args.color[0]]
        elif args.light:
            return ["filter", "light", args.light[0]]
    elif args.sort:
        return ["sort", args.sort[0]]
    elif args.main:
        return "mdata"
    elif args.all:
        return "adata"
    elif args.exit:
        return "exit"
    elif args.edit:
        return ["edit", str(args.edit[0])]
    elif args.delete:
        return ["delete", str(args.delete[0])]
    elif args.full:
        return ["full", str(args.full[0])]
    elif args.add:
        return ["add", str(args.add[0])]
    else:
        print("Try '--help' for more information.")
        raise ValueError("Invalid command")


def editing_commands(user_input):
    command_line = user_input.strip().lower().split()

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

    print(args)

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
        return "flower"
    elif args.color:
        return "color"
    elif args.light:
        return "light"
    elif args.exit:
        return "exit"
    elif args.abort:
        return "abort"
    else:
        print("Try '--help' for more information.")


def validate_id(arg_value, pat=re.compile(r"(\d{5})$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError(
            "Invalid value. Expected a 5-character int string."
        )
    return arg_value




result = data_commands(user, filters, garden=True)
print(result)
# result = editing_commands("--help")
# print(result)
