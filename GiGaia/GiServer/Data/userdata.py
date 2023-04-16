
from GiGaia.GiCore.Data.datafile import Datafile
from GiGaia.GiCore.Data.datatypes import D_RAW,D_INT64
from GiGaia.GiCore.Data.hashing import hash_pwd, hash_str

import os
import time

class UserData(Datafile):

    DATA_VERSION = 1
    STRUC = (
            ("pwd_hash", D_RAW, 1),
            ("salt", D_RAW, 1),
            ("last_login", D_INT64),
            ("last_write", D_INT64),
            )


    def __init__(self, users_dir, username):

        self.username = username
        self.user_hash = hash_str(username)

        super().__init__(os.path.join(users_dir, self.user_hash+'.user'))
    
    def on_create(self, new_pwd):

        self.change_password(new_pwd)
        self.last_login = 0

    def on_save(self):

        self.last_write = int(time.time())

    def check_password(self, pwd):
        
        pwd_h = hash_pwd(pwd, self.salt)

        return pwd_h == self.pwd_hash
    
    def login(self):

        self.last_login = int(time.time())
        self.save()

    def change_password(self, pwd):

        self.salt = os.urandom(16)
        self.pwd_hash = hash_pwd(pwd, self.salt)

        if self.exists:
            self.save()