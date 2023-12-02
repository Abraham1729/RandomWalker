from GameRules import GameRules
from Grapher import MyGrapher

##### Inintial State #####
start_num = 3
start_dist = 0.5
start_iter = 10000
start_seed = 3170
game = GameRules(
    num_anchors=start_num, 
    dist = start_dist, 
    iter=start_iter, 
    seed=start_seed)
graph = MyGrapher(game)