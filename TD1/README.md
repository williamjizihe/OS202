
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`

## lscpu

coller ici les infos *utiles* de lscpu.

*Des infos utiles s'y trouvent : nb core, taille de cache*
Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
NumberOfCores 6
NumberOfLogicalProcessors 12

## Produit matrice-matrice

| dim  | Temps CPU (s) | MFlops  |
|------|---------------|---------|
| 1024 | 2.59509       | 827.518 |
| 1023 | 1.20846       | 1771.81 |
| 1025 | 1.25418       | 1717.28 |

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`mingw32-make TestProductMatrix.exe && ./TestProductMatrix.exe 1024`

| ordre       | time     | MFlops  | MFlops(n=2048) |
|-------------|----------|---------|----------------|
| i,j,k(orig) | 2.42437  | 885.792 | 298.626        |
| j,i,k       | 2.45405  | 875.079 | 264.208        |
| i,k,j       | 14.1017  | 152.286 |                |
| k,i,j       | 14.8245  | 144.86  |                |
| j,k,i       | 0.659577 | 3255.85 | 2675.62        |
| k,j,i       | 0.910057 | 2359.73 | 2008.12        |

*Discussion des résultats*

### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

| OMP_NUM | MFlops | MFlops(n=2048) | MFlops(n=512) | MFlops(n=4096) |
|---------|--------|----------------|---------------|----------------|
| 1       |        |                |               |                |
| 2       |        |                |               |                |
| 3       |        |                |               |                |
| 4       |        |                |               |                |
| 5       |        |                |               |                |
| 6       |        |                |               |                |
| 7       |        |                |               |                |
| 8       |        |                |               |                |




### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
