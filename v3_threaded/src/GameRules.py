import numpy as np
import ctypes
from Grapher import MyGrapher

class Game():
    # Update seed value
    def set_seed(self, seed):
        self.seed = seed                # update class variable
        self.cset_seed(seed) # update c seed

    def __init__(
        self,
        num_anchors,
        dist,
        iter,
        seed,
        resX,
        resY,
        num_threads,
        show_anchors=True):

        ## Load C Library and set function footprints ##
        self.get_functions()
        self.set_footprints()

        ## Game-based variables ##
        self.num_anchors = num_anchors
        self.iter = iter
        self.dist = dist
        self.set_seed(seed)
        self.show_anchors = show_anchors
        self.num_threads = num_threads

        # CFunction Parameters
        self.startX = 0.
        self.startY = 0.
        self.resX = resX
        self.resY = resY

        ### Game Setup ###
        ## Anchors ##
        self.compute_anchors()      # Python list   

        ## Targets ##
        self.set_target_array()     # Create memory object
        self.compute_targets()      # Do the computations

        ## Steps ##
        self.set_steps_arrays()     # Create memory object
        self.compute_steps()        # Do the computations

        ## Screen ##
        self.set_screen_arrays()    # Pixel array for steps and anchors
        self.fit_to_screen()        # Transform to screen coordinates
        self.set_screen()           # Create heatmap (1D)

    ### C shared library initialization ###
    def get_functions(self):
        ## Get functions from shared library ##
        self.compute_lib = ctypes.cdll.LoadLibrary('./v3/bin/RandomCompute.so')
        self.ccompute_targets = self.compute_lib.compute_targets
        self.ccompute_steps = self.compute_lib.compute_steps
        self.ccompute_bounds = self.compute_lib.compute_bounds
        self.cset_seed = self.compute_lib.set_seed
        self.cset_screen = self.compute_lib.set_screen
        self.cfit_to_screen = self.compute_lib.fit_to_screen

    def set_footprints(self):
        # set_seed
        self.cset_seed.argtypes = [ctypes.c_int]
        self.cset_seed.restype = None

        # set_screen
        self.cset_screen.argtypes = [
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # screen
            ctypes.c_int,                                                       # resX
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # pixelX
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # pixelY
            ctypes.c_int                                                        # size
        ]
        self.cset_screen.restype = None

        # fit_to_screen
        self.cfit_to_screen.argtypes = [
            ctypes.c_int,                                                       # size
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsX
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsY
            ctypes.c_double,                                                    # minX
            ctypes.c_double,                                                    # maxX
            ctypes.c_double,                                                    # minY
            ctypes.c_double,                                                    # maxY
            ctypes.c_int,                                                       # resX
            ctypes.c_int,                                                       # resY
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # pixelX
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # pixelY
        ]
        self.cfit_to_screen.restype = None

        # compute_targets
        self.ccompute_targets.argtypes = [
            ctypes.c_int,                                                       # size
            ctypes.c_int,                                                       # num_anchors
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS')        # targets
        ]
        self.ccompute_targets.restype = None

        # compute_steps
        self.ccompute_steps.argtypes = [
            ctypes.c_int,                                                       # iter
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # anchorX
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # anchorY
            np.ctypeslib.ndpointer(dtype=np.int32, flags='C_CONTIGUOUS'),       # target
            ctypes.c_double,                                                    # distFactor
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsX
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsY
        ]
        self.ccompute_steps.restype = None

        # compute_bounds
        self.ccompute_bounds.argtypes = [
            ctypes.POINTER(ctypes.c_double),    # minX
            ctypes.POINTER(ctypes.c_double),    # maxX
            ctypes.POINTER(ctypes.c_double),    # minY
            ctypes.POINTER(ctypes.c_double),    # maxY
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsX
            np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS'),     # stepsY
            ctypes.c_int    # length of steps array
        ]
        self.ccompute_bounds.restype = None

    ### Target Functions ###

    def set_target_array(self):
        self.targets = np.ndarray(shape=(self.iter), dtype=np.int32)

    def compute_targets(self):
        # when threaded, this will need to pass a specific indexed start for self.targets.
        self.cset_seed(self.seed)
        self.ccompute_targets(ctypes.c_int(self.iter), 
                                ctypes.c_int(self.num_anchors), 
                                self.targets)

    ### Anchor Functions ###
    def compute_anchors(self):
        # Compute polar angle for each target
        angle = [np.pi * (1/2 + 2*i/self.num_anchors) for i in range(self.num_anchors)]
        angle = np.array(angle)

        # Distribute r=1 polygon vertices
        self.x_anchors = np.array(np.cos(angle), dtype=np.double)   
        self.y_anchors = np.array(np.sin(angle), dtype=np.double)

        # This has world coordinates. I'll leave the translation to screen coordinates to the screen functions.

    ### Steps Functions ###

    def create_steps_array(self):
        ## create mem obj based on iteration size
        self.steps_X = np.ndarray(shape=(self.iter * self.num_threads), dtype=np.double)
        self.steps_Y = np.ndarray(shape=(self.iter * self.num_threads), dtype=np.double)

    def set_start_position(self):
        # traverse master position block; index based on thread number
        for i in range(self.num_threads):
            index = i * self.iter
            self.steps_X[index] = self.startX
            self.steps_Y[index] = self.startY

    def set_steps_arrays(self):
        self.create_steps_array()   # create master position segment
        self.set_start_position()   # apply self.startX/Y to each thread's position segment

    def compute_steps(self):
        # Set seed
        self.cset_seed(self.seed)

        # Compute steps
        # per thread, this means passing specific starting indices for steps_X
        self.ccompute_steps(
            ctypes.c_int(self.iter),
            self.x_anchors,
            self.y_anchors,
            self.targets,
            ctypes.c_double(self.dist),
            self.steps_X,
            self.steps_Y
        )
        


    # Should this be migrated to the graphing module?
   

    ### Screen Functions ###

    def compute_graphical_bounds(self):
        # initialize
        self.minX = ctypes.c_double(self.startX)
        self.maxX = ctypes.c_double(self.startX)
        self.minY = ctypes.c_double(self.startY)
        self.maxY = ctypes.c_double(self.startY)
        # update bounds for graphing pieces
        self.ccompute_bounds(
            ctypes.byref(self.minX),
            ctypes.byref(self.maxX),
            ctypes.byref(self.minY),
            ctypes.byref(self.maxY),
            self.steps_X,
            self.steps_Y,
            self.iter) # might need to update this to reflect threads

    def fit_to_screen(self):
        self.cfit_to_screen(
            ctypes.c_int(self.iter),
            self.steps_X,
            self.steps_Y,
            self.minX,
            self.maxX,
            self.minY,
            self.maxY,
            ctypes.c_int(self.resX),
            ctypes.c_int(self.resY),
            self.pixel_X,
            self.pixel_Y)
        
    def set_screen_arrays(self):
        self.pixel_X = np.ndarray(shape=(self.iter + self.num_anchors),dtype=np.int32)  # Don't forget that we're graphing out the polygon vertices too
        self.pixel_Y = np.ndarray(shape=(self.iter + self.num_anchors),dtype=np.int32)  # ^
        self.screen = np.zeros(shape=(self.resX * self.resY),dtype=np.int32)

    def set_screen(self):
        self.cset_screen(
            self.screen,
            ctypes.c_int(self.resX),
            self.pixel_X,
            self.pixel_Y,
            ctypes.c_int(self.iter))