# Only works for symmetric ply thicknesses for now
# Reference: Example 1 page 17 Chapter 9 Lecture Slides for strain calculation
# Reference: Example page 19 Chapter 8 Lecture Slides for Primary and Principle stress plots
import numpy as np
import matplotlib.pyplot as plt
from constants import *
from Q_and_Qbar import *
from ABD_matrices import *
from stresses_strains import *
from tsai_wu import failure_criterion

np.set_printoptions(precision=4)

print("Odd \n", height, ", ", stack, "\n")
print("Even \n", height, ", ", stack, "\n")
print("(midplane, height array) ", midplane, ", ", height, '\n')

A, B, D = ABD_triple(Q0, stack, height)

print("\n", "A \n", A, "\n B \n", B, "\n D \n", D, "\n")

ABD = ABD_matrix(A, B, D)
print("\n ABD stiffness matrix in hectanewton/meter, hectanewton, and hectanewton meter respectively: \n", ABD, "\n")

# Calculate principal laminate strains and radii of curvature at midplane
midstrain = np.dot(np.linalg.inv(ABD), force_moment)
print("\n Strains (ex, ey, exy) and radii of curvature (kx, ky, kxy): \n", midstrain)

# Assign variables for principal strains and stresses in each ply k
# Calculate principal and primary strains and stresses in each ply k
# Strain varies linearly
estrain_glob = midstrain[:3]
kstrain_glob = midstrain[3:6]

plystrain_glob, plystress_glob = global_ply(
    Q0, stack, estrain_glob, kstrain_glob, height)
plystrain_loc, plystress_loc = local_ply(
    plystrain_glob, plystress_glob, height, stack)

print("\n Principal Strain for each ply boundary: \n", plystrain_glob, "\n")
print("\n Principal Stress for each ply boundary: \n", plystress_glob, "\n")
print("\n Primary Strain for each ply boundary: \n", plystrain_loc, "\n")
print("\n Primary Stress for each ply boundary: \n", plystress_loc, "\n")

# temporary values to input into the function to ensure it works
plystresses = np.ones(shape=(3, ply_num))
maxstress = np.full((5, ply_num), 0.5)

print(failure_criterion(plystresses, maxstress))

# x values for plotting purposes mwahahahah >:]
plot_height = np.zeros(2*len(height)-2)
for k in range(len(height)-1):
    plot_height[2*k] = height[k]
    plot_height[2*k+1] = height[k+1]
