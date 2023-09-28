import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.animation import FuncAnimation
import numpy as np
from smooth_func import smooth
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
    def graph_state(self):
        ax.clear()
        ax.scatter(self.x, self.y, color=colormap[self.choice], s=3)    # Implement button to toggle colormap (esp for high pow_2)
        if self.show_anchor:
            ax.scatter(self.x_anchors,self.y_anchors, color='k', s=5)       # Implement button to toggle this for high pow_2
        plt.draw()

##### Inintial State #####
start_num = 3
start_dist = 0.5
start_iter = 10000
start_seed = 3170
game = GameRules(num_anchors=start_num, dist = start_dist, iter=start_iter, seed=start_seed)

##### Matplotlib Setup #####
fig = plt.figure(figsize=(32,24))   # Increased Size for Animation Prints
ax = fig.add_subplot()

# (Colormap Initialization)
nice_colors = np.array(
    [[0.75,0,0],[0,0.75,0],[0,0,0.75],
    [0.75,0.75,0],[0.75,0,0.75],[0,0.75,0.75]])
rand_colors = np.random.random(size=(500,3)).round(1)           # Arbitrary dimension of 500, increase if you ever do anchors > 500.
colormap = np.concatenate((nice_colors,rand_colors),axis=0)

### Widget functions ###

# Seed-setting Textbox
def seedbox(text):
    # Update State
    result = eval(text)
    if result != game.seed:     # (avoids unwanted submission for clicking out of box)
        game.set_seed(result)   # Sets the new seed
        game.compute_targets()  # Computes anchor selection based on seed
        game.compute_steps()    # Computes new (x,y) positions given the anchor selection sequence

    # Plot new state
    game.graph_state()

# Iter-setting Textbox
def iterbox(text):
    # Update State
    result = eval(text)
    if result != game.iter:         # (avoids unwanted submission for clicking out of box)
        game.iter = eval(text)      # Sets the new iteration value
        game.set_seed(game.seed)    # Gotta reset this, that's annoying
        game.compute_targets()      # Computes new targets
        game.compute_steps()        # And the new steps

        # Plot new state
        game.graph_state()

# anch_num textbox
def anchbox(text):
    # Update State
    result = int(eval(text))
    if result != game.num and result > 0:   # (avoids unwanted submission for clicking out of box)
        game.num = result                   # Sets the new iteration value
        game.set_seed(game.seed)            # Gotta reset this, that's annoying
        game.compute_anchors()              # Compute new anchors
        game.compute_targets()              # Computes new targets
        game.compute_steps()                # And the new steps

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
            game.dist = result                 # Sets the new iteration value
            game.set_seed(game.seed)            # Gotta reset this, that's annoying
            game.compute_steps()                # And the new steps

        # Plot new state
        game.graph_state()

# Toggle Anchors Button
def toggle_anchors(null):
    if game.show_anchor:
        game.show_anchor = False
    else: game.show_anchor = True
    
    game.graph_state()

# Random Seed Button
def rand_seed(null):
    game.set_seed(np.random.randint(10000))
    seed_box.set_val(game.seed)
    game.compute_targets()
    game.compute_steps()
    game.graph_state()

# 1 Step Button
def plus_one(null):
    game.iter += 1
    game.set_seed(game.seed)
    game.compute_targets()
    game.compute_steps()
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


# Generation of frames for animation purposes
ax.autoscale(False)
game.show_anchor=False                  # needed for scalable view
null,dist_vals = smooth(0.000002,0,201) # varying distance values
# dist_vals = dist_vals.round(9)        # Avoid floating point error
i = 0
for dist in dist_vals:
    game.dist = dist
    dist_box.set_val(dist)
    game.compute_steps()
    game.graph_state()
    plt.savefig(f"/Volumes/ABT/filedump/000002_0_201/{i}.png")
    i += 1
