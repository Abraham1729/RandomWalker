from matplotlib import pyplot as plt

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