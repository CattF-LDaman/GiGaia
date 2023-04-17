
from .base import Base
from .caverns import Caverns
from .caves import Caves

LAYERS = [Base, Caverns, Caves]

SETTINGS = {l.__name__:l.SETTINGS for l in LAYERS}