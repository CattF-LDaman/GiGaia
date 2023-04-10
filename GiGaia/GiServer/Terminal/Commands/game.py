
def players(server, args):
    """Show all players."""
    return ", ".join(server.game.players.keys()) if server.game.players else "Nobody online :("