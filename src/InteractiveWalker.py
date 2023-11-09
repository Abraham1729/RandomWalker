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
    ## Compute Targets Footprint ##
    compute_lib.compute_targets.argtypes = [
        ctypes.c_int,                       # iterations        int
        ctypes.c_int,                       # num_anchors       int
        ctypes.POINTER(ctypes.c_int)]       # targets           int*
    compute_lib.compute_targets.restype = None

    ## Compute Steps Footprint ##
    compute_lib.compute_steps.argtypes = [
        ctypes.c_int,                       # iterations        int
        ctypes.c_double,                    # distance_factor   double
        ctypes.c_double,                    # startX            double
        ctypes.c_double,                    # startY            double
        ctypes.c_int,                       # num_anchors       int
        ctypes.POINTER(ctypes.c_double),    # anchorX           double*
        ctypes.POINTER(ctypes.c_double),    # anchorY           double*
        ctypes.POINTER(ctypes.c_int),       # target            int*
        ctypes.c_int,                       # resX              int
        ctypes.c_int,                       # resY              int
        ctypes.POINTER(ctypes.c_double),    # stepsX            double*
        ctypes.POINTER(ctypes.c_double),    # stepsY            double*
        ctypes.POINTER(ctypes.c_int),       # pixelX            int*
        ctypes.POINTER(ctypes.c_int),       # pixelY            int*
        ctypes.c_double,                    # minX            double
        ctypes.c_double,                    # maxX            double
        ctypes.c_double,                    # minY            double
        ctypes.c_double,                    # maxY            double
    ]
    compute_lib.compute_steps.restype = None

    # Setting seed for c program:
    compute_lib.set_seed.argtypes = [ctypes.c_int]
    compute_lib.set_seed.restype = None

    # Setting Screen
    compute_lib.set_screen.argtypes = [
        ctypes.POINTER(ctypes.c_int),       # screen            int*
        ctypes.c_int,                       # resX              int
        ctypes.POINTER(ctypes.c_int),       # pixelX            int*
        ctypes.POINTER(ctypes.c_int),       # pixelY            int*
        ctypes.c_int                       # size              int
    ]
    compute_lib.set_screen.restype = None

    # Fitting steps to screen
    compute_lib.fit_to_screen.argtypes = [
        ctypes.POINTER(ctypes.c_double),    # stepsX            double*
        ctypes.POINTER(ctypes.c_double),    # stepsY            double*
        ctypes.POINTER(ctypes.c_int),       # pixelX            int*
        ctypes.POINTER(ctypes.c_int),       # pixelY            int*
        ctypes.c_int,                       # resX              int
        ctypes.c_int,                       # resY              int
        ctypes.c_double,                    # minX            double
        ctypes.c_double,                    # maxX            double
        ctypes.c_double,                    # minY            double
        ctypes.c_double,                    # maxY            double
        ctypes.c_int,                       # size              int
    ]
    compute_lib.fit_to_screen.restype = None

    # Update seed value
    def set_seed(self, seed):
        self.seed = seed                # update class variable
        self.compute_lib.set_seed(seed) # update c seed

    def __init__(
        self,
        num_anchors,
        dist,
        iter,
        seed,
        resX,
        resY):

        ## Computational attributes/methods
        self.num_anchors = num_anchors
        self.iter = iter
        self.dist = dist
        self.set_seed(seed)

        # Variables for functions
        self.startX = ctypes.c_double(0.)
        self.startY = ctypes.c_double(0.)
        self.resX = ctypes.c_int(resX)
        self.resY = ctypes.c_int(resY)
        self.minX = self.startX
        self.maxX = self.startX
        self.minY = self.startY
        self.maxY = self.startY
        
        # Initial State Computations
        self.compute_anchors()      # Computers anchors in Python list)
        self.targets_and_steps()    # Compute targets and steps with C funciton

    ## CType Computation Functions
    def targets_and_steps(self):
        # Reset C seed:
        self.compute_lib.set_seed(self.seed)

        ## Compute targets
        self.targets = (ctypes.c_int * self.iter)()
        self.compute_lib.compute_targets(self.iter, self.num_anchors, self.targets)

        # print(self.resX.value * self.resY)
        ## Set up necessary ctype input
        self.screen = (ctypes.c_int * (self.resX.value * self.resY.value))()
        self.csteps_X = (ctypes.c_double * self.iter)()
        self.csteps_Y = (ctypes.c_double * self.iter)()
        self.cpixel_X = (ctypes.c_int * self.resX.value)()
        self.cpixel_Y = (ctypes.c_int * self.resY.value)()
        ## Compute Steps
        self.compute_lib.compute_steps(
            self.iter,          # int
            self.dist,          # double
            self.startX,        # double
            self.startY,        # double
            self.num_anchors,   # int
            self.cx_anchors,    # double*
            self.cy_anchors,    # double* 
            self.targets,       # int*
            self.resX,          # int
            self.resY,          # int
            self.csteps_X,
            self.csteps_Y,
            self.cpixel_X,
            self.cpixel_Y,
            self.minX,
            self.maxX,
            self.minY,
            self.maxY)
        
        print("Computed steps!")
        print("Doing screen management!")
        self.fit_to_screen()
        self.set_screen()

        print(type(self.screen))
        sum = 0
        for i in self.screen:
            print(i)
            sum += i
        print(f"Sum = {sum}")
        print(f"Accessing end of screen: {self.screen[resX*resY - 1]}")

    def compute_anchors(self):
        # populate python lists
        self.x_anchors = []
        self.y_anchors = []
        #** I want to add functionality for adjusting the angle with a widget **#
        angle = np.pi / 2   

        for i in range(self.num_anchors):
            self.x_anchors.append(np.cos(angle))
            self.y_anchors.append(np.sin(angle))
            angle += 2*np.pi/self.num_anchors

        # allocate memory for ctypes double array, populate with data from python lists
        self.cx_anchors = (ctypes.c_double * self.num_anchors)(*self.x_anchors)
        self.cy_anchors = (ctypes.c_double * self.num_anchors)(*self.y_anchors)

    def compute_steps(self):
        ## Set up necessary ctype input
        self.screen = (ctypes.c_int * (self.resX * self.resY))()
        self.csteps_X = (ctypes.c_double * self.iter)()
        self.csteps_Y = (ctypes.c_double * self.iter)()
        self.cpixel_X = (ctypes.c_int * self.resX)()
        self.cpixel_Y = (ctypes.c_int * self.resY)()

        ## Compute with C library; rerturns void, modifies step arrays.
        self.compute_lib.compute_steps(
            self.iter,          # int
            self.dist,          # double
            self.startX,        # double
            self.startY,        # double
            self.num_anchors,   # int
            self.cx_anchors,    # double*
            self.cy_anchors,    # double*
            self.targets,       # int*
            self.resX,          # int
            self.resY,          # int
            self.csteps_X,
            self.csteps_Y,
            self.cpixel_X,
            self.cpixel_Y)

    def fit_to_screen(self):
        print("Starting fit_to_screen")
        print(type(self.maxX))
        self.compute_lib.fit_to_screen(
            self.csteps_X,
            self.csteps_Y,
            self.cpixel_X,
            self.cpixel_Y,
            self.resX,
            self.resY,
            self.minX,
            self.maxX,
            self.minY,
            self.maxY,
            self.iter)
        print("Done fit_to_screen")

