import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.animation import FuncAnimation
import numpy as np
import ctypes
import time

class GameRules():

    # C shared library
    compute_lib = ctypes.CDLL('./shared_compute.so')

    ### Defining library function signiture ###
    ## Compute Steps Footprint ##
    compute_lib.compute_steps.argtypes = [ctypes.c_int,                   # iterations        int
                                        ctypes.POINTER(ctypes.c_int),     # target            double array
                                        ctypes.c_double,                  # distance_factor   double
                                        ctypes.POINTER(ctypes.c_double),  # stepsX            double array
                                        ctypes.POINTER(ctypes.c_double),  # stepsY            double array
                                        ctypes.c_int,                     # num_anchors       int
                                        ctypes.POINTER(ctypes.c_double),  # anchorX           double array
                                        ctypes.POINTER(ctypes.c_double)]  # anchorY           double array
    compute_lib.compute_steps.restype = None                                # void

    ## Compute Targets and Steps Footprint ##
    compute_lib.targets_and_steps.argtypes = [ctypes.c_int,                   # iterations        int
                                        ctypes.POINTER(ctypes.c_int),     # target            double array
                                        ctypes.c_double,                  # distance_factor   double
                                        ctypes.POINTER(ctypes.c_double),  # stepsX            double array
                                        ctypes.POINTER(ctypes.c_double),  # stepsY            double array
                                        ctypes.c_int,                     # num_anchors       int
                                        ctypes.POINTER(ctypes.c_double),  # anchorX           double array
                                        ctypes.POINTER(ctypes.c_double)]  # anchorY
    compute_lib.targets_and_steps.restype = None

    def __init__(self,num_anchors,dist,iter,seed):
        ## Computational attributes/methods
        self.num = num_anchors
        self.iter = iter
        self.dist = dist
        self.set_seed(seed)     # sets self.seed, informs np.random module
        
        # Initial State Computations
        self.compute_anchors()  # Computers anchors in Python list
        self.targets_and_steps()# Compute targets and steps with C funciton

        ## Graphing-specific attributes/methods
        self.show_anchor = True # Toggling anchor display

    ## CType Memory Management Functions
    def set_c_anchors(self):
        # Can also be used to free / reinitialize
        self.cx_anchors = (ctypes.c_double * self.num)(*self.x_anchors)
        self.cy_anchors = (ctypes.c_double * self.num)(*self.y_anchors)

    def set_c_targets(self):
        # Can also be used to free / reinitialize
        self.c_targets = (ctypes.c_int * self.iter)()

    def set_c_steps(self):
        # Can also be used to free / reinitialize
        self.c_stepsX = (ctypes.c_double * self.iter)()
        self.c_stepsY = (ctypes.c_double * self.iter)()

    ## CType Computation Functions
    def targets_and_steps(self):
        ## Set up necessary ctype inputs
        self.set_c_targets()  # redundant on the first call of this function
        self.set_c_steps()    # same here -- redundant for first call

        ## Compute with C library: returns void, modifies target and step arrays.
        self.compute_lib.targets_and_steps(self.iter,
                                           self.c_targets,
                                           self.dist,
                                           self.c_stepsX,
                                           self.c_stepsY,
                                           self.num,
                                           self.cx_anchors,
                                           self.cy_anchors)

    def compute_anchors(self):
        self.x_anchors = []
        self.y_anchors = []
        angle = np.pi / 2   # np.pi / 4 is also nice

        for i in range(self.num):
            self.x_anchors.append(np.cos(angle))
            self.y_anchors.append(np.sin(angle))
            angle += 2*np.pi/self.num

        self.set_c_anchors()

    def compute_steps(self):
        ## Set up necessary ctype input
        self.reset_c_steps()

        ## Compute with C library; rerturns void, modifies step arrays.
        self.compute_lib.compute_steps(self.iter,
                                       self.c_targets,
                                       self.dist,
                                       self.c_stepsX,
                                       self.c_stepsY,
                                       self.num,
                                       self.cx_anchors,
                                       self.cy_anchors)

    # Update seed value
    def set_seed(self, seed):
        self.seed = seed
        np.random.seed(seed)

    # Plot it
    def graph_state(self):
        start = time.time()
        ax.clear()
        middle1 = time.time()
        ax.scatter(self.c_stepsX, self.c_stepsY, color=colormap[self.c_targets], s=3)    # Implement button to toggle colormap (esp for high pow_2)
        middle2 = time.time()
        if self.show_anchor:
            ax.scatter(self.x_anchors,self.y_anchors, color='k', s=5)       # Implement button to toggle this for high pow_2
        middle3 = time.time()
        plt.draw()
        end = time.time()
        print("Graphing Details:\n&&&&&&&&&&&&")
        print(f"Clearing axis:\t\t{middle1-start:.4f}")
        print(f"Scattering Bulk:\t{middle2-middle1:.4f}")
        print(f"Scattering Anchors:\t{middle3-middle2:.4f}")
        print(f"plt.draw():\t\t{end-middle3:.4f}")
        print(f"Total:\t\t\t{end - start:.4f}")
        print("&&&&&&&&&&&&&&&")


