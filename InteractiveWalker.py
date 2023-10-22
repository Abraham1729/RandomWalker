import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
# from matplotlib.widgets import TextBox, Button
from matplotlib.animation import FuncAnimation
import numpy as np
import ctypes
from Grapher import MyGrapher

class GameRules():
    # C shared library
    compute_lib = ctypes.CDLL('./RandomCompute.so')

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

    # Setting seed for c program:
    compute_lib.set_seed.argtypes = [ctypes.c_int]
    compute_lib.set_seed.restype = None

    def __init__(self,num_anchors,dist,iter,seed):
        ## Computational attributes/methods
        self.num_anchors = num_anchors
        self.iter = iter
        self.dist = dist
        self.set_seed(seed)
        
        # Initial State Computations
        self.compute_anchors()  # Computers anchors in Python list
        self.targets_and_steps()# Compute targets and steps with C funciton

        ## Graphing-specific attributes/methods
        self.show_anchor = True # Toggling anchor display

    ## CType Memory Management Functions
    def set_c_anchors(self):
        # Can also be used to free / reinitialize
        self.cx_anchors = (ctypes.c_double * self.num_anchors)(*self.x_anchors)
        self.cy_anchors = (ctypes.c_double * self.num_anchors)(*self.y_anchors)

    def set_c_targets(self):
        # Can also be used to free / reinitialize
        self.c_targets = (ctypes.c_int * self.iter)()

    def set_c_steps(self):
        # Can also be used to free / reinitialize
        self.c_stepsX = (ctypes.c_double * self.iter)()
        self.c_stepsY = (ctypes.c_double * self.iter)()

    ## CType Computation Functions
    def targets_and_steps(self):
        # Reset C seed:
        self.compute_lib.set_seed(self.seed)

        ## Set up necessary ctype inputs
        self.set_c_targets()  # redundant on the first call of this function
        self.set_c_steps()    # same here -- redundant for first call

        ## Compute with C library: returns void, modifies target and step arrays.
        self.compute_lib.targets_and_steps(self.iter,
                                           self.c_targets,
                                           self.dist,
                                           self.c_stepsX,
                                           self.c_stepsY,
                                           self.num_anchors,
                                           self.cx_anchors,
                                           self.cy_anchors)

    def compute_anchors(self):
        self.x_anchors = []
        self.y_anchors = []
        angle = np.pi / 2       # Should I add functionality for adjusting the angle?

        for i in range(self.num_anchors):
            self.x_anchors.append(np.cos(angle))
            self.y_anchors.append(np.sin(angle))
            angle += 2*np.pi/self.num_anchors

        self.set_c_anchors()

    def compute_steps(self):
        ## Set up necessary ctype input
        self.set_c_steps()

        ## Compute with C library; rerturns void, modifies step arrays.
        self.compute_lib.compute_steps(self.iter,
                                       self.c_targets,
                                       self.dist,
                                       self.c_stepsX,
                                       self.c_stepsY,
                                       self.num_anchors,
                                       self.cx_anchors,
                                       self.cy_anchors)

    # Update seed value
    def set_seed(self, seed):
        self.seed = seed                # update class variable
        self.compute_lib.set_seed(seed) # update c seed


if __name__ == "__main__":
    ##### Inintial State #####
    start_num = 3
    start_dist = 0.5
    start_iter = 10000
    start_seed = 3170
    game = GameRules(num_anchors=start_num, dist = start_dist, iter=start_iter, seed=start_seed)

    ### Instantiate a Grapher (Comes with Widgets) ###
    myGrapher = MyGrapher(game)
    myGrapher.graph_state()
