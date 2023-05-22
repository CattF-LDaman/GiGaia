
from GiGaia.GiServer.Game.userstate import Userstate
from GiGaia.GiCore.Game.states import STATE_IDS as SIDS

class Setup(Userstate):

    def __init__(self, user):
        super().__init__(user)

    def finish(self):

        self.log(f"{self.user.name} has logged in.", 10)
        self.user.switch_state(SIDS.PLAYING)

    def setup(self):

        self.h.send("SC_GAME_INFO", {   'name':self.game.config.name,
                                        'theme_color':self.game.config.theme_color,
                                        'description':self.game.config.description, 
                                        'connected':len(self.game.users), 
                                        'user_exist':False if not self.user.data.exists else not self.user.data.remove_pass,
                                        'tickrate':self.game.config.tickrate,
                                    })
        
        login_success = False
        for _ in range(self.game.config.login_attempts):
            lgn = self.h.recv("CS_LOGIN")
            if not lgn:
                self.user.disconnect("Empty login response.")
                return

            if self.user.data.exists:
                if self.user.data.remove_pass:
                    login_success = True
                    self.user.data.change_password(lgn.password)
                    break
                else:
                    if self.user.data.check_password(lgn.password):
                        login_success = True
                        break
                    else:
                        self.h.send("SC_LOGIN_CONFIRM", {'is_ok': False, 'msg':"Invalid credentials."})
            else:
                self.user.data.create(lgn.password)
                login_success = True
                break

        if login_success:
            self.h.send("SC_LOGIN_CONFIRM", {'is_ok': True, 'msg':""})
            self.finish()
        else:
            self.user.disconnect("Too many invalid login attempts.")

    def tick(self):

        pass