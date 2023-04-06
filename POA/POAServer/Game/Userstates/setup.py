
from POA.POAServer.Game.userstate import Userstate

class Setup(Userstate):

    def __init__(self, user):
        super().__init__(user)

    def setup(self):
        
        nation = self.h.recv("CS_CREATE_NATION")
        if not nation:
            pass
        print(nation)

        self.h.send("SC_NATION_OK", {'is_ok': True, 'msg':""})

    def tick(self):

        pass