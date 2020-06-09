import os, json
import yaml

path_to_recipies = "recipes/"

#missing_values = set()
recipes = {}
worth = {}

def getYMLID(str):
    return ''.join(''.join(str.split("minecraft:")).split("_"))

def parse_worth():
    with open("worth.yml", "r") as stream:
        try:
            data = yaml.safe_load(stream)['worth']
            for x in data:
                worth[x] = data[x]
        except yaml.YAMLError as exc:
            print(exc)

def parse_recipes():
    for file_name in [file for file in os.listdir(path_to_recipies) if file.endswith('.json')]:
        with open(path_to_recipies + file_name) as json_file:
            data = json.load(json_file)
            if 'type' in data:
                #print(data)
                object_name = ""
                recipe = {}
                if data['type'] in ['minecraft:stonecutting','minecraft:smelting', 'minecraft:campfire_cooking', 'minecraft:smoking', 'minecraft:blasting']:
                    object_name = data['result']

                    if 'item' in data['ingredient']:
                        recipe = {data['ingredient']['item']:1}
                    elif 'tag' in data['ingredient']:
                        recipe = {data['ingredient']['tag']:1}

                    if 'count' in data['result']:
                        recipe["COUNT"] = data['result']['count']
                    else:
                        recipe["COUNT"] = 1

                    recipes[object_name] = recipe
                elif data['type'] in ['minecraft:crafting_shaped', 'minecraft:crafting_shapeless']:
                    object_name = data['result']['item']
                    recipe = {}

                    if 'count' in data['result']:
                        recipe["COUNT"] = data['result']['count']
                    else:
                        recipe["COUNT"] = 1

                    if data['type'] == 'minecraft:crafting_shapeless':
                        for x in data['ingredients']:
                            if 'item' in x:
                                recipe[x['item']] = 1
                            elif 'tag' in x:
                                recipe[x['tag']] = 1

                    elif data['type'] == 'minecraft:crafting_shaped':
                        keys = {}

                        for x in data['key']:
                            if len(list(data['key'][x])) == 1:
                                if 'item' in data['key'][x]:
                                    keys[x] = data['key'][x]['item']
                                elif 'tag' in data['key'][x]:
                                    keys[x] = data['key'][x]['tag']
                            else:
                                #DEAL WITH THIS
                                #take only first result?
                                #check if lower first
                                #rip
                                # 'key': {'#': [{'item': 'minecraft:purpur_block'}, {'item': 'minecraft:purpur_pillar'}]}
                                #set somthing to return for keys[x]
                                #[{'item': 'minecraft:purpur_block'}, {'item': 'minecraft:purpur_pillar'}]
                                minItemId = ""
                                minItemVal = 1e9
                                for y in list(data['key'][x]):
                                    validId = getYMLID(y['item'])
                                    if validId in worth:
                                        minItemVal = min(worth[validId], minItemVal)
                                        if minItemVal == worth[validId]:
                                            minItemId = y['item']
                                    else:
                                        continue
                                keys[x] = minItemId

                            recipe[keys[x]] = 0

                        for x in data['pattern']:
                            for y in keys:
                                recipe[keys[y]] += x.count(y)

                    if not recipe:
                        print("EMPTY RECIPE ON " + data)
                    recipes[object_name] = recipe
                if(to_recalc):
                    for x in recipe:
                        if x in affectedRecipes:
                            affectedRecipes.add(object_name)
                            break


def calcWorth(item):
    itemID = getYMLID(item)
    if itemID in worth:
        return worth[itemID]
    else:
        sumTot = 0
        if item in recipes:
            #print(item)
            recipe = recipes[item]
            for y in recipe:
                if not y == 'COUNT':
                    add = calcWorth(y)
                    #print(str(y) + " " + str(add))
                    sumTot += add*recipe[y]
            sumTot = round(sumTot/recipe['COUNT'],2)
        else:
            print("MISSING ITEM OF ID " + itemID)
            worth[itemID] = float(input())
            return worth[itemID]
        worth[itemID] = sumTot
        return worth[itemID]

def write_worth():
    with open("updated_worth.yml", "w") as outstream:
        try:
            outdata = {'worth':worth}
            yaml.safe_dump(outdata, outstream)
        except yaml.YAMLError as exc:
            print(exc)

def recalcItem(item):
    print(item)
    itemID = getYMLID(item)
    if item not in affectedRecipes:#if nnot affected
        return worth[itemID]
    else:#if affected
        if item in itemsToRecalc:  # if item was directly channged\
            return itemsToRecalc[item]
        elif item in recipes:#if item has recipe
            sumTot = 0
            recipe = recipes[item]
            for y in recipe:
                print(str(y) + " : " + str(recipe))
                if not y == 'COUNT':
                    add = recalcItem(y)
                    print(add)
                    sumTot+=add*recipe[y]
            sumTot = round(sumTot/recipe['COUNT'],2)
            return sumTot
        else:#if item doesn't hvae recipe
             return worth[itemID]

to_recalc = False
itemsToRecalc = {}
affectedRecipes = set()
recalcd = set()

while True:
    user_in = input("Would you like to recalculate values of items: ")
    if(user_in.lower() in ['yes', 'y']):
        to_recalc=True
        break
    elif(user_in.lower() in ['no', 'n']):
        to_recalc=False
        break
    else:
        print("please enter a valid answer")


parse_worth()

while to_recalc:
    user_in = input("Please enter the id of the item you would like to change, type 'stop' to stop: ")
    if user_in == 'stop':
        break
    else:
        if "minecraft:" in user_in:
            try:
                itemsToRecalc[user_in] = int(input("enter the value to be changed to: "))
                affectedRecipes.add(user_in)
            except:
                print("that is not a valid id or an improper value")
                continue
        else:
            try:
                user_in = "minecraft:" + user_in
                itemsToRecalc[user_in] = int(input("enter the value to be changed to: "))
                affectedRecipes.add(user_in)
            except:
                print("that is not a valid id or an improper value")
                continue

parse_recipes()

if not to_recalc:
    for x in recipes:
        calcWorth(x)
else:
    print("amount of recipes to be changed: " + str(len(affectedRecipes)))
    for x in affectedRecipes:
        worth[getYMLID(x)] = recalcItem(x)
        print("value of item '" + x + "' has been corrected to: " + str(worth[getYMLID(x)]))


write_worth()