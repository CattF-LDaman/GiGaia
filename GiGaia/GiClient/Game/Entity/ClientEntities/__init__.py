
from .person import Person
from .bob import Bob
from .firefly import Firefly
from .blob import Blob

_ents = [Person, Bob, Firefly,Blob]

ENTITIES = {ent.ID:ent for ent in _ents}
ENTITIES_NAME = {ent.NAME:ent for ent in _ents}