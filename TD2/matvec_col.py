# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI

# MPI initialization
globCom = MPI.COMM_WORLD
nbp = globCom.size
rank = globCom.rank

# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])

cols_per_proc = dim // nbp
start_col = cols_per_proc * rank
end_col = cols_per_proc * (rank+1) if rank != nbp-1 else dim

local_A = A[:, start_col:end_col]
local_u = u[start_col:end_col]
local_v = local_A.dot(local_u)

# Gather the resulting vector v
v = np.zeros(dim)
globCom.Allreduce(local_v, v, op=MPI.SUM)

if rank == 0:
    print(f"v = {v}")
