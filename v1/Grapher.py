import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button

class MyGrapher():

    def __init__(self, game, showFig=True, anchorSize=5, stepCircleSize=3, dpi=300):
        self.game = game
        self.dpi = dpi
        self.showFig = showFig
        self.anchorSize = anchorSize
        self.stepCircleSize = stepCircleSize

        self.set_fig()
        self.set_colormap()



        if self.showFig: 
            self.set_widget_locations()
            self.graph_state()
            plt.show()
        else:
            self.graph_state() 
            self.savefig()

    def set_fig(self):
        self.fig = plt.figure(figsize=(8,6))
        self.ax = self.fig.add_subplot()

    def set_colormap(self):
        # (Colormap Initialization)
        nice_colors = np.array(
            [[0.75,0,0],
             [0,0.75,0],
             [0,0,0.75],
             [0.75,0.75,0],
             [0.75,0,0.75],
             [0,0.75,0.75]])
        # Arbitrary dimension of 500, increase if you ever do anchors > 500.
        rand_colors = np.random.random(size=(500,3)).round(1)
        self.colormap = np.concatenate((nice_colors,rand_colors),axis=0)

    def set_widget_locations(self):
        ### Wiget Locations ###  
        # Seedbox location
        sx_pos = 0.1; swidth = 0.08
        sy_pos = 0.0125; sheight = 0.05
        axbox = plt.axes([sx_pos, sy_pos, swidth, sheight])
        self.seed_box = TextBox(axbox, 'Seed: ', initial=f"{self.game.seed}")
        self.seed_box.on_submit(self.seedbox)

        # Iterbox location
        ix_pos = 0.35; iwidth = 0.1
        iy_pos = 0.0125; iheight = 0.05
        axbox = plt.axes([ix_pos, iy_pos, iwidth, iheight])
        self.iter_box = TextBox(axbox, 'Iterations: ', initial=f"{self.game.iter}")
        self.iter_box.on_submit(self.iterbox)

        # Anchbox location
        ax_pos = 0.6; awidth = 0.05
        ay_pos = 0.0125; aheight = 0.05
        axbox = plt.axes([ax_pos, ay_pos, awidth, aheight])
        self.anch_box = TextBox(axbox, 'Anchors: ', initial=f"{self.game.num}")
        self.anch_box.on_submit(self.anchbox)

        # Distbox location
        dx_pos = 0.8; dwidth = 0.08
        dy_pos = 0.0125; dheight = 0.05
        dxbox = plt.axes([dx_pos, dy_pos, dwidth, dheight])
        self.dist_box = TextBox(dxbox, 'Dist: ', initial=f"{self.game.dist}")
        self.dist_box.on_submit(self.distbox)

        # Toggle Anchors location
        tanch_x = 0.23; tanch_width = 0.175  
        tanch_y = 0.9; tanch_height = 0.05
        tanch_ax = plt.axes([tanch_x, tanch_y, tanch_width, tanch_height])
        self.tanch = Button(tanch_ax, "Hide Anchors")
        self.tanch.on_clicked(self.toggle_anchors)

        # Rand_Seedbox Location
        bx = 0.43; bwidth = 0.175  
        by = 0.9; bheight = 0.05
        bax = plt.axes([bx, by, bwidth, bheight])
        self.brand = Button(bax, "Random Seed")
        self.brand.on_clicked(self.rand_seed)

        # Plus 1 Location
        p_one_x = 0.63; p_one_width = 0.175  
        p_one_y = 0.9; p_one_height = 0.05
        p_one_ax = plt.axes([p_one_x, p_one_y, p_one_width, p_one_height])
        self.p_one = Button(p_one_ax, "1 Step")
        self.p_one.on_clicked(self.plus_one)

    def graph_state(self):
        self.ax.clear()
        # Implement button to toggle colormap (esp for high pow_2)
        self.ax.scatter(self.game.x, self.game.y, color=self.colormap[self.game.choice], s=self.stepCircleSize)    
        if self.game.show_anchor: 
            self.ax.scatter(self.game.x_anchors,self.game.y_anchors, color='k', s=self.anchorSize)
        if (not self.showFig): 
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.draw()

    ### Widget functions ###
    # Seed-setting Textbox
    def seedbox(self, text):
        # Update State
        result = eval(text)
        if result != self.game.seed:     # (avoids unwanted submission for clicking out of box)
            self.game.set_seed(result)   # Sets the new seed
            self.game.compute_targets()  # Computes anchor selection based on seed
            self.game.compute_steps()    # Computes new (x,y) positions given the anchor selection sequence

        # Plot new state
        self.graph_state()

    # Iter-setting Textbox
    def iterbox(self, text):
        # Update State
        result = eval(text)
        if result != self.game.iter:         # (avoids unwanted submission for clicking out of box)
            self.game.iter = eval(text)      # Sets the new iteration value
            self.game.set_seed(self.game.seed)    # Gotta reset this, that's annoying
            self.game.compute_targets()      # Computes new targets
            self.game.compute_steps()        # And the new steps

            # Plot new state
            self.graph_state()

    # anch_num textbox
    def anchbox(self, text):
        # Update State
        result = int(eval(text))
        if result != self.game.num and result > 0:   # (avoids unwanted submission for clicking out of box)
            self.game.num = result                   # Sets the new iteration value
            self.game.set_seed(self.game.seed)            # Gotta reset this, that's annoying
            self.game.compute_anchors()              # Compute new anchors
            self.game.compute_targets()              # Computes new targets
            self.game.compute_steps()                # And the new steps

            # Plot new state
            self.graph_state()

    # anch_num textbox
    def distbox(self, text):
        # Update State
        result = eval(text)
        if result != self.game.dist:                # (avoids unwanted submission for clicking out of box)
            if result > 2:
                print("REFUSED: Solution diverges for large iterations. Disable for low iterations at your own risk.")
            else:
                self.game.dist = result                 # Sets the new iteration value
                self.game.set_seed(self.game.seed)            # Gotta reset this, that's annoying
                self.game.compute_steps()                # And the new steps

            # Plot new state
            self.graph_state()

    # Toggle Anchors Button
    def toggle_anchors(self, null):
        if self.game.show_anchor:
            self.game.show_anchor = False
        else: self.game.show_anchor = True
        
        self.graph_state()

    # Random Seed Button
    def rand_seed(self, null):
        self.game.set_seed(np.random.randint(10000))
        self.seed_box.set_val(self.game.seed)
        self.game.compute_targets()
        self.game.compute_steps()
        self.graph_state()

    # 1 Step Button
    def plus_one(self, null):
        self.game.iter += 1
        self.game.set_seed(self.game.seed)
        self.game.compute_targets()
        self.game.compute_steps()
        self.graph_state()

    def savefig(self):
        plt.savefig(fname=f"./res/{self.game.num}_{self.game.dist}_{self.game.seed}_{self.game.iter}.png", dpi=self.dpi)
        plt.close()
    