
from .base import Base
from .caverns import Caverns
from .caves import Caves
from .deposits import LimestoneDeposits, GraniteDeposits, CoalDeposits, NoxumLuxDeposits
from .treetest import TreeTest
from .house import House

LAYERS = [Base, LimestoneDeposits, GraniteDeposits, Caverns, Caves, CoalDeposits, NoxumLuxDeposits, House]

SETTINGS = {l.__name__:l.SETTINGS for l in LAYERS}