
from POA.POACore.Networking import AUTH_HANDSHAKE, AUTH_OBF_HANDSHAKE
from POA.POACore.Networking.connection import Connection
from POA.POACore.Networking.obf import generate_key

def authenticate(conn,addr):

    if conn.recv(len(AUTH_HANDSHAKE)) != AUTH_HANDSHAKE:

        conn.close()
        return "Failed handshake, probably not a POA client."

    server_key = generate_key()
    conn.send(server_key)
    client_key = conn.recv(256)

    conn = Connection(conn,addr,client_key,server_key)

    if conn.recv(len(AUTH_OBF_HANDSHAKE)) != AUTH_OBF_HANDSHAKE:

        conn.close()
        return "Obfuscation handshake failed."

    conn.send(b"bG0N")

    return conn
