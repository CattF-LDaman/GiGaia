
class EntityBase:

    PROPERTIES = {}

    def __init__(self):
        print("EntityBase in")
        if hasattr(self.__class__,'PROPERTIES'):
            for cls in self.__class__.__mro__:  # Merges properties between child and parent classes
                if hasattr(cls,"PROPERTIES"):
                    print(f"    {self.__class__.__name__} <- {cls.__name__} {getattr(cls,'PROPERTIES',[])}")
                    self.__class__.PROPERTIES.update(getattr(cls,'PROPERTIES',[]))
        print("EntityBase out")

class PhysicalBase(EntityBase):

    PROPERTIES = {"Based","Gay"}

    def __init__(self):
        print("PhysicalBase in")
        super().__init__()
        print("PhysicalBase out")


class PersonBase(PhysicalBase):

    PROPERTIES = {"Big","Bad"}

    def __init__(self):
        print("PersonBase in")
        super().__init__()
        print("PersonBase out")

class Entity(EntityBase):

    def __init__(self):
        print("Entity in")
        super().__init__()
        print("Entity out")

class Person(Entity, PersonBase):

    def __init__(self):
        print(", ".join([cls.__name__ for cls in self.__class__.__mro__]))
        print("Person in")
        super().__init__()
        print("Person out")

if __name__ == "__main__":

    p = Person()
    print(p.PROPERTIES)