import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button

class MyGrapher():

    def __init__(self, game, show_anchors=True,
                 xDim=1, yDim=1, colormap='gnuplot2', dpi=300, showGraph=True, saveLoc="./v2/res/"):
        '''
        Provides the interactive pyplot graph for a given Game instance.
        Comes with all kinds of fun widgets placed as haphazardly as can be.
        '''

        # Parse arguments
        self.game = game
        self.show_anchors = show_anchors    # toggle anchor display
        self.xDim = xDim                    # Scaling the display window
        self.yDim = yDim                    # Scaling the display window

        self.colormap = colormap            # Current pyplot colormap
        self.dpi = dpi                      # dpi of image
        self.saveLoc = saveLoc              # Used to modify the savefile directory

        # Additional colormaps for reference
        self.colormaps = ['magma', 'inferno', 'plasma', 'viridis', 'cividis', 'twilight', 'twilight_shifted', 
                          'turbo', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'GnBu', 'Greens', 'Greys', 'OrRd', 
                          'Oranges', 'PRGn', 'PiYG', 'PuBu', 'PuBuGn', 'PuOr', 'PuRd', 'Purples', 'RdBu', 'RdGy', 
                          'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Spectral', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr', 
                          'YlOrRd', 'afmhot', 'autumn', 'binary', 'bone', 'brg', 'bwr', 'cool', 'coolwarm', 'copper', 
                          'cubehelix', 'flag', 'gist_earth', 'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 
                          'gist_stern', 'gist_yarg', 'gnuplot', 'gnuplot2', 'gray', 'hot', 'hsv', 'jet', 'nipy_spectral', 
                          'ocean', 'pink', 'prism', 'rainbow', 'seismic', 'spring', 'summer', 'terrain', 'winter', 'Accent', 
                          'Dark2', 'Paired', 'Pastel1', 'Pastel2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 
                          'tab20c', 'grey', 'gist_grey', 'gist_yerg', 'Grays', 'magma_r', 'inferno_r', 'plasma_r', 
                          'viridis_r', 'cividis_r', 'twilight_r', 'twilight_shifted_r', 'turbo_r', 'Blues_r', 'BrBG_r', 
                          'BuGn_r', 'BuPu_r', 'CMRmap_r', 'GnBu_r', 'Greens_r', 'Greys_r', 'OrRd_r', 'Oranges_r', 
                          'PRGn_r', 'PiYG_r', 'PuBu_r', 'PuBuGn_r', 'PuOr_r', 'PuRd_r', 'Purples_r', 'RdBu_r', 'RdGy_r', 
                          'RdPu_r', 'RdYlBu_r', 'RdYlGn_r', 'Reds_r', 'Spectral_r', 'Wistia_r', 'YlGn_r', 'YlGnBu_r', 
                          'YlOrBr_r', 'YlOrRd_r', 'afmhot_r', 'autumn_r', 'binary_r', 'bone_r', 'brg_r', 'bwr_r', 'cool_r', 
                          'coolwarm_r', 'copper_r', 'cubehelix_r', 'flag_r', 'gist_earth_r', 'gist_gray_r', 
                          'gist_heat_r', 'gist_ncar_r', 'gist_rainbow_r', 'gist_stern_r', 'gist_yarg_r', 'gnuplot_r', 
                          'gnuplot2_r', 'gray_r', 'hot_r', 'hsv_r', 'jet_r', 'nipy_spectral_r', 'ocean_r', 'pink_r', 
                          'prism_r', 'rainbow_r', 'seismic_r', 'spring_r', 'summer_r', 'terrain_r', 'winter_r', 'Accent_r', 
                          'Dark2_r', 'Paired_r', 'Pastel1_r', 'Pastel2_r', 'Set1_r', 'Set2_r', 'Set3_r', 'tab10_r', 'tab20_r', 'tab20b_r', 'tab20c_r']
        

        # Set up the figures
        self.set_figs()
        self.set_widget_locations()

        # Show the darned thing
        self.graph_state()

        # Good to disable when generating pictures via loop
        if showGraph: plt.show()

    ##### Figure Setup Functions #####

    def set_figs(self):    
        ### Defining Fig and Ax ###
        self.fig1 = plt.figure(figsize=(self.xDim,self.yDim)) # default figsize (6.4,4.8) width height
        self.ax1 = self.fig1.add_subplot()
        self.fig1.subplots_adjust(left=0, right=1, top=1, bottom=0)

        ### Widget Figure ###
        self.fig2 = plt.figure(figsize=(self.xDim,1))
        self.ax2 = self.fig2.add_subplot()
        self.fig2.subplots_adjust(left=0, right=1, top=1, bottom=0)

    def set_widget_locations(self):
        ### Lower Half of Figure ###
        # SeedBox location #
        sx_pos = 0.05; swidth = 0.08
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
        ax_pos = 0.7; awidth = 0.05
        ay_pos = 0.0125; aheight = 0.25
        axbox = plt.axes([ax_pos, ay_pos, awidth, aheight])
        self.anch_text = TextBox(axbox, 'Anchors: ', initial=f"{self.game.num_anchors}")
        self.anch_text.on_submit(self.anchBox)

        # distBox location #
        dx_pos = 0.9; dwidth = 0.08
        dy_pos = 0.0125; dheight = 0.25
        axbox = plt.axes([dx_pos, dy_pos, dwidth, dheight])
        self.dist_box = TextBox(axbox, 'Dist: ', initial=f"{self.game.dist}")
        self.dist_box.on_submit(self.distBox)

        ### Upper Half of Figure ###
        # resBox location #
        rx_pos = 0.05; rwidth = 0.08
        ry_pos = 0.7; rheight = 0.25
        axbox = plt.axes([rx_pos, ry_pos, rwidth, rheight])
        self.res_box = TextBox(axbox, 'ResX: ', initial=f"{self.game.resX}")
        self.res_box.on_submit(self.resBox)

        # Heatmap textbox location #
        hx = 0.35; hwidth = 0.10  
        hy = 0.7; hheight = 0.25
        hax = plt.axes([hx, hy, hwidth, hheight])
        self.heat_text = TextBox(hax, "Colormap: ", initial=f"{self.colormap}")
        self.heat_text.on_submit(self.heatbox)

        # Dpi textbox location #
        dx = 0.6; dwidth = 0.05  
        dy = 0.7; dheight = 0.25
        dax = plt.axes([dx, dy, dwidth, dheight])
        self.dpi_text = TextBox(dax, "DPI: ", initial=f"{self.dpi}")
        self.dpi_text.on_submit(self.set_dpi)
            
        # Save Figure Location #
        fx = 0.70; fwidth = 0.10  
        fy = 0.7; fheight = 0.25
        fax = plt.axes([fx, fy, fwidth, fheight])
        self.save_box = Button(fax, "Save Figure")
        self.save_box.on_clicked(self.save_fig)
        
        # Rand_Seedbox Location #
        bx = 0.83; bwidth = 0.15  
        by = 0.7; bheight = 0.25
        bax = plt.axes([bx, by, bwidth, bheight])
        self.rand_box = Button(bax, "Random Seed")
        self.rand_box.on_clicked(self.rand_seed)

    ##### Widget Functions #####
    ### Lower Half of Figure ###
    # Seed-setting Textbox
    def seedbox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.seed:     # (avoids unwanted submission for clicking out of box)
            self.game.set_seed(result)   # Sets the new seed
            self.game.compute_targets()
            self.game.compute_steps()
            self.game.set_screen_arrays()
            self.game.fit_to_screen()
            self.game.set_screen()

        # Plot new state
        self.graph_state()

    # Iter-setting Textbox
    def iterBox(self,text):
        # Update State
        result = eval(text)
        if result != self.game.iter:         # (avoids unwanted submission for clicking out of box)
            self.game.iter = eval(text)      # Sets the new iteration value
            self.game.set_target_array()
            self.game.compute_targets()
            self.game.set_steps_arrays()
            self.game.compute_steps()
            self.game.set_screen_arrays()
            self.game.fit_to_screen()
            self.game.set_screen()

            # Plot new state
            self.graph_state()

    # anchBox textbox
    def anchBox(self,text):
        # Update State
        result = int(eval(text))
        if result != self.game.num_anchors and result > 0:   # (avoids unwanted submission for clicking out of box)
            self.game.num_anchors = result                   # Sets the new iteration value
            self.game.compute_anchors()              # Compute new anchors
            self.game.compute_targets()
            self.game.compute_steps()
            self.game.set_screen_arrays()
            self.game.fit_to_screen()
            self.game.set_screen()

            # Plot new state
            self.graph_state()

    # distBox textbox
    def distBox(self,text):
        result = eval(text)
        # Don't waste computations for no-change submissions
        if result != self.game.dist:
            if result > 2:
                print("REFUSED: Solution diverges for large iterations. Disable for low iterations at your own risk.")
            else:
                # Updates distance with textbox entry
                self.game.dist = result
                # Recomputes steps and screen
                self.game.compute_steps()
                self.game.set_screen_arrays()
                self.game.fit_to_screen()
                self.game.set_screen()

            # Plot new state
            self.graph_state()

    ### Upper Half of Figure ###
    # resBox textbox
    def resBox(self,text):
        result = eval(text)
        if result != self.game.resX:
            # Updates resX and resY
            self.game.resX = result
            self.game.resY = result
            # Don't need to recomupte targets or steps
            # Do need to rescale to screen.
            self.game.set_screen_arrays()
            self.game.fit_to_screen()
            self.game.set_screen()

            # Plot the new state
            self.graph_state()

    # heatbox textbox
    def heatbox(self,text):
        # Update state
        # result = eval(text)
        if text != self.colormap and text in self.colormaps:
            self.colormap = text
            self.graph_state()

    # Set DPI
    def set_dpi(self,text):
        self.dpi = eval(text)

    # Save fig (High dpi)
    def save_fig(self, null):
        self.fig1.savefig(fname=f"{self.saveLoc}{self.game.num_anchors}_{self.game.dist:7f}_{self.game.iter}-{self.game.seed}_{self.game.resX}_{self.dpi}-{self.colormap}.png",dpi=self.dpi,)


    # Random Seed Button
    def rand_seed(self, null):
        self.game.set_seed(np.random.randint(0,10000))
        
        # Recomputes 
        self.game.compute_targets()
        self.game.compute_steps()
        self.game.set_screen_arrays()
        self.game.fit_to_screen()
        self.game.set_screen()
        self.graph_state()
        self.seed_box.set_val(self.game.seed)


    ### Display it ###        
    def graph_state(self):
        self.ax1.clear()
        self.ax1.imshow(self.game.screen.reshape((self.game.resX, self.game.resY)), cmap=self.colormap)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.draw()
        self.fig1.canvas.draw_idle()
