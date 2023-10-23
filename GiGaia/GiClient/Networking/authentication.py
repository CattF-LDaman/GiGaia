from GiGaia.GiCore.Networking import AUTH_HANDSHAKE, AUTH_OBF_HANDSHAKE
from GiGaia.GiCore.Networking.connection import Connection
from GiGaia.GiCore.Networking.obf import generate_key

def authenticate(conn, addr):

    conn.send(AUTH_HANDSHAKE)

    server_key = conn.recv(256)
    client_key = generate_key()
    conn.send(client_key)

    conn = Connection(conn, addr, server_key, client_key)

    conn.send(AUTH_OBF_HANDSHAKE)

    if conn.recv(4) != b"bG0N":

        return "Obfuscation handshake failed."

    return conn

class AuthenticationError(Exception):
    pass