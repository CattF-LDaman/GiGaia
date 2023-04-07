
from .start import Start
from .play import Play, ConnectTo, Joining
from .info import Info

__pages = [Start, Info, Play, ConnectTo, Joining]

PAGES = {p.__name__:p for p in __pages}