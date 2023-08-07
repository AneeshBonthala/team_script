from move_picker import assign_moves
from team_builder import create_team_3

team = create_team_3()

with open('output.txt', 'w') as output:
    output.write('\n'.join([str(entry) for entry in assign_moves(team)]))