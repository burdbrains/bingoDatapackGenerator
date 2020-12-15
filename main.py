# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os

# img_alt = "idk"
#
# path = "path"
#
# if not os.path.exists(path):
#     os.makedirs(path)
#
# filename = img_alt + '.jpg'
# with open(os.path.join(path, filename), 'wb') as temp_file:
#     temp_file.write(buff)


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


def generate_datapack(codes, exceptions):
    codes.sort()
    exceptions.sort()

    pretty = pretty_list(codes)

    scores = scores_list(codes)

    print(pretty)
    print(scores)


item_codes = ["anvil", "apple", "book", "bow", "chest", "crafting_table", "crossbow", "dispenser", "dried_kelp_block",
              "furnace", "hay_block", "hopper", "oak_boat", "piston", "powered_rail"]
item_craft_exc = ["apple", "sugar_cane"]

generate_datapack(item_codes, item_craft_exc)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
