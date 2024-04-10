from typing import LiteralString
from tabulate import tabulate

def dictionary_to_list(dictionary):
    new_list: list =[]
    for key, value in dictionary.items():
        if isinstance(value, list):
            value_str: LiteralString = ', '.join(value)
            new_list.append([f"{key}", f"{value_str}"])
        else:
            new_list.append([f"{key}",f"{value}"])
    return new_list



def print_combined_command_tables(filt, sort, other) -> None:
    f = dictionary_to_list(filt)
    for item in f:
        item[0] = f"f:{item[0]}:"
    s = dictionary_to_list(sort)
    m = dictionary_to_list(other)
# Format each table separately
    table1: str = tabulate(f, headers=["Filter commands", ":possible options"], tablefmt="outline")
    table3: str = tabulate(s, headers=["Sort by","command"], tablefmt="outline")
    table2: str = tabulate(m, headers=["Other Commands", "command"], tablefmt="outline")

# Split each table into lines
    lines1: list[str] = table1.split('\n')
    lines2: list[str] = table2.split('\n')
    lines3: list[str] = table3.split('\n')

    max_lines: int = max(len(lines1), len(lines2), len(lines3))

# Pad the lines of each table with empty strings to match the maximum number of lines
    lines1 += [''] * (max_lines - len(lines1))
    lines2 += [''] * (max_lines - len(lines2))
    lines3 += [''] * (max_lines - len(lines3))
# Combine the corresponding lines from both tables horizontally
    combined_lines: list[str] = [line1 + line2 + line3 for line1, line2, line3 in zip(lines1, lines2, lines3)]
# Join the combined lines back into a single string
    combined_table: str = '\n'.join(combined_lines)
    print(combined_table)