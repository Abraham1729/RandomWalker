# RandomWalker

Y'all figure this out on your own what do you think this is some sort of charity??

The main thing is you're going to want to compile the RandomCompute.c file into a shared library so that the InteractiveWalker.py script can pick it up. I *could* write up a commandline argument to do that, but I'm working with GCC and I don't know if that's gonna work nicely with Windows machines of if you barbarians will have to figure out the compiler of your choice and necessary flags to do the same.

Anwyays here's the gcc way of doing things:

```
gcc -shared -o <outputname>.so <c_file>.c
```

so in our case if you're using MacOS, you should just be able to run

```
gcc -shared -o RandomCompute.so RandomCompute.c
```

and that should be it.

*Please do not use the pre-compiled shared library I will be disappointed in you*

*It's just there because I'm a mess right now ok?*
