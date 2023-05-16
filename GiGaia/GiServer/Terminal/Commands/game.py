
def players(server, args, player=None):
    """Show all players."""
    return ", ".join(server.game.players.keys()) if server.game.players else "Nobody online :("

def tickrate(server, args, player=None):
    """Get current and target tickrate."""
    return f"CURRENT: {server.game.current_tickrate}, TARGET: {server.config.game.tickrate}"

def bobcoin(server, args, player=None):

    for e in server.game.entity_manager.entities.values():
        if e.NAME == "Bob":
            e.add_coins(int(args[0]) if args else 1)

def bob(server, args, player=None):

    server.game.entity_manager.spawn("Bob", (0,-5000))

def entities(server, args, player=None):
    """Show all entities."""
    return "\n".join(e.identity_str for e in server.game.entity_manager.entities.values())

def world(server, args, player=None):
    """Displays world information."""
    w = server.game.world
    inf = f"World: {w.name}\nLocation: {w.data.location}\nSeed: {w.data.seed}\nLoaded regions: {len(w.data.region_files)}\nTimestamp: {w.time.value}\nDay: {w.time.day}\nDay progress:{w.time.day_progress}"
    return inf

def superplayer(server, args, player=None):
    """Double a given player's speed and jump strength."""

    if not args:
        return "usage: superplayer <PLAYER NAME>"
    
    player_name = args[0]
    if player_name not in server.game.players:
        return f"No such player: {player_name}"
    
    player = server.game.players[player_name]
    if player.entity:
        player.entity.change("speed",player.entity.props["speed"]*2)
        player.entity.change("jump_strength",player.entity.props["jump_strength"]*2)

    return "God is dead."

def addtime(server, args, player=None):

    server.game.world.time_start += int(args[0])

def tp(server, args, player=None):
    """Teleport player"""

    if not player and len(args) != 3:
        return "usage: tp <PLAYER NAME> <X> <Y>"
    elif player and len(args) == 2:
        x = int(args[0])
        y = int(args[1])
    elif len(args) == 3:
        x = int(args[1])
        y = int(args[2])
        player_name = args[0]
        if player_name not in server.game.players:
            return f"No such player: {player_name}"
        player = server.game.players[player_name]

    if player.entity:
        player.entity.position[0] = x
        player.entity.position[1] = y

    return f"Teleported {player.name} to ({args[1]} {args[2]})"

def say(server, args, player=None):

    name = "SERVER"
    if player:
        name = player.name

    server.game.chat.broadcast_chat(name, " ".join(args))

def fly(server, args, player=None):
    """Toggles flight for a specified player or yourself."""

    if not args and player is None:
        return "usage: fly <PLAYER NAME>"
    elif args:
        player_name = args[0]
        if player_name not in server.game.players:
            return f"No such player: {player_name}"
        player = server.game.players[player_name]
    
    flying_enabled = player.entity.toggle_flight()

    return f"Flying has been {'enabled' if flying_enabled else 'disabled'} for {player.name}."
    
def flyspeed(server, args, player=None):
    """Changes or shows a player's flight speed."""
    speed = None
    # if len(args) < 2 and player is None:
    #     return "usage: flyspeed <PLAYER NAME> <SPEED>"
    if len(args) == 2:
        player_name = args[0]
        if player_name not in server.game.players:
            return f"No such player: {player_name}"
        player = server.game.players[player_name]
        speed = int(args[1])
    elif len(args) == 1:
        try:
            speed = int(args[0])
        except ValueError:
            player_name = args[0]
            if player_name not in server.game.players:
                return f"No such player: {player_name}"
            player = server.game.players[player_name]

    if speed is not None:
        player.entity.change("flight_speed", speed)
        return f"Flight speed for {player.name} changed to {speed}."

    return f"{player.name}'s flight speed is {player.entity.props['flight_speed']}."
