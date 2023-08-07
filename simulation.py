import numpy as np
from matplotlib import pyplot as plt
import team_builder 

# print(team_builder.create_team_2())

np.random.seed(0)
dupe_types = []
bsts = []
for i in range(0, 1001):
    team = team_builder.create_team_3()
    dupe_types.append(team_builder.get_num_dupe_types(team))
    bsts.append(team_builder.get_avg_bst(team))

print(np.average(dupe_types), np.std(dupe_types))
plt.hist(dupe_types, bins=np.arange(np.min(dupe_types), np.max(dupe_types) + 1))
plt.show()

# print(np.average(bsts), np.std(bsts))
# plt.scatter([i for i in range(0, 1001)], bsts)
# plt.show()


