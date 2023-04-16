
from .admin import stop, reloadconf, clients, disconnect, version
from .game import players, tickrate, bob, bobcoin, entities

import os
import inspect

all_cmds = [stop, reloadconf, clients, tickrate, disconnect, players, bob, bobcoin, entities, version]

commands = {cmd.__name__:cmd for cmd in all_cmds}

alias = {"exit":"stop", "?":"help", "dc":"disconnect", "kick":"disconnect", "build":version}

commands["listcmds"] = lambda s,a : f"All commands:\n{os.linesep.join(sorted(list(commands)))}"
commands["help"] = lambda s,a : f"All commands:\n\n{os.linesep.join([f'{cmdn}: {inspect.getdoc(command)}' if inspect.getdoc(command) else f'{cmdn}: No description.' for cmdn,command in sorted(commands.items())])}"
