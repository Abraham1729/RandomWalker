import ctypes

### Loading the shared library for future function calls ###
compute_lib = ctypes.CDLL('./shared_compute.so')


### Defining library function signiture ###
# Combined function (fewer loop iterations)
compute_lib.targets_and_steps.argtypes = [ctypes.c_int,                  # num_points        int
                                      ctypes.POINTER(ctypes.c_int),     # target            double array
                                      ctypes.c_double,                  # distance_factor   double
                                      ctypes.POINTER(ctypes.c_double),  # stepsX            double array
                                      ctypes.POINTER(ctypes.c_double),  # stepsY            double array
                                      ctypes.c_int,                     # num_anchors       int
                                      ctypes.POINTER(ctypes.c_double),  # anchorX           double array
                                      ctypes.POINTER(ctypes.c_double)]  # anchorY           double array
compute_lib.targets_and_steps.restype = None                                # void

# Compute Targets
compute_lib.compute_targets.argtypes = [ctypes.c_int,                       # num_points
                                        ctypes.c_int,                       # num_anchors 
                                        ctypes.POINTER(ctypes.c_int)]       # target
compute_lib.compute_targets.restype = None

# Compute Steps
compute_lib.compute_steps.argtypes = [ctypes.c_int,                     # num_points        int
                                      ctypes.POINTER(ctypes.c_int),     # target            double array
                                      ctypes.c_double,                  # distance_factor   double
                                      ctypes.POINTER(ctypes.c_double),  # stepsX            double array
                                      ctypes.POINTER(ctypes.c_double),  # stepsY            double array
                                      ctypes.c_int,                     # num_anchors       int
                                      ctypes.POINTER(ctypes.c_double),  # anchorX           double array
                                      ctypes.POINTER(ctypes.c_double)]  # anchorY           double array
compute_lib.compute_steps.restype = None


### Defining inputs for c function ###
num_points = 1000000            # actual implementation: defined in class 
distance_factor = 0.5           # actual implementation: defined in class

# Target and Steps arrays creation
c_targets = (ctypes.c_int * num_points)()
c_stepsX = (ctypes.c_double * num_points)()
c_stepsY = (ctypes.c_double * num_points)()
print(c_stepsY == c_stepsX)

# Hard coding example anchors
num_anchors = 3
anchorsX = [-1.0, 0.0, 1.0]
anchorsY = [0.0, 1.5, 0.0]

# Converting to c_type arrays
c_anchorX = (ctypes.c_double * len(anchorsX))(*anchorsX)
c_anchorY = (ctypes.c_double * len(anchorsY))(*anchorsY)


### Invoking C function ###
compute_lib.targets_and_steps(num_points, c_targets, distance_factor, c_stepsX, c_stepsY, num_anchors, c_anchorX, c_anchorY)

### Spot check the array ###
print("Checking array contents:")
print("------------------------")
print(f"{c_stepsX[0]}\t{c_stepsY[0]}")
print(f"{c_stepsX[1]}\t{c_stepsY[1]}")
print(f"{c_stepsX[2]}\t{c_stepsY[2]}")
print(f"{c_stepsX[-1]:.4f}\t{c_stepsY[-1]:.4f}")
print(f"{c_stepsX[-2]:.4f}\t{c_stepsY[-2]:.4f}")
print(f"{c_stepsX[-3]:.4f}\t{c_stepsY[-3]:.4f}")