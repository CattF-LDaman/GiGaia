
class Body:
    
    def __init__(self, entity):

        self.entity = entity
        self.assets = entity.game.assets

        self.data = self.assets