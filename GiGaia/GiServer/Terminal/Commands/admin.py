from GiGaia.GiCore import INFO
from GiGaia.GiServer.Data.userdata import UserData

import time

def stop(server, args, player=None):
    """Stop server, nicely."""
    for user in tuple(server.game.users.values()):
        user.kick("Server closed." if len(args) == 0 else f"Server closed: {args[0]}")
    server.close()

def reloadconf(server, args, player=None):
    """Reloads config from files."""
    server.config.load()
    server.logger.config = server.config.logging.__dict__

    return "Config reloaded. WARNING: Some changes might still require restart to take effect."

def clients(server, args, player=None):
    """Show all connected clients."""
    out = ""
    tbl_head = f"{'USER':>16} | {'TIME_CONN':>16} | {'ADDR':>32} | {'RECV':>16} | {'SENT':>16}"
    out += (tbl_head)+"\n"
    out += ("-"*len(tbl_head))+"\n"
    for client in server.clients:
        out += f"{client.username[:16]:>16} | {client.time_active[:16]:>16} | {client.full_address[:32]:>32} | {client.received:>16} | {client.sent:>16}"+"\n"
    out += ("-"*len(tbl_head))
    return out

def disconnect(server, args, player=None):
    """Disconnects client from server."""
    cid = " ".join(args)
    c = server.identify(cid)
    if c:
        c.close()
        return f"Client '{c.identifier}' disconnected."
    
    return f"Client '{cid}' not found."

def version(server, args, player=None):
    """Shows version and build of running server."""

    return INFO

def privileges(server, args, player=None):
    """Promotes specified user to privilege level or shows level."""

    if len(args) == 0 and player:
        return f"{player.name} is privilege level {player.user.privileges}."

    if len(args) == 1 and args[0] in server.game.users:
        return f"{args[0]} is privilege level {server.game.users[args[0]].privileges}."

    if len(args) != 2:
        return "Usage: privileges [USER] [LEVEL]"
    
    user = args[0]
    level = int(args[1])

    if level > 5 or level < 0:
        return "Level must be between 0 and 5."

    if player:
        if player.user.privileges < level:
            return f"You must be privilege level {level} or higher to do that."
    
    if user not in server.game.users:
        return "User not found."

    if player and player.user.privileges <= server.game.users[user].privileges:
        return "Target player has equal or higher privileges than you."
    
    server.game.users[user].set_privileges(level)
    return f"User {user} is now privilege level {level}."

def rempass(server, args, player=None):
    """Removes specified user password."""

    if len(args) != 1:
        return "Usage: rempass [USER]"
    
    user_data = UserData(server.game.dirs["users"], args[0])

    if not user_data.exists:
        return f"User '{args[0]}' not found."
    
    if player and player.user.privileges <= user_data.privileges:
        return "Target player has equal or higher privileges than you."

    user_data.remove_pass = True
    user_data.save()

    return f"'{args[0]}' must now reset their password on login."

def kick(server, args, player=None):
    """Kicks player from server."""

    if len(args) == 0:
        return "Usage: kick [PLAYER] [REASON]"
    
    player_name = args[0]
    reason = "No reason."
    if len(args) == 2:
        reason = args[1]
    
    if player_name not in server.game.users:
        return "Player not found."

    target_player = server.game.users[player_name]

    if player and player.user.privileges <= target_player.privileges:
        return "Target player has equal or higher privileges than you."

    target_player.kick(f"Kicked by {player.name if player else 'server'}: {reason}")

    return f"'{args[0]}' has been kicked."