if __name__ == "__main__":

    ##### Inintial State #####
    start_num = 3
    start_dist = 0.5
    start_iter = 10000
    start_seed = 3170
    game = GameRules(num_anchors=start_num, dist = start_dist, iter=start_iter, seed=start_seed)

    ##### Matplotlib Setup #####
    fig = plt.figure(figsize=(8,6)) # default figsize (6.4,4.8) width height
    ax = fig.add_subplot()

    # (Colormap Initialization)
    nice_colors = np.array(
        [[0.75,0,0],[0,0.75,0],[0,0,0.75],
        [0.75,0.75,0],[0.75,0,0.75],[0,0.75,0.75]])
    rand_colors = np.random.random(size=(500,3)).round(1)           # Arbitrary dimension of 500, increase if you ever do anchors > 500.
    colormap = np.concatenate((nice_colors,rand_colors),axis=0)

    ### Widget functions ###
    if True:
        # # Seed-setting Textbox
        def seedbox(text):
            # Update State
            result = eval(text)
            if result != game.seed:     # (avoids unwanted submission for clicking out of box)
                game.set_seed(result)   # Sets the new seed
                game.targets_and_steps()

            # Plot new state
            game.graph_state()

        # Iter-setting Textbox
        def iterbox(text):
            # Update State
            result = eval(text)
            if result != game.iter:         # (avoids unwanted submission for clicking out of box)
                game.iter = eval(text)      # Sets the new iteration value
                game.targets_and_steps()

                # Plot new state
                game.graph_state()

        # anch_num textbox
        def anchbox(text):
            # Update State
            result = int(eval(text))
            if result != game.num and result > 0:   # (avoids unwanted submission for clicking out of box)
                game.num = result                   # Sets the new iteration value
                game.compute_anchors()              # Compute new anchors
                game.targets_and_steps()

                # Plot new state
                game.graph_state()

        # anch_num textbox
        def distbox(text):
            # Update State
            result = eval(text)
            if result != game.dist:                # (avoids unwanted submission for clicking out of box)
                if result > 2:
                    print("REFUSED: Solution diverges for large iterations. Disable for low iterations at your own risk.")
                else:
                    start = time.time()
                    game.dist = result                 # Sets the new iteration value
                    game.compute_steps()                # And the new steps
                    middle = time.time()

                # Plot new state
                game.graph_state()
                end = time.time()
                print("---------------------------")
                print(f"Compute:\t{middle-start:.4f}")
                print(f"Graphing:\t{end-middle:.4f}")
                print(f"Total Time:\t{end-start:.4f}")

        # Toggle Anchors Button
        def toggle_anchors(null):
            print("---------------------------")
            start = time.time()
            game.show_anchor = not game.show_anchor
            game.graph_state()
            end = time.time()
            print(f"Total (Graphing) Time:\t{end-start:.4f}")

        # Random Seed Button
        def rand_seed(null):
            start = time.time()
            middle1 = time.time()
            middle2 = time.time()
            game.targets_and_steps()
            middle3 = time.time()
            game.graph_state()
            end = time.time()
            print("-------------------------")
            print(f"Randomizer:\t{middle1-start:.4f}")
            print(f"Setting Box:\t{middle2-middle1:.4f}")
            print(f"Compute:\t{middle3-middle2:.4f}")
            print(f"Graphing:\t{end - middle3:.4f}")
            print(f"Total Time:\t{end-start:.4f}")

        # 1 Step Button
        def plus_one(null):
            game.iter += 1
            game.targets_and_steps()
            game.graph_state()

    ### Wiget Locations ###
    if True:    
        # Seedbox location
        sx_pos = 0.1; swidth = 0.08
        sy_pos = 0.0125; sheight = 0.05
        axbox = plt.axes([sx_pos, sy_pos, swidth, sheight])
        seed_box = TextBox(axbox, 'Seed: ', initial=f"{start_seed}")
        seed_box.on_submit(seedbox)

        # Iterbox location
        ix_pos = 0.35; iwidth = 0.1
        iy_pos = 0.0125; iheight = 0.05
        axbox = plt.axes([ix_pos, iy_pos, iwidth, iheight])
        iter_box = TextBox(axbox, 'Iterations: ', initial=f"{start_iter}")
        iter_box.on_submit(iterbox)

        # Anchbox location
        ax_pos = 0.6; awidth = 0.05
        ay_pos = 0.0125; aheight = 0.05
        axbox = plt.axes([ax_pos, ay_pos, awidth, aheight])
        anch_box = TextBox(axbox, 'Anchors: ', initial=f"{start_num}")
        anch_box.on_submit(anchbox)

        # Distbox location
        dx_pos = 0.8; dwidth = 0.08
        dy_pos = 0.0125; dheight = 0.05
        dxbox = plt.axes([dx_pos, dy_pos, dwidth, dheight])
        dist_box = TextBox(dxbox, 'Dist: ', initial=f"{start_dist}")
        dist_box.on_submit(distbox)

        # Toggle Anchors location
        tanch_x = 0.23; tanch_width = 0.175  
        tanch_y = 0.9; tanch_height = 0.05
        tanch_ax = plt.axes([tanch_x, tanch_y, tanch_width, tanch_height])
        tanch = Button(tanch_ax, "Hide Anchors")
        tanch.on_clicked(toggle_anchors)

        # Rand_Seedbox Location
        bx = 0.43; bwidth = 0.175  
        by = 0.9; bheight = 0.05
        bax = plt.axes([bx, by, bwidth, bheight])
        brand = Button(bax, "Random Seed")
        brand.on_clicked(rand_seed)

        # Plus 1 Location
        p_one_x = 0.63; p_one_width = 0.175  
        p_one_y = 0.9; p_one_height = 0.05
        p_one_ax = plt.axes([p_one_x, p_one_y, p_one_width, p_one_height])
        p_one = Button(p_one_ax, "1 Step")
        p_one.on_clicked(plus_one)

    # Invoke graphing funcs
    game.graph_state()
    plt.show()