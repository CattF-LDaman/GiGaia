
def players(server, args):
    """Show all players."""
    return ", ".join(server.game.players.keys()) if server.game.players else "Nobody online :("

def tickrate(server, args):
    """Get current and target tickrate."""
    return f"CURRENT: {server.game.current_tickrate}, TARGET: {server.config.game.tickrate}"

def bobcoin(server, args):

    for e in server.game.entity_manager.entities.values():
        if e.NAME == "Bob":
            e.add_coins(int(args[0]) if args else 1)

def bob(server, args):

    server.game.entity_manager.spawn("Bob", (0,-5000))

def entities(server, args):
    """Show all entities."""
    return "\n".join(e.identity_str for e in server.game.entity_manager.entities.values())

def world(server, args):
    """Displays world information."""
    w = server.game.world
    inf = f"World: {w.name}\nLocation: {w.data.location}\nSeed: {w.data.seed}\nLoaded regions: {len(w.data.region_files)}\nTimestamp: {w.time.value}\nDay: {w.time.day}\nDay progress:{w.time.day_progress}"
    return inf

def superplayer(server, args):
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

def aids(server, args):

    return str(server.game.players[args[0]].entity.aids())