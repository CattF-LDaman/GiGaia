
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

    server.game.entity_manager.spawn("Bob", (10,0))

def entities(server, args):
    """Show all entities."""
    return "\n".join(e.identity_str for e in server.game.entity_manager.entities.values())