from Grapher import GraphManager
from GameRules import GameManager

### Inintial Game State ###
start_num = 3
start_dist = 0.5
start_iter = 100
start_seed = 3170
resX = 250
resY = 250

displayScaleX = 9
displayScaleY= 9

# Set up the game #
game = GameManager(
    num_anchors = start_num, 
    dist = start_dist, 
    iter = start_iter, 
    seed = start_seed,
    resX = resX,
    resY = resY)

# Invoke the Grapher (Comes with Widgets) #
myGrapher = GraphManager(
    game,
    show_anchors = False,
    xDim = displayScaleX,
    yDim = displayScaleY)