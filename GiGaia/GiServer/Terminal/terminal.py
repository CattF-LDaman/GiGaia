
from .Commands import commands, alias

import traceback

class Terminal:

    def __init__(self,server):

        self.server = server
        self.running = True

    def run(self):

        self.server.log("You can now input commands.")
        while self.running:

            cmd_in = input()

            cmd = cmd_in.split(" ")[0]
            args = cmd_in.split(" ")[1:]

            self.server.log(f"CMD: {cmd_in}",1)

            if cmd in commands or cmd in alias:

                try:
                    out = commands[alias[cmd] if cmd in alias else cmd](self.server, args)
                    self.server.log(f"OUT:\n{out}\n")
                except Exception as e:
                    self.server.log(f"Server encountered an error while executing your command:\n{''.join(traceback.format_exception(e, value=e ,tb=e.__traceback__))}",4)

            else:
                self.server.log(f"Unknown command: {cmd_in}",3)