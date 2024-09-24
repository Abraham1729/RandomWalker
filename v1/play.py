from GameRules import GameRules
from Grapher import MyGrapher

##### Inintial State #####
start_num = 3
start_dist = 0.5
start_seed = 3170
start_seed = 3000
start_iter = 9

game = GameRules(
    num_anchors=start_num, 
    dist=start_dist, 
    iter=start_iter, 
    seed=start_seed
)

anchorSize = 25
stepCircleSize = 25

graph = MyGrapher(game, showFig=True, anchorSize=anchorSize, stepCircleSize=stepCircleSize, dpi=50)

