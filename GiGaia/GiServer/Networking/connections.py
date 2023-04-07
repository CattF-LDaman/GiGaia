
from GiGaia.GiCore.threading import threaded_daemon
from GiGaia.GiCore.version import VERSION_BYTES, VERSION_STRING, version_to_string, version_from_bytes
from GiGaia.GiCore.Networking import BOND_E_WRONGVERSION,BOND_S_SAMEVERSION, BOND_E_USERNAMECOLLIDE, BOND_S_USERNAMEOK

from GiGaia.GiServer.handle import Handle
from GiGaia.GiServer.Networking.authentication import authenticate

import socket

@threaded_daemon
def accept_connections(server):

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    try:
        soc.bind(("", server.config.server.port))
        server.log(f"Socket bound on port {server.config.server.port}",1)
    except OSError:
        server.log(f"Couldn't bind socket to port {server.config.server.port}, maybe another server instance is already running.",5)
        server.close(1)

    soc.listen()
    server.log("Started listening on socket.",1)

    server.log("Connections will now be accepted.",2)

    while True:
        conn, addr = soc.accept()

        server.log(f"New connection with {addr[0]}:{addr[1]}",1)

        bond_connection(server,conn,addr)

@threaded_daemon
def bond_connection(server,conn,addr):

    try:

        conn = authenticate(conn,addr)

        if type(conn) == str:

            server.log(f"{addr[0]}:{addr[1]} failed authentication: {conn}",1)
            return

        server.log(f"{conn.full_address} succesfully authenticated.")

        client_version = conn.recv(3)

        if client_version != VERSION_BYTES:

            conn.send(BOND_E_WRONGVERSION)
            conn.send(VERSION_BYTES)
            conn.close()
            server.log(f"Disconnected from {conn.full_address}: wrong bG0N version: {version_to_string(version_from_bytes(client_version))}.")
            return

        conn.send(BOND_S_SAMEVERSION)

        client_username = conn.recvsized(lensize=1).decode("ascii")

        if client_username in server.user_clients:
            conn.send(BOND_E_USERNAMECOLLIDE)
            conn.close()
            server.log(f"{conn.full_address} tried to connect with username that's already online: {client_username}")
            return

        conn.send(BOND_S_USERNAMEOK)

        client = Handle(server,conn,addr,client_username)
        server.join(client)

        server.log(f"{client.identifier} connected.")

    except ConnectionError:

        server.log(f"Lost connection with {addr[0]}:{addr[1]} during authentication.",1)
