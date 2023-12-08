
from .base import Base
from .caverns import Caverns
from .caves import Caves
from .deposits import LimestoneDeposits, GraniteDeposits, CoalDeposits, NoxumLuxDeposits
from .treetest import TreeTest
from .house import House
from .mines import Mine

LAYERS = [Base, LimestoneDeposits, GraniteDeposits, Caverns, Caves, CoalDeposits, NoxumLuxDeposits, House, Mine]

SETTINGS = {l.__name__:l.SETTINGS for l in LAYERS}