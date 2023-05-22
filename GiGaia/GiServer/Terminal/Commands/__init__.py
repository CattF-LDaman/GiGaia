
from .admin import stop, reloadconf, clients, disconnect, version, privileges, rempass
from .game import players, tickrate, bob, bobcoin, entities, world, superplayer, addtime, tp, say, fly, flyspeed

import os
import inspect

all_cmds = [stop, reloadconf, clients, tickrate, disconnect, players, bob, bobcoin, entities, version, world, superplayer, addtime, tp, privileges, say, fly, flyspeed, rempass]

commands = {cmd.__name__:cmd for cmd in all_cmds}

alias = {"exit":"stop", "?":"help", "dc":"disconnect", "kick":"disconnect", "build":"version","priv":"privileges"}

privileges = {stop:5, reloadconf:5, clients:4, disconnect:4, rempass:4, players:1, entities:2, version:4, world:4, superplayer:1, fly:2, flyspeed:2, addtime:1, tp:1}

commands["listcmds"] = lambda s,a,p : f"All commands:\n{os.linesep.join(sorted(list(commands)))}"
commands["help"] = lambda s,a,p : f"All commands:\n\n{os.linesep.join([f'{cmdn}: {inspect.getdoc(command)}' if inspect.getdoc(command) else f'{cmdn}: No description.' for cmdn,command in sorted(commands.items())])}"
commands["whoami"] = lambda s,a,p : p.name if p else 'SERVER'