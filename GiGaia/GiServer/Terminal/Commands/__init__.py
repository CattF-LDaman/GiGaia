
from .admin import stop, test, reloadconf, clients, tickrate, disconnect

import os
import inspect

all_cmds = [stop, test, reloadconf, clients, tickrate, disconnect]

commands = {cmd.__name__:cmd for cmd in all_cmds}

alias = {"exit":"stop", "?":"help", "dc":"disconnect", "kick":"disconnect"}

commands["listcmds"] = lambda s,a : f"All commands:\n{os.linesep.join(list(commands))}"
commands["help"] = lambda s,a : f"All commands:\n\n{os.linesep.join([f'{cmdn}: {inspect.getdoc(command)}' if inspect.getdoc(command) else f'{cmdn}: No description.' for cmdn,command in commands.items()])}"
