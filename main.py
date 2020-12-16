import os


def generate_structure(directory, codes, exceptions):
    scores, pretty = generate_arrays(codes, exceptions)
    path = directory + r"\Bingo"
    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(path + r"\data")
        generate_packmeta(path)

        os.makedirs(path + r"\data\bingo")
        os.makedirs(path + r"\data\bingo\functions")
        generate_standards(path + r"\data\bingo\functions", scores, pretty)

        os.makedirs(path + r"\data\bingo\functions\create_board")
        generate_create_board(path + r"\data\bingo\functions\create_board", scores)

        os.makedirs(path + r"\data\bingo\functions\items")
        generate_items(path + r"\data\bingo\functions\items", codes, exceptions, scores, pretty)

        os.makedirs(path + r"\data\bingo\functions\utilities")
        generate_utilities(path + r"\data\bingo\functions\utilities", scores)

        os.makedirs(path + r"\data\minecraft")
        os.makedirs(path + r"\data\minecraft\tags")
        os.makedirs(path + r"\data\minecraft\tags\functions")
        generate_jsons(path + r"\data\minecraft\tags\functions")

    else:
        print("Bingo datapack directory already exists in: " + directory)


def generate_items(directory, codes, exceptions, scores, pretty):
    for i in range(len(scores)):
        with open(os.path.join(directory, scores[i].lower() + ".mcfunction"), 'w') as temp_file:
            if codes[i] in exceptions:
                temp_file.write('scoreboard objectives add craft' + scores[i] + ' minecraft.picked_up:minecraft.' + codes[i] + '\n')
            else:
                temp_file.write('scoreboard objectives add craft' + scores[i] + ' minecraft.crafted:minecraft.' + codes[i] + '\n')
            temp_file.write('scoreboard objectives add score' + scores[i] + ' dummy\n')
            temp_file.write('scoreboard players set @a score' + scores[i] + ' 0\n')
            temp_file.write('tellraw @a {"text":"' + pretty[i] + '"}\n')
            temp_file.write('scoreboard players add @s incrementItems 1\n')
            temp_file.write('scoreboard players set @s range' + scores[i] + ' -1\n')
            if i+1 < len(scores):
                for j in range(i+1, len(scores)):
                    temp_file.write('scoreboard players remove @s range' + scores[j] + ' 1\n')
            temp_file.write('scoreboard players remove @s range 1\n')


def generate_create_board(directory, scores):
    with open(os.path.join(directory, "create_board.mcfunction"), 'w') as temp_file:
        temp_file.write('scoreboard players set @s range ' + str(len(scores)+1) + '\n')
        item_val = 0
        for s in scores:
            temp_file.write('scoreboard players set @s range' + s + ' ' + str(item_val) + '\n')
            item_val += 1
        temp_file.write('execute as @s at @s run function bingo:create_board/pick_items\n')

    with open(os.path.join(directory, "pick_items.mcfunction"), 'w') as temp_file:
        temp_file.write('execute as @s at @s run function bingo:create_board/random\n')
        temp_file.write('execute as @a if score @s incrementItems matches 9.. run function bingo:bingo_board\n')
        temp_file.write('execute unless score @s incrementItems matches 9.. run function bingo:create_board/pick_items\n')

    with open(os.path.join(directory, "random_select.mcfunction"), 'w') as temp_file:
        for s in reversed(scores):
            temp_file.write('execute if score @s random = @s range' + s + ' run function bingo:items/' + s.lower() + '\n')

    with open(os.path.join(directory, "random.mcfunction"), 'w') as temp_file:
        temp_file.write('summon area_effect_cloud ~ ~ ~ {Tags:["random_uuid"]}\n')
        temp_file.write('execute store result score @s random run data get entity @e[type=area_effect_cloud,tag=random_uuid,limit=1] UUID[0]\n')
        temp_file.write('scoreboard players operation @s random %= @s range\n')
        temp_file.write('kill @e[type=area_effect_cloud,tag=random_uuid]\n')
        temp_file.write('function bingo:create_board/random_select\n')


