# RandomWalker #

## Rules of the Game ##
This project explores the journey of a traveler marching in the direction of randomly chosen vertices of an n-dimensional polygon. 

## Operational Details ##
To launch the simulation, use the Makefile to compile the appropriate C libraries, then run the shell script provided:

```
make all
./run.sh
```

## Overview of Implementation ##
Discuss the division of labor between Python and the compiled C library.

Discuss the division of labor between Python manager classes.

## Acknowledgements ##
Numberphile video on the Chaos game initially brought this idea to my attention with the reveal of the Sierpinsky Triangle via N=3 D=0.5. I didn't believe it, so I made it myself, then improved on it and played around with distance factors.

https://www.youtube.com/watch?v=kbKtFN71Lfs

## Dependencies ##
1. Python
    - Numpy
    - MatPlotLib
2. python3-tk (Linux backend for MatPlotLib)
3. gcc
