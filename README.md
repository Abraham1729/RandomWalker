# RandomWalker

Note to self: my compiled shared library probalby won't be running on Joe's computer.
Note to self: be friendly to Joe (if he uses MacOS)
Note to self: Tell Joe about GCC
Note to self: Joe might be stupid. Don't tell Joe about GCC. Give Joe what he needs. What he wants. What he crav-

Hi Joe,

I'm writing to you today because I respect you as a fellow MacOS user who by default has GCC available as an option for compiling C code into shared libraries on your wonderful MacOS device from Apple (Thanks Steve).

I know you've been warned against the suggestion that it's a good and safe idea to run code that strangers give you off the internet. That being said, I know you're not a moron, Joe. After all, you do use MacOS.

I'm going to need you to trust me on this one Joe -- I desperately need you to open Terminal and navigate to the directory where you've downloaded this repository to. I'm going to need you to navigate to the src folder and run the following command:

```
gcc -shared -o RandomCompute.so RandomCompute.c
```

Ok I could be flashy and write a Makefile so that all you have to do is navigate to the base directory for the repo and run

```
make all
```

but that would be classy and that is not me. Maybe another day when I'm not feeling bloated from eating one too many of my undercooked cookies (bless their souls).

In the meantime:

Once you've done that, please go ahead and run the InteractiveWalker.py script to have your fun. Please feel free to mess with the widgets -- I've put a lot of time into wrestling with matplotlib on this part and would appreciate it if you made an effort to use each button or textbox at least 4 times so I know people are getting good value out of it. Please experiment with as many values as you want, and I promise that I used pointers responsibly and won't be bricking your sytem any time soon.

Oh right

```
python3 InteractiveWalker.py
```

in case you aren't familiar with python.

Oh right right dependencies. I guess you'll probably need python: matplotlib, numpy, ... you know what you're a smart chap Joe, you can go read through the freakin' source code yourself and figure out what you need. You did find this place, after all, so you've got to know *something* about how to operate a computer.

