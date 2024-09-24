import numpy as np
import time






# create large array
n = 100000000
start = time.time()
myArray = np.random.randint(0,10000,size=n)
end = time.time()
print(f"Array creation {end - start}")
start = time.time()
myArray = myArray % 7
end = time.time()
print(f"Array modulo operation {end - start}")
