
from .start import Start
from .play import Play, ConnectTo, Joining, PlayLocal
from .info import Info
from .lostconn import LostConn

__pages = [Start, Info, Play, ConnectTo, Joining, PlayLocal, LostConn]

PAGES = {p.__name__:p for p in __pages}