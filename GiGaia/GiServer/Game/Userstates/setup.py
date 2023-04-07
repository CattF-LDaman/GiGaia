
from GiGaia.GiServer.Game.userstate import Userstate

class Setup(Userstate):

    def __init__(self, user):
        super().__init__(user)

    def setup(self):

        self.h.send("SC_GAME_INFO", {'name':self.game.config.name, 'description':self.game.config.description, 'connected':0})
        
        nation = self.h.recv("CS_LOGIN")
        if not nation:
            pass
        print(nation)

        self.h.send("SC_LOGIN_CONFIRM", {'is_ok': True, 'msg':""})

    def tick(self):

        pass