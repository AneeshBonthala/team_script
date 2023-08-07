from random import choice, choices, randint
from pkmn_parser import return_pkmn_list
import copy
import numpy as np

pkmn_list = copy.copy(return_pkmn_list())
length = len(pkmn_list)
#print(length)
median_bst = np.median([pkmn['BST'] for pkmn in pkmn_list])
#print(median_bst)

type_factors = {}
def config_tfs():
    global type_factors
    for pkmn in pkmn_list:
        for type in pkmn['Types']:
            if type not in type_factors:
                type_factors[type] = 1

def increment_type(type):
    global type_factors
    type_factors[type] += 1

def get_type_factor(pkmn):
    tf = type_factors[pkmn['Types'][0]] ** (-1)
    if len(pkmn['Types']) == 2:
        tf = tf * type_factors[pkmn['Types'][1]] ** (-1)
    return tf

def bst_weight(team, slot, pkmn):
    last_bst = team[slot - 2]['BST']
    if last_bst < median_bst:
        if pkmn['BST'] < median_bst:
            return 0.5
        else:
            return 1
    else:
        if pkmn['BST'] > median_bst:
            return 0.5
        else:
            return 1


# -----------------------------------------

# completely random team
def generate_random_pokemon_1(team, slot):
    return choice(pkmn_list)

# half probability of getting a type again for each instance of that type in team
def generate_random_pokemon_2(team, slot):
    if slot == 1:
        new_pkmn = choice(pkmn_list)
    else:
        new_pkmn = choices(pkmn_list, weights = [get_type_factor(pkmn) for pkmn in pkmn_list], k = 1)
        new_pkmn = new_pkmn[0]
    return new_pkmn

# same as 2 AND half probability of getting a pokemon as good (if last mon was bad) or as bad (if last mon was good) as the last mon
def generate_random_pokemon_3(team, slot):
    if slot == 1:
        new_pkmn = choice(pkmn_list)
    else:
        new_pkmn = choices(pkmn_list, weights = [bst_weight(team, slot, pkmn) * get_type_factor(pkmn) for pkmn in pkmn_list], k = 1)
        new_pkmn = new_pkmn[0]
    return new_pkmn

# ------------------------------------------

def reset():
    global pkmn_list
    pkmn_list = copy.copy(return_pkmn_list())
    config_tfs()

def add_to_team(team, pkmn):
    team.append(pkmn)
    pkmn_list.remove(pkmn)
    primary_type = pkmn['Types'][0]
    increment_type(primary_type)
    if len(pkmn['Types']) == 2:
        secondary_type = pkmn['Types'][1]
        increment_type(secondary_type)

def get_num_dupe_types(team):
    dupes = {}
    for pkmn in team:
        for type in pkmn['Types']:
            if type not in dupes:
                dupes[type] = 1
            else: 
                dupes[type] += 1
    counter = 0
    for value in dupes.values():
        counter += value - 1
    return counter

def get_avg_bst(team):
    bstt = 0
    for pkmn in team:
        bstt += pkmn['BST']
    return bstt/6

def create_team_1():
    reset()
    team = []
    add_to_team(team, generate_random_pokemon_1(team, 1))
    add_to_team(team, generate_random_pokemon_1(team, 2))
    add_to_team(team, generate_random_pokemon_1(team, 3))
    add_to_team(team, generate_random_pokemon_1(team, 4))
    add_to_team(team, generate_random_pokemon_1(team, 5))
    add_to_team(team, generate_random_pokemon_1(team, 6))
    return team

def create_team_2():
    reset()
    team = []
    add_to_team(team, generate_random_pokemon_2(team, 1))
    add_to_team(team, generate_random_pokemon_2(team, 2))
    add_to_team(team, generate_random_pokemon_2(team, 3))
    add_to_team(team, generate_random_pokemon_2(team, 4))
    add_to_team(team, generate_random_pokemon_2(team, 5))
    add_to_team(team, generate_random_pokemon_2(team, 6))
    return team

def create_team_3():
    reset()
    team = []
    add_to_team(team, generate_random_pokemon_3(team, 1))
    add_to_team(team, generate_random_pokemon_3(team, 2))
    add_to_team(team, generate_random_pokemon_3(team, 3))
    add_to_team(team, generate_random_pokemon_3(team, 4))
    add_to_team(team, generate_random_pokemon_3(team, 5))
    add_to_team(team, generate_random_pokemon_3(team, 6))
    return team

#print(create_team_3())




