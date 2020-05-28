import os, json
import yaml

path_to_recipies = "recipes/"

missing_values = set()
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
                    sumTot += add
        else:
            print("MISSING ITEM OF ID " + itemID)
            missing_values.add(itemID)
            return 0
        worth[itemID] = sumTot
        return sumTot

parse_worth()
parse_recipes()

print(len(worth))

for x in recipes:
    calcWorth(x)

print(len(worth))
print(len(missing_values))
print(missing_values)