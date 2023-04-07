
import time

def stop(server, args):
    """Stop server, nicely."""
    server.close()

def test(server, args):

    server.traffic.broadcast("P_TEST", {"timestamp":int(time.time()), "message":" ".join(args)})  # Send test packet

    return f"Sent P_TEST packet to {len(server.clients)} clients."

def reloadconf(server, args):
    """Reloads config from files."""
    server.config.load()
    server.logger.config = server.config.server.logging_config

    return "Config reloaded. WARNING: Some changes might still require restart to take effect."

def clients(server, args):
    """Show all connected clients."""
    out = ""
    tbl_head = f"{'USER':>16} | {'TIME_CONN':>16} | {'ADDR':>32} | {'RECV':>16} | {'SENT':>16}"
    out += (tbl_head)+"\n"
    out += ("-"*len(tbl_head))+"\n"
    for client in server.clients:
        out += f"{client.username[:16]:>16} | {client.time_active[:16]:>16} | {client.full_address[:32]:>32} | {client.received:>16} | {client.sent:>16}"+"\n"
    out += ("-"*len(tbl_head))
    return out

def tickrate(server, args):
    """Get current and target tickrate."""
    return f"CURRENT: {server.game.current_tickrate}, TARGET: {server.config.game.tickrate}"

def disconnect(server, args):
    cid = " ".join(args)
    c = server.identify(cid)
    if c:
        c.close()
        return f"Client '{c.identifier}' disconnected."
    
    return f"Client '{cid}' not found."