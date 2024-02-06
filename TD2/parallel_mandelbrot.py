# Calcul de l'ensemble de Mandelbrot en python
from mpi4py import MPI
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm as cm


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False):# -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3./width
scaleY = 2.25/height
convergence = np.empty((width, height), dtype=np.double)

# Calcul de l'ensemble de mandelbrot :
def calculate_band(start_row, end_row, width, height, scaleX, scaleY, mandelbrot_set):
    band = np.zeros((end_row - start_row, width), dtype=np.double)
    for y in range(start_row, end_row):
        if y >= height:
            break
        for x in range(width):
            c = complex(-2. + scaleX*x, -1.125 + scaleY * y)
            band[y - start_row, x] = mandelbrot_set.convergence(c, smooth=True)
    return band

# MPI initialization
globCom = MPI.COMM_WORLD
nbp = globCom.size
rank = globCom.rank

rows_per_process = int(height / nbp) + 1 if height % nbp != 0 else int(height / nbp)
start_row = rank * rows_per_process
end_row = start_row + rows_per_process

deb = time()
local_band = calculate_band(start_row, end_row, width, height, scaleX, scaleY, mandelbrot_set)
fin = time()

if rank == 0:
    print(f"Temps du calcul de l'ensemble de Mandelbrot : {fin-deb}")
    full_image = np.empty((rows_per_process * nbp, width), dtype=np.double)
else:
    full_image = None

globCom.Gather(local_band, full_image, root=0)

if rank == 0:
    deb = time()
    # Si le nombre de processus ne divise pas height, il faut tronquer l'image
    full_image = full_image[:height, :] 
    image = Image.fromarray(np.uint8(cm.plasma(full_image.T)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()