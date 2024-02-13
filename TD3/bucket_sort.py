import numpy as np
from mpi4py import MPI
import time

def creat_bucket(A, dim, nbp):
    # Calculate the range of values for each process
    min_value, max_value = min(A), max(A)
    value_range = (max_value - min_value) / nbp

    # Initialize empty buckets
    buckets = np.zeros((nbp, dim + 1), dtype=np.int64)

    # Assign values to buckets based on their range
    for value in A:
        bucket_index = int((value - min_value) / value_range)
        if bucket_index == nbp:
            bucket_index -= 1
        buckets[bucket_index][buckets[bucket_index][0] + 1] = value
        buckets[bucket_index][0] += 1
    return buckets

# MPI initialization
globCom = MPI.COMM_WORLD
nbp = globCom.size
rank = globCom.rank

dim = 20

buckets = None
tab = np.empty(dim + 1, dtype=np.int64)

if rank == 0:
    # Generate a list of random values
    A = np.random.randint(0, 100, dim)
    print(f"A = {A}")
    time1 = time.time()
    buckets = creat_bucket(A, dim, nbp)

globCom.Scatter(buckets, tab, root=0)
bucket = tab[1:tab[0]+1]
    
print(f"Process {rank} received {bucket}")
bucket.sort()
gathered_data = globCom.gather(bucket, root=0)

if rank == 0:
    time2 = time.time()
    sorted_data = np.concatenate(gathered_data)
    print("Sorted data:", sorted_data)
    print(f"Time taken: {time2 - time1} seconds")