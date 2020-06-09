# Minecraft_Item_Worth_Calculator

## Usage
To use this script, make sure you have the recipies folder from your decompiled minecraft jar of whatever version you are playing on as well as your outdated/to be changed worth.yml in the folder with evalecon.py.

### Prerequisites 

To run this program you need python 3 which can be found at https://www.python.org/downloads/

as well as this you will need the PyYaml which can be installed via the following CL commands
```
pip install PyYaml
```

then you may run the program through the command line or any other method you like by navigating to the scripts directory and typing
```
python evalecon.py
```

#### Updating Your Economy
to use this program to up update your economy, when prompted on whether you would like to recalculate values of items enter 'no' or 'n'. The program will then proceed to add values/worth to any items it can then, if it cant find the values, it will prompt you to enter some values.

#### Changing existing item's values
when prompted to recalculate enter 'yes' or 'y'. You will now be asked to enter the ids of the items you would like to update, and then their value, you can enter the id either with or without 'minecraft:' in front. Remember that this program is case sensitive so everything should be lowercased when dealing with Id's. after you entering your new values for all items, type 'stop' and the program will tell you the updated values of all the items.

### Using the updated values
After the program has successfully ran, the updated values can be found in the 'updated_worth.yml' file, rename this to worth.yml and replace the one in your plugins folder and you should be good to go
