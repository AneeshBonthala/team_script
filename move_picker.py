from move_parser import return_move_list
import team_builder
from global_move_parser import return_all_moves
import numpy as np
from random import choice, choices, randint, sample
import copy

pkmn_moves = copy.copy(return_move_list())
all_moves = copy.copy(return_all_moves())

rand_team = team_builder.create_team_1()
balanced_team = team_builder.create_team_3()


# First move:
# Pokemon's 7 best moves are put into a list
# One is chosen at random to be its first move
# Moves of STAB type are 8x more likely to be chosen
# Hyper Beam is always 2x less likely to be chosen because of how common it is

def choose_move_1(pkmn):
    index = pkmn_moves.index(pkmn['Name']) + 1
    pkmn_learnset = pkmn_moves[index]
    possible_move = []
    possible_ev = []
    possible_weights = []
    for move in pkmn_learnset:
        move_index = all_moves.index(move['Name'])
        move_name = all_moves[move_index]
        move_type = all_moves[move_index + 1]
        expected_value = all_moves[move_index + 2]
        factor = 1
        if move_type in pkmn['Types']:
            factor = 8
        if move_name == 'MOVE_HYPER_BEAM':
            factor = 0.5
        if len(possible_move) < 7:
            possible_move.append(move_name)
            possible_ev.append(expected_value)
            possible_weights.append(factor)
        else:
            seventh_strongest = np.min(possible_ev)
            index_to_pop = possible_ev.index(seventh_strongest)
            if expected_value > seventh_strongest:
                possible_move.pop(index_to_pop)
                possible_ev.pop(index_to_pop)
                possible_weights.pop(index_to_pop)
                possible_move.append(move_name)
                possible_ev.append(expected_value)
                possible_weights.append(factor)
            elif expected_value == seventh_strongest:
                rand_int = randint(0, 1)
                if rand_int == 0:
                    possible_move.pop(index_to_pop)
                    possible_ev.pop(index_to_pop)
                    possible_weights.pop(index_to_pop)
                    possible_move.append(move_name)
                    possible_ev.append(expected_value)
                    possible_weights.append(4) if move_type in pkmn['Types'] else possible_weights.append(1)
    #print(possible_move)
    chosen_move = choices(possible_move, weights = possible_weights, k = 1)
    return chosen_move[0]

# Second move
# If Pokemon is Ditto, return
# Otherwise, all of Pokemon's moves are put into a list
# One is chosen at random to be Pokemon's second move
# If move_1 was not of STAB type,
#   STAB types are now 32x more likely to be chosen
# Else, they are just 1x likely to be chosen

def choose_move_2(pkmn, move_1):
    if pkmn['Name'] == 'Ditto':
        return None
    index = pkmn_moves.index(pkmn['Name']) + 1
    pkmn_learnset = pkmn_moves[index]
    possible_move = []
    possible_weights = []
    move_1_index = all_moves.index(move_1)
    for move in pkmn_learnset:
        move_index = all_moves.index(move['Name'])
        move_name = all_moves[move_index]
        move_type = all_moves[move_index + 1]
        expected_value = all_moves[move_index + 2]
        if move_name == move_1:
            continue
        factor = 1
        if all_moves[move_1_index + 1] not in pkmn['Types']:
            factor = 32
        possible_move.append(move_name)
        possible_weights.append(factor) if move_type in pkmn['Types'] else possible_weights.append(1)
    #print(possible_move)
    chosen_move = choices(possible_move, weights = possible_weights, k = 1)
    return chosen_move[0]

# Third Move
# All of Pokemon's moves are put into a list
# Status Effect moves are 16x more likely to be chosen
# All others are just 1x likely to be chosen

def choose_move_3(pkmn, move_1, move_2):
    index = pkmn_moves.index(pkmn['Name']) + 1
    pkmn_learnset = pkmn_moves[index]
    possible_move = []
    possible_weights = []
    for move in pkmn_learnset:
        move_index = all_moves.index(move['Name'])
        move_name = all_moves[move_index]
        expected_value = all_moves[move_index + 2]
        if move_name == move_1 or move_name == move_2:
            continue
        possible_move.append(move_name)
        factor = 1
        if expected_value == 0:
            factor = 16
        possible_weights.append(factor)
    chosen_move = choices(possible_move, weights = possible_weights, k = 1)
    return chosen_move[0]
            
# Fourth Move
# If any of Pokemon's moves require a sleep-inducing move to be effective
# Give that Pokemon a sleep inducing move if possible
# Otherwise, all of Pokemon's level-up learnset moves are put into a list
# One is chosen at random

def choose_move_4(pkmn, move_1, move_2, move_3):
    index = pkmn_moves.index(pkmn['Name']) + 1
    pkmn_learnset = pkmn_moves[index]
    flag = False
    possible_move = []
    for entry in [move_1, move_2, move_3]:
        if entry == 'MOVE_SLEEP_TALK' or entry == 'MOVE_SNORE':
            return 'MOVE_REST'
        if entry == 'MOVE_DREAM_EATER':
            flag = True
    for move in pkmn_learnset:
        if move['Name'] == move_1 or move['Name'] == move_2 or move['Name'] == move_3:
            continue
        if move['Name'] == 'MOVE_DREAM_EATER' or move['Name'] == 'MOVE_SNORE' or move['Name'] == 'MOVE_SLEEP_TALK':
            continue
        if flag == True:
            if move['Name'] == 'MOVE_SLEEP_POWDER':
                return 'MOVE_SLEEP_POWDER'
            if move['Name'] == 'MOVE_SING':
                return 'MOVE_SING'
            if move['Name'] == 'MOVE_HYPNOSIS':
                return 'MOVE_HYPNOSIS'
            if move['Name'] == 'MOVE_YAWN':
                return 'MOVE_YAWN'
            if move['Name'] == 'MOVE_LOVELY_KISS':
                return 'MOVE_LOVELY_KISS'
        if move['Learned'] == 'lvlup' or move['Learned'] == 'u20':
            possible_move.append(move['Name'])
    return choice(possible_move)

def assign_moves(team):
    pokemon_moves = []
    for pkmn in team:
        pokemon_moves.append(pkmn['Name'])
        move_1 = choose_move_1(pkmn)
        move_2 = choose_move_2(pkmn, move_1)
        if move_2 == None:
            pokemon_moves.append((move_1, 'MOVE_NONE', 'MOVE_NONE', 'MOVE_NONE'))
            continue
        move_3 = choose_move_3(pkmn, move_1, move_2)
        move_4 = choose_move_4(pkmn, move_1, move_2, move_3)
        pokemon_moves.append((move_1, move_2, move_3, move_4))
    return pokemon_moves

def random_moves(team):
    pokemon_moves = []
    for pkmn in team:
        if pkmn['Name'] == 'Ditto':
            moves = ('MOVE_TRANSFORM')
            continue
        pokemon_moves.append(pkmn['Name'])
        index = pkmn_moves.index(pkmn['Name']) + 1
        pkmn_learnset = pkmn_moves[index]
        moves = sample([move['Name'] for move in pkmn_learnset], k = 4)
        moves = tuple(moves)
        pokemon_moves.append(moves)
    print(pokemon_moves)

# random_moves(rand_team)
# assign_moves(rand_team)
# print(team_builder.get_avg_bst(rand_team), team_builder.get_num_dupe_types(rand_team))
# random_moves(balanced_team)
# assign_moves(balanced_team)
# print(team_builder.get_avg_bst(balanced_team), team_builder.get_num_dupe_types(balanced_team))
