#usr/bin/python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import UnivariateSpline
from scipy.integrate import quad
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

xminorLocator = AutoMinorLocator()
y1minorLocator = AutoMinorLocator()
y2minorLocator = AutoMinorLocator()


def integrate(x, y, a, b):
    """
    x - independent variable of the data set
    y - dependent variable of the data set
    a - lower limit of integration (usually 0)
    b - upper limit of integration (usually 1)
    """
    #Fit a spline
    spline = UnivariateSpline(x, y, s=0)
    
    #Evaluate the spline
    '''plt.plot(x, y, 'o', label='Data')
    plt.plot(x, spline(x), '-', label='Cubic Spline')
    plt.legend()
    plt.show()'''
    
    #Integrate the spline
    integral_value = spline.integral(a, b) 
    return integral_value, spline(x)

kJ_mol_Kelvin = 120	# 1 kJ/mol = 120 K

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

integrate_value , spline_fit = integrate(dUdl_array_sorted[:,0],dUdl_array_sorted[:,1], 0 , 1)

#print(f"Integrated answer is {np.trapz(dUdl_array_sorted[:,1],dUdl_array_sorted[:,0])} kJ/mol")
print(f"Integrated answer is {integrate_value:.3f} kJ/mol")

### Plotting ###
fig, axs = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(6,4.2))
fig.subplots_adjust(hspace=0.1)

axs.plot(dUdl_array_sorted[:,0], dUdl_array_sorted[:,1],color='blue', linestyle='solid', linewidth=2, marker='s', markersize=4, label='NO$_{3}^{-}$ + H$_{3}$O$^{+}$')
axs.plot(dUdl_array_sorted[:,0], spline_fit, linestyle='solid', color='darkorange', linewidth=2, label = 'Cubic fit')

axs.grid(True)
axs.grid(which='both')
axs.grid(which='minor', alpha=0.1)
axs.grid(which='major', alpha=0.5)
axs.set_ylabel('$\langle \\frac{\partial U}{\partial \lambda} \\rangle$ / [kJ/mol]', fontsize=14)
axs.set_xlabel('$\lambda$',  fontsize=14)
legend = axs.legend(loc='lower left', shadow=False, fontsize=10, frameon=False)

fig.tight_layout()
fig.savefig('dUdl_NO3n_H3Op_with_CubicFit.pdf')
fig.savefig('dUdl_NO3n_H3Op_with_CubicFit.svg')
