from Grapher import MyGrapher
from GameRules import Game

### Inintial Game State ###
start_num = 3
start_dist = 0.5
start_iter = 100
start_seed = 3170
resX = 250
resY = 250
num_threads = 1

displayScaleX = 9
displayScaleY= 9

# Set up the game #
game = Game(
    num_anchors = start_num, 
    dist = start_dist, 
    iter = start_iter, 
    seed = start_seed,
    resX = resX,
    resY = resY,
    num_threads = num_threads)

# Invoke the Grapher (Comes with Widgets) #
myGrapher = MyGrapher(
    game,
    show_anchors = False,
    xDim = displayScaleX,
    yDim = displayScaleY)