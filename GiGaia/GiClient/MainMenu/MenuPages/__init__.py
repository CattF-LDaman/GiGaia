
from .start import Start
from .play import Play, ConnectTo, Joining, PlayLocal
from .info import Info

__pages = [Start, Info, Play, ConnectTo, Joining, PlayLocal]

PAGES = {p.__name__:p for p in __pages}