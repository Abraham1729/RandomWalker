from matplotlib import pyplot as plt
from matplotlib.widgets import TextBox, Button
import random

class MyWidget:
    def __init__(self, grapher, x, y, width, height):
        # set references
        self.grapher = grapher
        self.game = grapher.game

        # Widget location 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.axbox = plt.axes([x, y, width, height])

class HeatmapBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.heat_text = TextBox(self.axbox, "Colormap: ", initial=f"{self.grapher.colormap}")
        self.heat_text.on_submit(self.update)

    def update(self,text):
        # result = eval(text)
        if text != self.grapher.colormap and text in self.colormaps:
            self.grapher.colormap = text
            self.grapher.graph_state()

    colormaps = ['magma', 'inferno', 'plasma', 'viridis', 'cividis', 'twilight', 'twilight_shifted', 
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
    
class ResolutionBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.res_box = TextBox(self.axbox, 'ResX: ', initial=f"{self.game.resX}")
        self.res_box.on_submit(self.update)

    def update(self,text):
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
            self.grapher.graph_state()

class RandomSeedButton(MyWidget):
    def __init__(self, grapher, x, y , width, height):
        super().__init__(grapher, x, y , width, height)
        self.randomSeedButton = Button(self.axbox, "Random Seed")
        self.randomSeedButton.on_clicked(self.update)

    def update(self, null):
        # self.game.set_seed(np.random.randint(0,10000))
        self.game.set_seed(random.randint(0,10000))
        
        # Recomputes 
        self.game.compute_targets()
        self.game.compute_steps()
        self.game.set_screen_arrays()
        self.game.fit_to_screen()
        self.game.set_screen()
        self.grapher.graph_state()
        # self.seed_box.set_val(self.game.seed)
        self.grapher.seedBox.seedBox.set_val(self.game.seed)

class SaveButton(MyWidget):
    def __init__(self, grapher, x, y , width, height):
        super().__init__(grapher, x, y , width, height)
        self.saveButton = Button(self.axbox, "Save Figure")
        self.saveButton.on_clicked(self.update)

    def update(self, null):
        self.grapher.graphFig.savefig(fname=f"{self.grapher.saveLoc}{self.game.num_anchors}_{self.game.dist:7f}_{self.game.iter}-{self.game.seed}_{self.game.resX}_{self.grapher.dpi}-{self.grapher.colormap}.png",dpi=self.grapher.dpi,)

class SeedBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.seedBox = TextBox(self.axbox, 'Seed: ', initial=f"{self.game.seed}")
        self.seedBox.on_submit(self.update)

    def update(self,text):
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
        self.grapher.graph_state()

class IterationBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.iterationBox = TextBox(self.axbox, 'Iterations: ', initial=f"{self.game.iter}")
        self.iterationBox.on_submit(self.update)

    def update(self,text):
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
            self.grapher.graph_state()

class DpiBox(MyWidget):
    def __init__(self, grapher, x, y , width, height):
        super().__init__(grapher, x, y , width, height)
        self.dpiBox = TextBox(self.axbox, "DPI: ", initial=f"{self.grapher.dpi}")
        self.dpiBox.on_submit(self.update)

    def update(self,text):
        self.grapher.dpi = eval(text)

class AnchorBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.anchorBox = TextBox(self.axbox, 'Anchors: ', initial=f"{self.game.num_anchors}")
        self.anchorBox.on_submit(self.update)

    def update(self,text):
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
            self.grapher.graph_state()

class DistanceBox(MyWidget):
    def __init__(self, grapher, x, y, width, height):
        super().__init__(grapher, x, y, width, height)
        self.distanceBox = TextBox(self.axbox, 'Dist: ', initial=f"{self.game.dist}")
        self.distanceBox.on_submit(self.update)


    def update(self,text):
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
            self.grapher.graph_state()


