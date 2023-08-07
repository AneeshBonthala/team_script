# Only 79 Pokemon are obtainable before the Elite Four and at Lvl. 50
# Included are all fully evolved forms and legendaries
# Excluded are Dragonite, Mewtwo, and Mew

pkmn_list = []

with open('text/pokemon_info.txt') as pkmn:
    bst = 0
    new_pkmn_dict = {}
    for line in pkmn:
        line = line.strip()
        if line[:9] == '[SPECIES_':
            pkmn_name = line[9:-3].title()
            new_pkmn_dict['Name'] = pkmn_name
        if line[:5] == '.base':
            stat = line[-4:-1].strip('=').strip()
            bst += int(stat)
        if line[:6] == '.types':
            line = line.strip('.types = {').strip('},')
            type_list = line.split(', ')
            if type_list[0] == type_list[1]:
                type_list.remove(type_list[0])
            new_pkmn_dict['Types'] = type_list
        if line == '},':
            new_pkmn_dict['BST'] = bst
            bst = 0
            pkmn_list.append(new_pkmn_dict.copy())
            new_pkmn_dict.clear()

#print(pkmn_list)

def return_pkmn_list():
    return pkmn_list