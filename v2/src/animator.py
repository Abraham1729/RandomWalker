from Grapher import MyGrapher
from GameRules import Game
import numpy as np

### Inintial Game State ###
start_num = 6
start_dist = 1
start_iter = 100000000
start_seed = 3170
resX = 5000
resY = 5000

displayScaleX = 9
displayScaleY= 9




# Set up the game #
game = Game(num_anchors=start_num, 
                    dist = start_dist, 
                    iter=start_iter, 
                    seed=start_seed,
                    resX=resX,
                    resY=resY)

# Invoke the Grapher (Comes with Widgets) #
myGrapher = MyGrapher(game,
                        show_colors=False,
                        show_anchors=True,
                        xDim=displayScaleX,
                        yDim=displayScaleY,
                        showGraph=False,
                        colormap="flag_r",
                        saveLoc="../res/flag/")


# We're going to do some animations over distance changes first
start = 1
stop = 0
steps = 101
distances = np.linspace(start,stop,steps)


def update_distance():
    game.compute_steps()
    game.set_screen_arrays()
    game.fit_to_screen()
    game.set_screen()

def draw_and_save():
    myGrapher.graph_state()
    myGrapher.save_fig('null')

for i in distances:
    game.dist = round(i,7)
    update_distance()
    draw_and_save()
    


