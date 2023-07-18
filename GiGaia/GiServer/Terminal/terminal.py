
from .Commands import commands, alias, privileges

import traceback

class Terminal:

    def __init__(self,server):

        self.server = server
        self.running = True

    def parse(self, cmd_in, player=None):

        cmd_in = cmd_in.strip()

        cmd = cmd_in.split(" ")[0]
        args = cmd_in.split(" ")[1:]

        self.server.log((f"<{player.name}> " if player else "")+f"CMD: {cmd_in}")

        if not player:
            level = 6
        else:
            level = player.user.privileges

        if cmd in commands or cmd in alias:

            try:
                cmd_func = commands[alias[cmd] if cmd in alias else cmd]

                if cmd_func in privileges:
                    if privileges[cmd_func] > level:
                        player.send_msg("Insufficient privileges.","CMD")
                        return

                out = cmd_func(self.server, args, player)

                if not player:
                    self.server.log(f"OUT:\n{out}\n")
                elif out:
                    player.send_msg(str(out), "CMD")

            except Exception as e:
                if not player:
                    self.server.log(f"Server encountered an error while executing your command:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
                else:
                    self.server.log(f"Server encountered an error while executing {player.name}'s command:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)
                    player.send_msg(f"Server error: {str(e)}", "CMD")
        elif not player:
            self.server.log(f"Unknown command: {cmd_in}",3)
        else:
            player.send_msg("No such command.", "CMD")

    def run(self):

        self.server.log("You can now input commands.")
        while self.running:

            cmd_in = input()

            if self.running:
                self.parse(cmd_in)