
from .admin import stop, reloadconf, clients, disconnect, version, privileges, rempass, kick, outbound, pid, ping, testtp
from .game import players, tickrate, bob, bobcoin, entities, world, superplayer, miniplayer, addtime, tp, say, fly, flyspeed, visent, stresstest, destent, gent, tileids, summon, noclip, noclipent, litent, rainitems, destall, itmtest, timescale

import os
import inspect

all_cmds = [stop,
            reloadconf, 
            clients, 
            tickrate, 
            disconnect, 
            players, 
            bob, 
            bobcoin, 
            entities, 
            version, 
            world, 
            superplayer,
            miniplayer,
            addtime, 
            tp, 
            privileges, 
            say, 
            fly, 
            flyspeed, 
            rempass, 
            visent, 
            stresstest,
            kick, 
            outbound, 
            destent, 
            gent, 
            tileids, 
            summon,
            noclip,
            noclipent,
            pid,
            litent,
            ping,
            rainitems,
            destall,
            timescale,
            testtp
            #itmtest
        ]

commands = {cmd.__name__:cmd for cmd in all_cmds}

alias = {"exit":"stop", "?":"help", "dc":"disconnect", "build":"version","priv":"privileges", "teleport":"tp", "nc":"noclip", "nce":"noclipent", "lit":"litent", "glow":"litent", "killall":"destall", "kill":"destent"}

privileges = {stop:5, reloadconf:5, clients:4, disconnect:4, kick:3, rempass:4, players:1, entities:2, version:4, world:4, superplayer:1, miniplayer:1, fly:2, flyspeed:2, addtime:1, tp:1, visent:2, stresstest:5, outbound:4, destent:2, gent:1, tileids:1, summon:2, noclip:2, noclipent:2, pid:5, litent:2, ping:4, testtp:4, rainitems:5, destall:2, timescale:3}

commands["listcmds"] = lambda s,a,p : f"All commands:\n{os.linesep.join(sorted(list(commands)))}"
commands["help"] = lambda s,a,p : f"All commands:\n\n{os.linesep.join([f'{cmdn}: {inspect.getdoc(command)}' if inspect.getdoc(command) else f'{cmdn}: No description.' for cmdn,command in sorted(commands.items()) if command not in privileges or privileges[command] <= (p.user.privileges if p else 6)])}"
commands["whoami"] = lambda s,a,p : p.name if p else 'SERVER'