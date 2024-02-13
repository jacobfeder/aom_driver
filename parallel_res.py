import numpy as np
import matplotlib.pyplot as plt
import pylab

x = np.linspace(0, 1)
pot_R = 2e6 * x
shunt_R = 2.7e6
out_voltage = 10e-6 * 1 / (1/pot_R + 1/shunt_R)

###########
# plotting
###########
plot_width = 10

norm_fontsize = 22
small_fontsize = int(norm_fontsize*0.75)
sup_smallfontsize = int(norm_fontsize*0.5)
big_fontsize = int(norm_fontsize*1.25)

# fix title and axis spacing
plt.rcParams.update({
    # 'font.weight': 'bold',
    # 'axes.labelweight': 'bold',
    'font.size': norm_fontsize,
    'axes.titlepad': 10,
    'xtick.major.pad': 4,
    'savefig.dpi': 4*96,
    })

# figure setup
fig = plt.figure()
fig.set_size_inches(plot_width, 0.75*plot_width)

# axes
ax = plt.axes()

plt.plot(x, out_voltage)

# x/y grid lines
pylab.grid(True, linestyle='dashed')

# plot title
plt.title('Pot Adjustment', fontsize=big_fontsize)

# x axis label
plt.xlabel('Pot Turn', labelpad=5)
plt.xticks()

# y axis label
plt.ylabel('Voltage', labelpad=5)
plt.yticks()

# edge padding
fig.tight_layout(pad=0.5)

# save the plot
# fig.savefig(f'plt.png')

# show the plots
plt.show()
