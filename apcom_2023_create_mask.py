import itertools
from DPE_functions import *

FileInPath = r'C:\Users\andrej\Documents\FEI\2023_APCOM_prispevok\tpx2_info\\'

original = np.loadtxt(FileInPath + 'x_ray_10keV_70uA_0000.txt')
hdpe1 = np.loadtxt(FileInPath + 'Mask_1HDPE.txt')
hdpe2 = np.loadtxt(FileInPath + 'Mask_2HDPE.txt')
hdpe3 = np.loadtxt(FileInPath + 'Mask_3HDPE.txt')
kapton = np.loadtxt(FileInPath + 'Mask_kapton.txt')

mask = np.zeros([256,256])

for i, j in itertools.product(range(256), range(256)):
    if kapton[i,j] != 0:
        mask[i,j] = 1

for i, j in itertools.product(range(256), range(256)):
    if hdpe1[i,j] != 0:
        mask[i,j] = 2

for i, j in itertools.product(range(256), range(256)):
    if hdpe2[i,j] != 0:
        mask[i,j] = 3

for i, j in itertools.product(range(256), range(256)):
    if hdpe3[i,j] != 0:
        mask[i,j] = 4

tickfnt = 14
mydpi = 300
title = 'TPX2 X00 Si 500 $\mu$m regions'

# make a color map of fixed colors
cmap = colors.ListedColormap(['cyan', 'magenta', 'yellow', 'black', 'red'])
bounds=[0,1,2,3,4,5]
norm = colors.BoundaryNorm(bounds, cmap.N)

plt.close()
plt.cla()
plt.clf()
plt.rcParams["figure.figsize"] = (11.7, 8.3)
img=plt.matshow(mask[:,:], interpolation='nearest', origin='lower', cmap=cmap, norm=norm)
# If the orientation of matrix doesnt fit, use this instead
#plt.matshow(np.flip(np.rot90(
    #original[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
plt.gca().xaxis.tick_bottom()
cbar = plt.colorbar(img,label='Number of counts [-]', shrink=0.8, aspect=20*0.8, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0,1,2,3,4,5])
cbar.set_label(label='Number of counts [-]', size=tickfnt,
               weight='regular')   # format="%.1E"
cbar.ax.tick_params(labelsize=tickfnt)
# plt.clim(vmin,vmax) - set your own range using vmin, vmax
plt.clim(0, 4)
plt.xlabel('X position [pixel]', fontsize=tickfnt)
plt.ylabel('Y position [pixel]', fontsize=tickfnt)
plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label=title, fontsize=tickfnt+4)
plt.savefig(FileInPath + 'mask.png', dpi=mydpi,
            transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt(FileInPath + 'mask.txt', mask, fmt="%.3f")

title = 'X-ray of TPX2 X00 Si 500 $\mu$m'

plt.close()
plt.cla()
plt.clf()
plt.rcParams["figure.figsize"] = (11.7, 8.3)
img=plt.matshow(original[:,:], origin='lower')
# If the orientation of matrix doesnt fit, use this instead
#plt.matshow(np.flip(np.rot90(
    #original[::-1, :])), origin='lower', cmap='modified_hot', norm=colors.LogNorm())
plt.gca().xaxis.tick_bottom()
cbar = plt.colorbar(label='Number of counts [-]', shrink=0.8, aspect=20*0.8)
cbar.set_label(label='Number of counts [-]', size=tickfnt,
               weight='regular')   # format="%.1E"
cbar.ax.tick_params(labelsize=tickfnt)
# plt.clim(vmin,vmax) - set your own range using vmin, vmax
plt.clim(0, 5000)
plt.xlabel('X position [pixel]', fontsize=tickfnt)
plt.ylabel('Y position [pixel]', fontsize=tickfnt)
plt.xticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
plt.yticks([0, 63, 127, 191, 255], ['1', '64', '128', '192', '256'])
plt.tick_params(axis='x', labelsize=tickfnt)
plt.tick_params(axis='y', labelsize=tickfnt)
plt.title(label=title, fontsize=tickfnt+4)
plt.savefig(FileInPath + 'original.png', dpi=mydpi,
            transparent=True, bbox_inches="tight", pad_inches=0.01)
np.savetxt(FileInPath + 'original.txt', original, fmt="%.3f")