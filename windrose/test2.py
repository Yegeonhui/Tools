from windrose import WindroseAxes
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from math import  radians


direc = np.arange(0, 361, 22.5)
direc_mark = ['N', 'NNE','NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
sdirec=['SW', 'ESE', 'NW', 'ESE', 'E', 'WSW', 'E', 'ESE', 'SE', 'N', 'SW', 'WNW']
for i in range(len(sdirec)):
    index = direc_mark.index(sdirec[i])
    sdirec[i] = direc[index - 13] 

#sdirec = [radians(a) for a in sdirec]
svel=[12, 13, 11, 12, 12, 11, 14, 14, 16, 14, 10, 11]
# ax = WindroseAxes.from_ax()

# ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
# ax.set_theta_zero_location('N')
# viridis = plt.get_cmap('Set1')
# #ax.bar(sdirec, svel, normed=True, opening=0.8, edgecolor='white')
# ax.bar(sdirec, svel, normed=True, opening=0.8, edgecolor='white', cmap=viridis)
# #ax.set_legend()
# plt.savefig('windrose1.png')
# plt.show()

bins_range = np.arange(10, 16, 1)
ax = WindroseAxes.from_ax()
ax.set_xticklabels(['N', 'NW',  'W', 'SW', 'S', 'SE','E', 'NE'])
ax.set_theta_zero_location('N')
viridis = plt.get_cmap('hot')
ax.bar(sdirec, svel, normed=True, opening=0.8, edgecolor='white', bins=bins_range, cmap=viridis)

#ax.set_legend()
plt.savefig('windrose1.png')
plt.show()

