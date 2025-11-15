# RandomWalker #

## Why this exists ##
I was being a nerd and was watching Numberphile videos when I saw their exploration of the Chaos game. The big reveal of the video was the emergent Sierpinsky triangle, which I thought could not be anything other than a mistake in their code, so I decided to code it up myself. I was pleasantly surprised to find that I recovered their findings. To recover some face for my intuition being so wrong, I decided to make it beefier / better than their code, and eventually discovered that the domain of the Chaos game is much more fun once you start varying the distance factor as well.

Here's a link to the abovementioned video. It might be worth a watch. They also talk about Barnsley fers which are cool -- I'm sadly not smart enough to figure that one out though.

https://www.youtube.com/watch?v=kbKtFN71Lfs

## Get started ##
To launch the simulation, use the Makefile to compile the appropriate C libraries, then run the shell script provided:

```
make all
./run.sh
```

## Overview of Implementation ##
This is a Python program that leverages a custom compiled C library to compute the simluation values, and displays the results via MatPlotLib. NumPy and CTypes are implemented to allow the C functions to work with the same arrays allocated to the Python process, which significantly reduces the overall simulation time by eliminating a copy step that I previously didn't understand the need to eliminate.

App.py is the entry point for the program. It defines the initial parameters for the simulation, and then creates and passes parameters into the Game and Graph managers.

GameRules.py contains the Game manager class. Its primary function is to encapsulate and leverage the functionality written in RandomCompute.c. 

Grapher.py contains the Graph manager class. This class is responsible for the MatPlotLib figure lifecycle for the display window and the toolbar window. Usage of custom widgets are defined here.

MyWidgets.py is a collection of custom MatPlotLib Widgets to provide a GUI for modifying relevant simulation parameters.

RandomCompute.C is the heart of the simulation. It contains functionality for computing the sequence of destinations the walker travels towards, and the locations the walker visits. It also includes functionality for performing world-to-screen coordinate transformations so that a heat map can be generated and displayed by the Grapher manager.

## Dependencies ##
1. Python
    - Numpy
    - CTypes
    - MatPlotLib
2. python3-tk (Linux backend for MatPlotLib)
3. gcc
