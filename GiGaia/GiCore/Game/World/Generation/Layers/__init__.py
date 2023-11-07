
from .base import Base
from .caverns import Caverns
from .caves import Caves
from .deposits import LimestoneDeposits, GraniteDeposits, CoalDeposits, NoxumLuxDeposits

LAYERS = [Base, LimestoneDeposits, GraniteDeposits, Caverns, Caves, CoalDeposits, NoxumLuxDeposits]

SETTINGS = {l.__name__:l.SETTINGS for l in LAYERS}