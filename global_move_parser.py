
all_moves = []

with open('text/move_data.txt') as global_moves:
    power = 0
    for line in global_moves:
        if '[MOVE' in line:
            new_line = line.strip()
            move_name = new_line[1:-3]
            all_moves.append(move_name)
        if 'power' in line:
            new_line = line.strip('        .power = ')
            new_line = new_line[:-2]
            power = int(new_line)
        if 'accuracy' in line:
            new_line = line.strip('        .accuracy = ')
            new_line = new_line[:-2]
            accuracy = int(new_line) / 100
            expected_value = power * accuracy
            all_moves.append(expected_value)
            power = 0
        if 'type' in line:
            new_line = line.strip('        .type = ')
            type = new_line[:-2]
            all_moves.append(type)

# with open('output.txt', 'w') as output:
#     output.write(str(all_moves))

def return_all_moves():
    return all_moves



