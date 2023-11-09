import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button
import time

class MyGrapher():

    def __init__(self, game, show_anchors=True, show_colors=False, 
                 scaling=3, xDim=1, yDim=1, alpha=0.1):
        '''
        Takes in instance of GameRules in order to call relevant methods for widget functionality.
        Sets locations of all wigets.
        '''
        self.game = game
        self.show_anchors = show_anchors    # toggle anchor display
        self.show_colors = show_colors      # toggle anchor-based point colors
        self.xDim = xDim
        self.yDim = yDim
        self.alpha = alpha

        # Disable toolbar
        # plt.rcParams['toolbar'] = 'None'

        ### Defining Fig and Ax (Ordering in Code is important here) ###
        self.fig1 = plt.figure(figsize=(self.xDim*scaling,self.yDim*scaling)) # default figsize (6.4,4.8) width height
        self.ax1 = self.fig1.add_subplot()
        self.fig1.subplots_adjust(left=0, right=1, top=1, bottom=0)


        ##### Widget Figure #####
        self.fig2 = plt.figure(figsize=(5,1))
        self.ax2 = self.fig2.add_subplot()
        self.fig2.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # SeedBox location #
        sx_pos = 0.1; swidth = 0.08
        sy_pos = 0.0125; sheight = 0.25
        axbox = plt.axes([sx_pos, sy_pos, swidth, sheight])
        self.seed_box = TextBox(axbox, 'Seed: ', initial=f"{self.game.seed}")
        self.seed_box.on_submit(self.seedbox)

        # iterBox location #
        ix_pos = 0.35; iwidth = 0.1
        iy_pos = 0.0125; iheight = 0.25
        axbox = plt.axes([ix_pos, iy_pos, iwidth, iheight])
        self.iter_box = TextBox(axbox, 'Iterations: ', initial=f"{self.game.iter}")
        self.iter_box.on_submit(self.iterBox)

        # anchBox location #
        ax_pos = 0.6; awidth = 0.05
        ay_pos = 0.0125; aheight = 0.25
        axbox = plt.axes([ax_pos, ay_pos, awidth, aheight])
        self.anch_text = TextBox(axbox, 'Anchors: ', initial=f"{self.game.num_anchors}")
        self.anch_text.on_submit(self.anchBox)

        # distBox location #
        dx_pos = 0.8; dwidth = 0.08
        dy_pos = 0.0125; dheight = 0.25
        axbox = plt.axes([dx_pos, dy_pos, dwidth, dheight])
        self.dist_box = TextBox(axbox, 'Dist: ', initial=f"{self.game.dist}")
        self.dist_box.on_submit(self.distBox)

        # alpha_box location #
        alphaX_pos = 0.1; alphaWidth = 0.08
        alphaY_pos = 0.7; alphaHeight = 0.25
        axbox = plt.axes([alphaX_pos, alphaY_pos, alphaWidth, alphaHeight])
        self.alpha_box = TextBox(axbox, 'Alpha: ', initial=f"{self.alpha}")
        self.alpha_box.on_submit(self.alphaBox)

        # Toggle Color location #
        color_box_x = 0.23; color_box_width = 0.15  
        color_box_y = 0.7; color_box_height = 0.25
        color_box_ax = plt.axes([color_box_x, color_box_y, color_box_width, color_box_height])
        self.color_box = Button(color_box_ax, "Toggle Colors")
        self.color_box.on_clicked(self.toggle_color)

        # Toggle Anchors location #
        anch_box_x = 0.53; anch_box_width = 0.15  
        anch_box_y = 0.7; anch_box_height = 0.25
        anch_box_ax = plt.axes([anch_box_x, anch_box_y, anch_box_width, anch_box_height])
        self.anch_box = Button(anch_box_ax, "Toggle Anchors")
        self.anch_box.on_clicked(self.toggle_anchors)

        # Rand_Seedbox Location #
        bx = 0.83; bwidth = 0.15  
        by = 0.7; bheight = 0.25
        bax = plt.axes([bx, by, bwidth, bheight])
        self.rand_box = Button(bax, "Random Seed")
        self.rand_box.on_clicked(self.rand_seed)

        ##### Colormap Setup #####

        nice_colors = np.array(
            [[0.75,0,0],
            [0,0.75,0],
            [0,0,0.75],
            [0.75,0.75,0],
            [0.75,0,0.75],
            [0,0.75,0.75]])
        rand_colors = np.random.random(size=(500,3)).round(1)           # Arbitrary dimension of 500, increase if you ever do anchors > 500.
        self.colormap = np.concatenate((nice_colors,rand_colors),axis=0)

        self.graph_state()

    ##### Widget Functions #####
    # # Seed-setting Textbox
    def seedbox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.seed:     # (avoids unwanted submission for clicking out of box)
            self.game.set_seed(result)   # Sets the new seed
            self.game.targets_and_steps()

        # Plot new state
        self.graph_state()

    # Iter-setting Textbox
    def iterBox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.iter:         # (avoids unwanted submission for clicking out of box)
            self.game.iter = eval(text)      # Sets the new iteration value
            self.game.targets_and_steps()

            # Plot new state
            self.graph_state()

    # anchBox textbox
    def anchBox(self,text):
        # Update State
        result = int(eval(text))
        if result != self.game.num_anchors and result > 0:   # (avoids unwanted submission for clicking out of box)
            self.game.num_anchors = result                   # Sets the new iteration value
            self.game.compute_anchors()              # Compute new anchors
            self.game.targets_and_steps()

            # Plot new state
            self.graph_state()

    # distBox textbox
    def distBox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.dist:                # (avoids unwanted submission for clicking out of box)
            if result > 2:
                print("REFUSED: Solution diverges for large iterations. Disable for low iterations at your own risk.")
            else:
                self.game.dist = result                 # Sets the new iteration value
                self.game.compute_steps()                # And the new steps

            # Plot new state
            self.graph_state()
  
    # alphaBox textbox
    def alphaBox(self,text):
        result = eval(text)
        if result != self.alpha:
            self.alpha = result
            self.graph_state()

    # Toggle Anchors Button
    def toggle_anchors(self, null):
        self.show_anchors = not self.show_anchors
        self.graph_state()

    def toggle_color(self, null):
        self.show_colors = not self.show_colors
        self.graph_state()

    # Random Seed Button
    def rand_seed(self, null):
        self.game.set_seed(np.random.randint(0,10000))
        self.game.targets_and_steps()
        self.graph_state()
        self.seed_box.set_val(self.game.seed)

    ### Display it ###
    def graph_state(self):
        self.ax1.clear()

        # Determine the colors being used for graphing
        if self.show_colors:
            self.ax1.scatter(self.game.c_stepsX, self.game.c_stepsY, color=self.colormap[self.game.c_targets], s=1)
            self.ax1.set_facecolor("white")
        else:
            start = time.time()
            spotColor = [0.9975,0,0,self.alpha]
            self.ax1.scatter(self.game.c_stepsX, self.game.c_stepsY, color=spotColor, s=.1)
            self.ax1.set_facecolor([0,0,0])


        if self.show_anchors:
            self.ax1.scatter(self.game.x_anchors,self.game.y_anchors, color='k', s=5)

        plt.draw()
        self.fig1.canvas.draw_idle()

    def show_fig(self):
        plt.show()


    def save(self, dpi):
        plt.savefig("./foo.png", dpi=dpi)
