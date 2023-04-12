
def players(server, args):
    """Show all players."""
    return ", ".join(server.game.players.keys()) if server.game.players else "Nobody online :("

def tickrate(server, args):
    """Get current and target tickrate."""
    return f"CURRENT: {server.game.current_tickrate}, TARGET: {server.config.game.tickrate}"