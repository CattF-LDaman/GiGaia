
from . import CONNECT_NUM_TRIES
from .authentication import authenticate, AuthenticationError

from GiGaia.GiCore.version import VERSION_BYTES, VERSION_STRING, version_to_string, version_from_bytes
from GiGaia.GiCore.Networking import BOND_E_WRONGVERSION,BOND_S_SAMEVERSION, BOND_E_USERNAMECOLLIDE, BOND_S_USERNAMEOK, BOND_E_USERNAMEINVALID

import socket

def connect(addr):

    from GiGaia.GiClient import RUNNING_CLIENT as rc
    rc.log(f"Attempting connection with {addr[0]}:{addr[1]}")

    for t in range(CONNECT_NUM_TRIES):

        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            
            soc.connect(addr)

            conn = authenticate(soc, addr)

            if type(conn) == str:
                return AuthenticationError(conn)

            rc.log("Connection succeeded.")

            return conn

        except (ConnectionError, AuthenticationError) as e:

            rc.log(f"Connection error on try {t+1}/{CONNECT_NUM_TRIES}: {type(e).__name__}: {e}")
            rc.menu.join_fail_details = f"Retrying... Try {t+1}/{CONNECT_NUM_TRIES}"
            if t+1 == CONNECT_NUM_TRIES:
                return e

def login(conn, username):

    conn.send(VERSION_BYTES)

    version_ack = conn.recv(1)

    if version_ack == BOND_E_WRONGVERSION:

        server_version = conn.recv(3)

        raise VersionMismatch(f"You need version {version_to_string(version_from_bytes(server_version))} to play on this server.")

    conn.sendsized(username.encode('ascii'),lensize=1)

    username_ack = conn.recv(1)

    if username_ack == BOND_E_USERNAMECOLLIDE:

        raise UsernameCollision("User with same username already on server.")
    
    elif username_ack == BOND_E_USERNAMEINVALID:

        raise InvalidUsername("Invalid username.")

class VersionMismatch(Exception):
    pass

class UsernameCollision(Exception):
    pass

class InvalidUsername(Exception):
    pass