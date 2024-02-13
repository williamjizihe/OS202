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

rows_per_proc = dim // nbp if dim % nbp == 0 else dim // nbp + 1
start_row = rows_per_proc * rank
end_row = rows_per_proc * (rank+1) if rank != nbp-1 else dim

local_A = A[start_row:end_row, :]
local_v = local_A.dot(u)

# Gather the resulting vector v
if rank == 0:
    v = np.empty(rows_per_proc * nbp)
else:
    v = None
globCom.Gatherv(local_v, v, root=0)

if rank == 0:
    v = v[:dim]
    print(f"v = {v}")
