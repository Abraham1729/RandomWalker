import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button

class MyGrapher():

    def __init__(self, game):
        '''
        Takes in instance of GameRules in order to call relevant methods for widget functionality.
        Sets locations of all wigets.
        '''
        self.game = game

        ### Defining Fig and Ax (Ordering in Code is important here) ###
        scaling = 3
        self.fig = plt.figure(figsize=(4*scaling,3*scaling)) # default figsize (6.4,4.8) width height
        self.ax = self.fig.add_subplot()

        ##### Widget Locations #####
        # Seedbox location #
        sx_pos = 0.1; swidth = 0.08
        sy_pos = 0.0125; sheight = 0.05
        axbox = plt.axes([sx_pos, sy_pos, swidth, sheight])
        self.seed_box = TextBox(axbox, 'Seed: ', initial=f"{self.game.seed}")
        self.seed_box.on_submit(self.seedbox)

        # Iterbox location #
        ix_pos = 0.35; iwidth = 0.1
        iy_pos = 0.0125; iheight = 0.05
        axbox = plt.axes([ix_pos, iy_pos, iwidth, iheight])
        self.iter_box = TextBox(axbox, 'Iterations: ', initial=f"{self.game.iter}")
        self.iter_box.on_submit(self.iterbox)

        # Anchbox location #
        ax_pos = 0.6; awidth = 0.05
        ay_pos = 0.0125; aheight = 0.05
        axbox = plt.axes([ax_pos, ay_pos, awidth, aheight])
        self.anch_box = TextBox(axbox, 'Anchors: ', initial=f"{self.game.num_anchors}")
        self.anch_box.on_submit(self.anchbox)

        # Distbox location #
        dx_pos = 0.8; dwidth = 0.08
        dy_pos = 0.0125; dheight = 0.05
        axbox = plt.axes([dx_pos, dy_pos, dwidth, dheight])
        self.dist_box = TextBox(axbox, 'Dist: ', initial=f"{self.game.dist}")
        self.dist_box.on_submit(self.distbox)

        # Toggle Anchors location #
        anch_text_x = 0.23; anch_text_width = 0.175  
        anch_text_y = 0.9; anch_text_height = 0.05
        anch_text_ax = plt.axes([anch_text_x, anch_text_y, anch_text_width, anch_text_height])
        self.anch_text = Button(anch_text_ax, "Hide Anchors")
        self.anch_text.on_clicked(self.toggle_anchors)

        # Rand_Seedbox Location #
        bx = 0.43; bwidth = 0.175  
        by = 0.9; bheight = 0.05
        bax = plt.axes([bx, by, bwidth, bheight])
        self.rand_box = Button(bax, "Random Seed")
        self.rand_box.on_clicked(self.rand_seed)

        # Plus 1 Location #
        p_one_x = 0.63; p_one_width = 0.175  
        p_one_y = 0.9; p_one_height = 0.05
        p_one_ax = plt.axes([p_one_x, p_one_y, p_one_width, p_one_height])
        p_one = Button(p_one_ax, "1 Step")
        p_one.on_clicked(self.plus_one)

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
        plt.show()

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
    def iterbox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.iter:         # (avoids unwanted submission for clicking out of box)
            self.game.iter = eval(text)      # Sets the new iteration value
            self.game.targets_and_steps()

            # Plot new state
            self.graph_state()

    # anch_num textbox
    def anchbox(self,text):
        # Update State
        result = int(eval(text))
        if result != self.game.num_anchors and result > 0:   # (avoids unwanted submission for clicking out of box)
            self.game.num_anchors = result                   # Sets the new iteration value
            self.game.compute_anchors()              # Compute new anchors
            self.game.targets_and_steps()

            # Plot new state
            self.graph_state()

    # anch_num textbox
    def distbox(self,text):
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

    # Toggle Anchors Button
    def toggle_anchors(self, null):
        self.game.show_anchor = not self.game.show_anchor
        self.graph_state()

    # Random Seed Button
    def rand_seed(self, null):
        self.game.set_seed(np.random.randint(0,10000))
        self.game.targets_and_steps()
        self.graph_state()
        self.seed_box.set_val(self.game.seed)

    # 1 Step Button
    def plus_one(self, null):
        self.game.iter += 1
        self.game.targets_and_steps()
        self.graph_state()


    ### Display it ###
    def graph_state(self):
        self.ax.clear()
        self.ax.scatter(self.game.c_stepsX, self.game.c_stepsY, color=self.colormap[self.game.c_targets], s=1)    # Implement button to toggle colormap (esp for high pow_2)
        if self.game.show_anchor:
            self.ax.scatter(self.game.x_anchors,self.game.y_anchors, color='k', s=5)       # Implement button to toggle this for high pow_2
        plt.draw()