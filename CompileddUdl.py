#usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

xminorLocator = AutoMinorLocator()
y1minorLocator = AutoMinorLocator()
y2minorLocator = AutoMinorLocator()

kJ_mol_Kelvin = 120

root_folder = "./"

dUdl_list = []

for j in os.listdir(root_folder):
    if os.path.isdir(j):
        os.chdir(f"{j}/OUTPUT/CFC")
        a = np.loadtxt('dU_dlambda.out', comments='#')
        for i in range(len(a[:,0])):
            if str(a[i,1]) != 'nan':
                dUdl_list.append([a[i,0], a[i,1]/kJ_mol_Kelvin, a[i,2]/kJ_mol_Kelvin]) # Converting from Kelvin to kJ/mol
    else:
        continue
    os.chdir("../../../")

dUdl_list_sorted = sorted(dUdl_list)
dUdl_array_sorted = np.array(dUdl_list_sorted)
np.savetxt("Compiled_dU_dl.txt", dUdl_array_sorted, fmt=['%1.3f', ' %.4e', ' %.4e'], header='#Lambda dU/d\lambda[kJ/mol] Std.Err_dU/d\lambda [kJ/mol]')

print(f"Integrated answer is {np.trapz(dUdl_array_sorted[:,1],dUdl_array_sorted[:,0])} kJ/mol")

### Plotting ###
fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(6,4.2))
fig.subplots_adjust(hspace=0.1)

axs.plot(dUdl_array_sorted[:,0], dUdl_array_sorted[:,1],color='blue', linestyle='solid', linewidth=2, marker='s', markersize=4, label='NO$_{2}^{-}$ + H$_{3}$O$^{+}$')
#axs.plot(dUdl_array_sorted[:,0], dUdl_array_sorted[:,2],color='red', linestyle='solid', linewidth=2, marker='o', markersize=4, label='Column 2')

axs.grid(True)
axs.grid(which='both')
axs.grid(which='minor', alpha=0.1)
axs.grid(which='major', alpha=0.5)
axs.set_ylabel('$\langle \\frac{\partial U}{\partial \lambda} \\rangle$ / [kJ/mol]', fontsize=11)
axs.set_xlabel('$\lambda$',  fontsize=11)
#axs.set_ylim(-130,130)
#axs.set_ylim(-5,20)
#axs.set_xlim(1.8,4)
legend = axs.legend(loc='lower left', shadow=False, fontsize=10, frameon=False)

fig.tight_layout()
fig.savefig('dUdl_NO2n_H3Op.pdf')
fig.savefig('dUdl_NO2n_H3Op.svg')
