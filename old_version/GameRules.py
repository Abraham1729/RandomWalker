import numpy as np
class GameRules():
    def __init__(self,num_anchors,dist,iter,seed):
        # Computational attributes/methods
        self.num = num_anchors
        self.iter = iter
        self.dist = dist
        self.set_seed(seed)     # sets self.seed, informs np.random module
        self.compute_anchors()  # sets self.x/y_anchors
        self.compute_targets()  # sets self.choice
        self.compute_steps()    # sets self.x/y data

        # Graphing-specific attributes/methods
        self.show_anchor = True # Toggling anchor display

    # Update seed value
    def set_seed(self, seed):
        self.seed = seed
        np.random.seed(seed)

    # Computing anchor point positions
    def compute_anchors(self):
        self.x_anchors = []
        self.y_anchors = []
        angle = np.pi / 2

        for i in range(self.num):
            self.x_anchors.append(np.cos(angle))
            self.y_anchors.append(np.sin(angle))
            angle += 2*np.pi/self.num

    # Compute the target vector for determining new positions
    def compute_targets(self):
        self.choice = np.random.randint(0,self.num, size = self.iter+1)

    # Compute the (x,y) data for the current game run
    def compute_steps(self):
        self.x = np.zeros(self.iter+1)
        self.y = np.zeros(self.iter+1)

        for i in range(1,self.iter+1):
            self.x[i] = (self.x[i-1] + (self.x_anchors[self.choice[i]] - self.x[i-1]) * (self.dist))
            self.y[i] = (self.y[i-1] + (self.y_anchors[self.choice[i]] - self.y[i-1]) * (self.dist))

    # Plot it
    # def graph_state(self):
    #     ax.clear()
    #     ax.scatter(self.x, self.y, color=colormap[self.choice], s=3)    # Implement button to toggle colormap (esp for high pow_2)
    #     if self.show_anchor:
    #         ax.scatter(self.x_anchors,self.y_anchors, color='k', s=5)       # Implement button to toggle this for high pow_2
    #     plt.draw()