def generate_standards(directory, scores, pretty):
    with open(os.path.join(directory, "bingo_board.mcfunction"), 'w') as temp_file:
        temp_file.write(r'tellraw @s {"text":"\n\n\n"}' + '"\n')
        temp_file.write('tellraw @s [{"text":"   <","color":"yellow","bold": true},{"text":"Bingo Board","color":"gold","bold":true},{"text":">","color":"yellow","bold": true}]\n')
        for i in range(len(scores)):
            temp_file.write('execute as @s at @s if score @s score' + scores[i] + ' matches 0 run tellraw @s {"text":"' + pretty[i] + '","color":"red"}\n')
            temp_file.write('execute as @s at @s if score @s score' + scores[i] + ' matches 1 run tellraw @s {"text":"' + pretty[i] + '","color":"green","strikethrough":true}\n')
        temp_file.write(r'tellraw @s {"text":"\n\n\n"}' + '"\n')

    with open(os.path.join(directory, "game_winner.mcfunction"), 'w') as temp_file:
        temp_file.write('tellraw @a [{"color":"gold","bold":true,"selector":"@s"},{"color":"yellow","text":" completed their bingo board!", "bold":false}]\n')
        temp_file.write('scoreboard players set @s winner 1\n')

    with open(os.path.join(directory, "load.mcfunction"), 'w') as temp_file:
        temp_file.write('tellraw @a ["",{"color":"gold", "text":"[BINGO]", "bold":true},{"color":"yellow", "text":" Bingo datapack by burdbrains loaded!","italic": true}]\n')
        temp_file.write('function bingo:utilities/reset\n')

    with open(os.path.join(directory, "tick.mcfunction"), 'w') as temp_file:
        temp_file.write('execute as @e[scores={gameScore=9..}] at @s unless score @s winner matches 1 run function bingo:game_winner\n')
        for s in scores:
            temp_file.write('execute as @e[scores={craft' + s + '=1..}] at @s if score @s score' + s + ' matches 0 run scoreboard players add @s gameScore 1\n')
            temp_file.write('execute as @e[scores={craft' + s + '=1..}] at @s if score @s score' + s + ' matches 0 run scoreboard players set @s score' + s + ' 1\n')


def generate_utilities(directory, scores):
    with open(os.path.join(directory, "reset.mcfunction"), 'w') as temp_file:
        temp_file.write('scoreboard objectives remove random\n')
        temp_file.write('scoreboard objectives add random dummy\n')
        temp_file.write('scoreboard objectives remove range\n')
        temp_file.write('scoreboard objectives add range dummy\n')
        temp_file.write('scoreboard objectives remove incrementItems\n')
        temp_file.write('scoreboard objectives add incrementItems dummy\n')
        temp_file.write('scoreboard objectives remove gameScore\n')
        temp_file.write('scoreboard objectives add gameScore dummy\n')
        temp_file.write('scoreboard objectives remove winner\n')
        temp_file.write('scoreboard objectives add winner dummy\n')
        for s in scores:
            temp_file.write('scoreboard objectives remove range' + s + '\n')
            temp_file.write('scoreboard objectives add range' + s + ' dummy\n')
            temp_file.write('scoreboard objectives remove craft' + s + '\n')
            temp_file.write('scoreboard objectives remove score' + s + '\n')


def generate_packmeta(directory):
    with open(os.path.join(directory, "pack.mcmeta"), 'w') as temp_file:
        temp_file.write('{\n')
        temp_file.write('   "pack":\n')
        temp_file.write('   {\n')
        temp_file.write('       "pack_format": 6,\n')
        temp_file.write('       "description": "Bingo by burdbrains."\n')
        temp_file.write('   }\n')
        temp_file.write('}')


def generate_jsons(directory):
    with open(os.path.join(directory, "load.json"), 'w') as temp_file:
        temp_file.write('{\n')
        temp_file.write('   "values":[\n')
        temp_file.write('       "bingo:load"\n')
        temp_file.write('   ]\n')
        temp_file.write('}')
    with open(os.path.join(directory, "tick.json"), 'w') as temp_file:
        temp_file.write('{\n')
        temp_file.write('   "values":[\n')
        temp_file.write('       "bingo:tick"\n')
        temp_file.write('   ]\n')
        temp_file.write('}')


def format_pretty(string):
    spaces = string.replace("_", " ")
    result = spaces.title()
    return result


def format_scores(string):
    string = format_pretty(string)
    no_space = string.replace(" ", "")
    no_space = ''.join(char for char in no_space if char not in set('aeiou'))
    if len(no_space) > 11:
        no_space = no_space[:11]
    return no_space


def pretty_list(codes):
    empty_list = []
    for c in codes:
        temp = format_pretty(c)
        empty_list.append(temp)
    return empty_list


def scores_list(codes):
    empty_list = []
    for c in codes:
        temp = format_scores(c)
        empty_list.append(temp)
    return empty_list


def generate_arrays(codes, exceptions):
    codes.sort()
    exceptions.sort()

    pretty = pretty_list(codes)

    scores = scores_list(codes)

    print(pretty)
    print(scores)

    return scores, pretty


#####################################################################################################################
#                               THIS IS WHERE THE ITEMS FOR THE BINGO BOARD GO                                      #
#####################################################################################################################
item_codes = ["sugar_cane", "anvil", "apple", "book", "bow", "chest", "crafting_table", "crossbow", "dispenser", "dried_kelp_block",
              "furnace", "hay_block", "hopper", "oak_boat", "piston", "powered_rail"]

#####################################################################################################################
#                     THIS IS WHERE ITEMS THAT WON'T BE CRAFTED AND INSTEAD PICKED UP WILL GO                       #
#####################################################################################################################
item_craft_exc = ["apple", "sugar_cane"]

dp_path = r"C:\Users\erter\Documents\Datapacks"

generate_structure(dp_path, item_codes, item_craft_exc)
