
from .person import Person
from .bob import Bob
from .physical import Physical
from .firefly import Firefly
from .blob import Blob
from .doomfly import Doomfly
from .itementity import ItemEntity

_ents = [Person, Bob, Physical, Firefly, Blob, Doomfly, ItemEntity]

ENTITIES = {e.ID:e for e in _ents}