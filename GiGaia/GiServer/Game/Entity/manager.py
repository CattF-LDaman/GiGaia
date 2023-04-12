
class EntityManager:

    def __init__(self, game):
        
        self.game = game

        self.entities = {}
        self._cur_eid = 0 # Entity Instance ID

    def _get_eid(self):

        self._cur_eid += 1
        return self._cur_eid
    
    def spawn(self):
        pass
    
    def update(self):

        for 