def set_screen(self):
    print("Starting set_screen")
    self.compute_lib.set_screen(
            self.screen,        # int*
            self.resX,          # int
            self.cpixel_X,      
            self.cpixel_Y,
            self.iter)
    print("Done set_screen")

    def screen_management(self):
        self.fit_to_screen()
        self.set_screen()

    


if __name__ == "__main__":
    ##### Inintial State #####
    start_num = 3
    start_dist = 0.5
    start_iter = 100000
    start_seed = 3170
    resX = 4
    resY = 4

    ## Testing possibility of reshaping with numpy
    # compute_lib = ctypes.CDLL('./RandomCompute.so')
    # compute_lib.compute_targets.argtypes = [
    #     ctypes.c_int,                       # iterations        int
    #     ctypes.c_int]                       # num_anchors       int
    # compute_lib.compute_targets.restype = ctypes.POINTER(ctypes.c_int) # returns targets choice int array
    # foo = compute_lib.compute_targets(start_iter, start_num)
    # foo = np.ctypeslib.as_array(foo, (50,2))
    # print(foo.size)
    # print(foo.shape)
    # print(foo[49,1])

    game = GameRules(num_anchors=start_num, 
                     dist = start_dist, 
                     iter=start_iter, 
                     seed=start_seed,
                     resX=resX,
                     resY=resY)
    print("End of program")

    # ### Instantiate a Grapher (Comes with Widgets) ###
    # myGrapher = MyGrapher(game,
    #                       show_colors=False,
    #                       show_anchors=True,
    #                       scaling=1.125,
    #                       xDim=14,
    #                       yDim=9,
    #                       alpha=0.025)
    # myGrapher.graph_state()
    # myGrapher.show_fig()
    # # myGrapher.save(dpi=1000)
