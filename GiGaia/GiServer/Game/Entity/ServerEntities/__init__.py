
from .person import Person
from .bob import Bob
from .firefly import Firefly
from .blob import Blob
from .doomfly import Doomfly
from .itementity import ItemEntity
from .boink import Boink

_ents = [Person, Bob, Firefly, Blob, Doomfly, ItemEntity, Boink]

ENTITIES = {ent.ID:ent for ent in _ents}
ENTITIES_NAME = {ent.NAME:ent for ent in _ents}