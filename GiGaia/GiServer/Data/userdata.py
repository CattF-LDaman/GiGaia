
from GiGaia.GiCore.Data.struc import build_struc, read_struc
from GiGaia.GiCore.Data.datatypes import D_RAW,D_INT64
from GiGaia.GiCore.Data.hashing import hash_pwd, hash_str

import os
import time

class UserData:

    STRUC_VERSION = 1
    STRUC = (
            ("pwd_hash", D_RAW, 1),
            ("salt", D_RAW, 1),
            ("last_login", D_INT64),
            ("last_write", D_INT64),
            )


    def __init__(self, users_dir, username):
        
        self.username = username
        self.user_hash = hash_str(username)

        self.location = os.path.join(users_dir, self.user_hash+'.user')

        self.pwd_hash = None
        self.salt = None
        self.last_login = None

        if self.exists:
            self.read()


    @property
    def exists(self):
        return os.path.exists(self.location)
    
    def create(self, new_pwd):

        self.change_password(new_pwd)
        self.last_login = 0

        self.save()
        self.read()

    def save(self):

        udata = {
            'pwd_hash': self.pwd_hash,
            'salt': self.salt,
            'last_login': self.last_login,
            'last_write': int(time.time())
        }

        udata_packed = build_struc(self.STRUC, udata)

        with open(self.location, 'wb') as uf:
            uf.write(self.STRUC_VERSION.to_bytes(1,"little"))
            uf.write(udata_packed)

    def read(self):

        if not self.exists:
            pass
        
        with open(self.location, 'rb') as uf:

            uf_version = uf.read(1)[0]
            if uf_version != self.STRUC_VERSION:
                raise ValueError(f"UF version missmatch: {uf_version} != {self.STRUC_VERSION}")
            
            udata = read_struc(self.STRUC, uf.read())
            for k,v in udata.__dict__.items():
                setattr(self, k, v)

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