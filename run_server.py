
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from GiGaia.GiServer.server import Server

if __name__ == "__main__":
    Server(dev=True).run()