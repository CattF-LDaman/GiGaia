import inspect
import random

from GiGaia.GiCore.Game.World.coords import sum_coords, coord_range

def players(server, args, player=None):
    """Show all players."""
    return ", ".join(server.game.players.keys()) if server.game.players else "Nobody online :("

def tickrate(server, args, player=None):
    """Get (or set) current and target tickrate."""
    if len(args):
        server.config.game.tickrate = int(args[0])
        return f"Changed target tickrate to {args[0]}."
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
    inf = f"World: {w.name}\nLocation: {w.data.location}\nSeed: {w.data.seed}\nChunks being generated: {w.generator.generating}\nLoaded regions: {len(w.data.region_files)}\nTimestamp: {w.time.value}\nDay: {w.time.day}\nDay progress: {w.time.day_progress}"
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

def miniplayer(server, args, player=None):
    """Smaller man."""

    if not args and not player:
        return "usage: playersize <PLAYER NAME>"
    
    player_name = args[0] if args else player.name
    if player_name not in server.game.players:
        return f"No such player: {player_name}"
    
    player = server.game.players[player_name]
    if player.entity:
        player.entity.change("width", 3)
        player.entity.change("height", 6)
        player.entity.change("speed", 3200//2)
        player.entity.change("jump_strength", 650//2)
        player.entity.resize()

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

    return f"Teleported {player.name} to ({x} {y})"

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

def noclip(server, args, player=None):
    """Toggles noclip for a specified player or yourself."""

    if not args and player is None:
        return "usage: noclip <PLAYER NAME>"
    elif args:
        player_name = args[0]
        if player_name not in server.game.players:
            return f"No such player: {player_name}"
        player = server.game.players[player_name]
    
    noclip_enabled = player.entity.toggle_noclip()

    return f"Noclip has been {'enabled' if noclip_enabled else 'disabled'} for {player.name}."

def noclipent(server, args, player=None):
    """Toggles noclip for a specified entity."""

    if not args:
        return "usage: noclipent <EID>"
    elif args:
        eid = int(args[0])
        if eid not in server.game.entity_manager.entities:
            return f"No such entity: {eid}"
        entity = server.game.entity_manager.entities[eid]
    
    noclip_enabled = entity.toggle_noclip()

    return f"Noclip has been {'enabled' if noclip_enabled else 'disabled'} for {entity.NAME} {entity.eid}."

def stresstest(server, args, player=None):

    for _ in range(int(args[0])):

        server.game.entity_manager.spawn("Firefly", player.entity.position)

def visent(server, args, player=None):
    """Shows what entities are within a player's visibility range."""

    if not args and player is None:
        return "usage: visent <PLAYER NAME>"
    elif args:
        player_name = args[0]
        if player_name not in server.game.players:
            return f"No such player: {player_name}"
        player = server.game.players[player_name]

    return "\n".join(e.identity_str for e in player.visible_entities)

def destent(server, args, player=None):
    """Destroy specified entity."""
    if not args:
        return "usage: destent <EID>"

    eid = int(args[0])

    if eid not in server.game.entity_manager.entities:
        return "Entity not found."
    
    server.game.entity_manager.entities[eid].destroy()
    return "Entity destroyed."

def litent(server, args, player=None):
    """Makes entity visible in the dark."""
    if not args:
        return "usage: litent <EID>"

    eid = int(args[0])

    if eid not in server.game.entity_manager.entities:
        return "Entity not found."
    
    ent = server.game.entity_manager.entities[eid]
    ent.change("lit", not ent.props["lit"])

    return f"Entity {'un' if not ent.props['lit'] else ''}lit."

def gent(server, args, player=None):
    """Shows entity information by Entity Instance ID."""
    if not args:
        return "usage: gent <EID>"

    eid = int(args[0])

    if eid not in server.game.entity_manager.entities:
        return "Entity not found."
    
    ent = server.game.entity_manager.entities[eid]
    ent_props = "\n".join(f'\t--> {p} = {v}' for p,v in ent.props.items())
    ent_attr = "\n".join(f'\t--> {p} = {v}' for p,v in vars(ent).items())

    def get_first_subpckg(cls):
        return cls.__module__.split(".")[1]
    ent_cls_mro = ', '.join(f"{c.__name__} ({get_first_subpckg(c)})" for c in inspect.getmro(type(ent)) if c.__module__.startswith("GiGaia"))
    
    return f"""-- {ent.NAME}#{ent.eid} --
    ID:       {ent.ID}
    POSITION: {ent.position}
    PROPERTIES:
    {ent_props}
    CLASS_MRO:
        {ent_cls_mro}
    ATTR:
    {ent_attr}
    """

def tileids(server, args, players=None):

    return "\n".join(f"{t.id}: {t.display_name} ({t.name})" for t in server.assets.tiles.values())

def summon(server, args, player=None):

    try:
        for _ in range(amount := int(args[1]) if len(args) > 1 else 1):

            server.game.entity_manager.spawn(args[0], player.entity.position if player else (0,0))
        
        return f"Spawned {amount} {args[0]}"
    except KeyError:
        return f"Entity '{args[0]}' not found"
    except ValueError:
        return f"{args[1]} is not a number (amount)"
    
def rainitems(server, args, player=None):
    
    if not player:
        return "Must be a player for this one."
    
    for _ in range(int(args[0]) if args else 1):
        server.game.entity_manager.spawn("ItemEntity", sum_coords(player.entity.position, (random.randint(-150,150), random.randint(-600, -300))), props={"item":random.choice(list(server.assets.data.Items.__dict__.keys()))})
    return "Here they come baby"

def destall(server, args, player=None):
    """Destroy all entities with type."""
    if not args:
        return "usage: destent <EID>"

    etype = args[0]
    try:
        etype = int(args[0])
    except ValueError:
        pass
    
    destroyed = 0
    for ent in server.game.entity_manager.entities.copy().values():
        if ent.ID == etype or ent.NAME == etype:
            destroyed += 1
            ent.destroy()

    return f"Killed {destroyed} entities."

def itmtest(server, args, player=None):
    if player:
        player.inv.add_item('person', "jonko", 1, {"sleuren_left":int(args[0])})

def timescale(server, args, player=None):
    """Change game time scale (until restart)"""
    if not args:
        return 'usage: timescale <SCALE>'
    
    try:
        scale = float(args[0])
    except ValueError:
        return 'SCALE should be a number.'
    
    server.game.config.time_scale = scale
    return f"Changed time_scale to {scale}"

def createstruc(server, args, player=None):
    """Create a structure at current or given coordinates"""
    if not args:
        return "usage: createstruc <STRUC> <X> <Y>"
    
    struc = str(args[0])
    if struc not in server.assets.structures:
        return f"Structure '{struc}' does not exist"

    pos = player.entity.tile_pos if player else None
    if len(args) >= 3:
        pos = (int(args[1]), int(args[2]))
    if not pos:
        return "Please provide a position."

    server.game.world.create_structure(struc, pos)
    return f"Created '{struc}' at {pos}."