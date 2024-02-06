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

rows_per_proc = dim // nbp

local_A = A[rows_per_proc*rank:rows_per_proc*(rank+1), :]
local_v = local_A.dot(u)

# Gather the resulting vector v
if rank == 0:
    v = np.empty(dim)
else:
    v = None
globCom.Gather(local_v, v, root=0)

if rank == 0:
    print(f"v = {v}")
