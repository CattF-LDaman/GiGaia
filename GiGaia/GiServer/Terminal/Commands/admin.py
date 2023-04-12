
import time

def stop(server, args):
    """Stop server, nicely."""
    server.close()

def reloadconf(server, args):
    """Reloads config from files."""
    server.config.load()
    server.logger.config = server.config.logging.__dict__

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

def disconnect(server, args):
    """Disconnects client from server."""
    cid = " ".join(args)
    c = server.identify(cid)
    if c:
        c.close()
        return f"Client '{c.identifier}' disconnected."
    
    return f"Client '{cid}' not found."