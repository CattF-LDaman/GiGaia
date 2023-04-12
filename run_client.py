
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from GiGaia.GiClient.client import Client

if __name__ == "__main__":

    Client(dev=True).run()