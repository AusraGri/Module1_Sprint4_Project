# Home Flower Garden Helper

This program helps to create new flower gardens and manage plant data used in the garden.
User can create his plant database based on plants he prefers.
From plants in databse user is able to create flower gardens. Garden visualization is especialy very useful,
as it represent how tall plants are in garden, what main colors are and blooming / sowing time.
This helps to better visualize your flower garden and pick plants, that can create beautiful harmonized flower garden.
Also User is able to add additional comments about every garden, that helps to collect information about how every garden meets real
expectation. 
And lastly, user can export Garden data and plant data to pfd, for easy plant shoping, knowing when to sow plants 
or maybe sharing gardens with other people. 


## Usage
Program starts in main.py file. 
For code to work, make sure you have all needed libraries, 
that are listed in requirements.txt. You can use 
```pip install -r requirements.txt```
to install all needed libraries. 
User can choose the menu option on actions. 
If menu options are not given, user can interact with commands. 
When need help on commands, type -h or --help if menu is not visible.

Plant Database Comands
```
Plant Database Command Line Interface

Data Filtering:
  --type TYPE           Filter plant data by plant type
  --height VALUE        Filter plant data by plant height (cm)
  --name NAME           Filter plant data by plant name
  --sowing SOW_MONTH    Filter plant data by plant sowing time
  --flower MONTH        Filter plant data by plant flowering time
  --color COLOR         Filter plant data by plant color
  --light LIGHT         Filter plant data by plant lighting requerements

Data Sorting:
  --sort {type,name,height,color}
                        Sort plant data by type, name, height, or color

Data Editing:
  --edit PLANT_ID       Edit a plant by ID

Data Commands:
  --main                Return to main data
  --all                 Show all data
  --export              Exports current data to PDF
  --full PLANT_ID       Display full information about a plant by ID
  --exit                Exit the program

Data Commands:
  --delete PLANT_ID     Delete a plant by ID

```
Plant Editing Commands:
```
Editing Command Line Interface
Data Editing:
  Commands to edit data

  --addinfo   Edit plant additional information
  --type      Edit plant type
  --height    Edit plant height (cm)
  --name      Edit plant name
  --sowing    Edit plant sowing time
  --flower    Edit plant flowering time
  --color     Edit plant color
  --light     Edit plant lighting requerements
  --exit      Save changes and exit / exit editing panel
  --abort     Abort all changes
```
All Garden Commands:
```Garden Menu Interface

All Gardens Commands:
  Commands

  --open GARDEN_ID  Open Garden
  --search NAME     Search by Garden name
  --sort ATTRIBUTE  Sort Gardens by <name> or creation <date>
  --exit            Exit to Main Menu
```
Opended Garden Menu Commands:
```Garden Menu Interface

Garden Editing:
  Commands to edit garden

  --edit INFO        Edit Gardens <name> or <info> ('gardens description') information
  --remove PLANT_ID  Remove plant from Garden
  --visual           Show Visual table
  --delete           Delete current garden
  --add              Add plants to current garden
  --back             Back to All Gardens Menu
  --export           Export garden to PDF file
```

## Additional Information
For text editing is used ```webbrowser.open()```
It should work in all operating systems, but if you have any errors, let me know.