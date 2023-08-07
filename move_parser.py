# Since all teams will be set at Lvl. 50, only level up moves obtainable
# up to and including Lvl. 50 are valid selections
from pkmn_parser import return_pkmn_list
import copy

pkmn_list = copy.copy(return_pkmn_list())
pkmn_names = [pkmn['Name'] for pkmn in pkmn_list]
pkmn_moves = []

invalid_tutor_moves = ['MOVE_BODY_SLAM', 'MOVE_SWORDS_DANCE']
invalid_tmhms = ['MOVE_SLUDGE_BOMB', 'MOVE_FACADE', 'MOVE_WATERFALL']

# parse level up moves
with open('text/all_lvlup_moves.txt') as lvlup_moves:
    pkmn_name = None
    pkmn_learnset = []
    for_dupe_moves = []
    for line in lvlup_moves:
        if 'Learnset' in line:
            pkmn_name = line.strip('static const u16 s')[:-22]
            if pkmn_name in pkmn_names:
                pkmn_moves.append(pkmn_name)
                #print(pkmn_learnset)
                #print(pkmn_name)
        if 'MOVE' in line and pkmn_name in pkmn_names:
            move = {}
            new_line = line.strip().strip('LEVEL_UP_MOVE(')
            new_line = new_line.split(', ')
            level = int(new_line[0])
            move_name = new_line[1][:-2]
            if level > 50 or move_name in for_dupe_moves:
                continue
            elif level < 20:
                move['Learned'] = 'u20'
            else:
                move['Learned'] = 'lvlup'
            move['Name'] = move_name
            pkmn_learnset.append(move.copy())
            for_dupe_moves.append(move_name)
        if 'LEVEL_UP_END' in line and pkmn_name in pkmn_names:
            pkmn_moves.append(pkmn_learnset.copy())
            pkmn_learnset.clear()
            for_dupe_moves.clear()


#print(pkmn_moves)

#parse tutor moves

with open('text/all_tutor_moves.txt') as tutor_moves:
    index = 0
    pkmn_name = None
    for line in tutor_moves:
        if 'SPECIES' in line:
            lines = line.split(' = ')
            pkmn_name = lines[0]
            pkmn_name = pkmn_name.strip()
            pkmn_name = pkmn_name[9:-1].title()
            if pkmn_name not in pkmn_names:
                continue
            #print(pkmn_name)
            index = pkmn_moves.index(pkmn_name) + 1
            #print(index)
            if 'MOVE' in line:
                move = {}
                move_name = lines[1]
                move_name = move_name[6:-2]
                if move_name in invalid_tutor_moves or move_name in pkmn_moves[index]:
                    continue
                move["Learned"] = 'tutor'
                move['Name'] = move_name
                pkmn_moves[index].append(move.copy())
        elif 'MOVE' in line and pkmn_name in pkmn_names:
            move = {}
            new_line = line.strip()
            move_name = new_line[8:-1]
            if move_name[-1] == ')':
                move_name = move_name[:-1]
            if move_name in invalid_tutor_moves or move_name in pkmn_moves[index]:
                continue
            move["Learned"] = 'tutor'
            move['Name'] = move_name
            pkmn_moves[index].append(move.copy())

# parse tmhm moves

with open('text/all_tmhm_moves.txt') as tmhm_moves:
    index = 0
    pkmn_name = None
    for line in tmhm_moves:
        if 'SPECIES' in line:
            lines = line.split(' = ')
            pkmn_name = lines[0]
            pkmn_name = pkmn_name.strip()
            pkmn_name = pkmn_name[9:-1].title()
            if pkmn_name not in pkmn_names:
                continue
            #print(pkmn_name)
            index = pkmn_moves.index(pkmn_name) + 1
            #print(index)
            if 'TMHM(' in line:
                move = {}
                move_name = lines[1]
                move_name = move_name[23:-2]
                move_name = 'MOVE' + move_name
                if move_name in invalid_tmhms or move_name in pkmn_moves[index]:
                    continue
                move["Learned"] = 'tmhm'
                move['Name'] = move_name
                pkmn_moves[index].append(move.copy())
        elif 'TMHM(' in line and pkmn_name in pkmn_names:
            move = {}
            new_line = line.strip()
            move_name = new_line[11:-1]
            move_name = 'MOVE' + move_name
            if move_name[-1] == ')':
                move_name = move_name[:-2]
            if move_name in invalid_tmhms or move_name in pkmn_moves[index]:
                continue
            move["Learned"] = 'tmhm'
            move['Name'] = move_name
            pkmn_moves[index].append(move.copy())

with open('output.txt', 'w') as output:
    output.write(str(pkmn_moves))

def return_move_list():
    return pkmn_moves