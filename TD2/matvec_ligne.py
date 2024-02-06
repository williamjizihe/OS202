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

rows_per_proc = int(dim / nbp) + 1 if dim % nbp != 0 else int(dim / nbp)
rest = rows_per_proc * nbp - dim

local_v = np.zeros(dim)
if rank == nbp-1:
    local_A = A[rows_per_proc * rank:, :]
    local_v = local_A.dot(u)
    if rest != 0:
        local_v = np.pad(local_v, (0, rest), 'constant')
else:
    end_row = rows_per_proc * (rank+1) if rank != nbp-1 else dim
    local_A = A[rows_per_proc * rank:rows_per_proc * (rank+1), :]
    local_v = local_A.dot(u)

# Gather the resulting vector v
if rank == 0:
    v = np.empty(rows_per_proc * nbp)
else:
    v = None
globCom.Gather(local_v, v, root=0)
v = v[:dim]

if rank == 0:
    print(f"v = {v}")
