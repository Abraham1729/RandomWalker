from matplotlib import pyplot as plt
# from MyWidgets.MyWidgets import HeatmapBox, ResolutionBox, SeedBox, IterationBox, AnchorBox, DistanceBox, DpiBox, SaveButton, RandomSeedButton
from MyWidgets import HeatmapBox, ResolutionBox, SeedBox, IterationBox, AnchorBox, DistanceBox, DpiBox, SaveButton, RandomSeedButton

class GraphManager():

    def __init__(self, game, show_anchors=True,
                 xDim=1, yDim=1, colormap='gnuplot2', dpi=300, showGraph=True, saveLoc="./res/"):
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

        # Setup & Run
        self.set_figs()
        self.set_widgets()
        self.graph_state()
        if showGraph: plt.show()


    def set_figs(self):    
        ### Defining Fig and Ax ###
        self.graphFig = plt.figure(figsize=(self.xDim,self.yDim)) # default figsize (6.4,4.8) width height
        self.ax1 = self.graphFig.add_subplot()
        self.graphFig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        ### Widget Figure ###
        self.widgetFig = plt.figure(figsize=(self.xDim,1))
        self.ax2 = self.widgetFig.add_subplot()
        self.widgetFig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    def set_widgets(self):
        # Lower half of figure
        self.seedBox = SeedBox(                     self, x = 0.05, y = 0.0125, width = 0.08, height = 0.25)
        self.iterationBox = IterationBox(           self, x = 0.35, y = 0.0125, width = 0.10, height = 0.25)
        self.anchorBox = AnchorBox(                 self, x = 0.70, y = 0.0125, width = 0.05, height = 0.25)
        self.distanceBox = DistanceBox(             self, x = 0.90, y = 0.0125, width = 0.08, height = 0.25)

        # Upper half of figure
        self.resolutionBox = ResolutionBox(         self, x = 0.05, y = 0.7, width = 0.08, height = 0.25)
        self.heatmapBox = HeatmapBox(               self, x = 0.35, y = 0.7, width = 0.10, height = 0.25)
        self.dpiBox = DpiBox(                       self, x = 0.60, y = 0.7, width = 0.05, height = 0.25)
        self.saveButton = SaveButton(               self, x = 0.70, y = 0.7, width = 0.10, height = 0.25)
        self.randomSeedButton = RandomSeedButton(   self, x = 0.83, y = 0.7, width = 0.15, height = 0.25)

    ### Display it ###        
    def graph_state(self):
        self.ax1.clear()
        self.ax1.imshow(self.game.screen.reshape((self.game.resX, self.game.resY)), cmap=self.colormap)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.draw()
        self.graphFig.canvas.draw_idle()
