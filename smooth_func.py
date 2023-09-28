from matplotlib import pyplot as plt
import numpy as np

def smooth(a,b,num):
    '''
    Sigmoid-like distribution of values in domain [a,b] using num points.
    '''
    middle = int(num/2)
    x = np.linspace(a,b,num)
    y1 = 2 * (1 / (b-a)) ** 2 * (x[:middle] - a)**2
    y2 = -2 * (1 / (b-a))** 2 * (x[middle:] - b)**2 + 1
    y = np.concatenate((y1,y2))
    y = (b-a)*y + a
    return x,y

if __name__ == '__main__':
    # Graphically verifying results
    fig = plt.figure(figsize=(8,6))   # default figsize (6.4,4.8) width height
    ax = fig.add_subplot()
    x,y = smooth(2,1.9,201)
    # y = y.round(1)
    ax.scatter(x,y,s=1)
    plt.show()