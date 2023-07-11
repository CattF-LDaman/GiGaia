
from .base import Base
from .caverns import Caverns
from .caves import Caves
from .deposits import LimestoneDeposits, GraniteDeposits

LAYERS = [Base, LimestoneDeposits, GraniteDeposits, Caverns, Caves]

SETTINGS = {l.__name__:l.SETTINGS for l in LAYERS}