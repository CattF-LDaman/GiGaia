
from GiGaia.GiCore.Game.Entities.entity import Entity as EntityBase

class Entity(EntityBase):

    def __init__(self, entity_manager, eid, position, props={}):
        super().__init__(eid, position)

        self.em = self.entity_manager = entity_manager
        self.state = self.em.state
        self.game = self.em.game

        self.exists = True

        self.set_properties(props)

        self.ghost_position = self.position.copy()

        if self.props["name"]:
            self.state.ui.entity_name(self)

    def update_props(self, changes):

        self.props.update(changes)

    def update_position(self, new_pos):

        self.ghost_position = new_pos.copy()
        self.position = new_pos

    def destroy(self):

        self.em.remove(self.eid)

    @property
    def draw_pos(self):  # Position on the game screen

        return self.em.scene.convert_world_to_screen_coord(self.ghost_position)

    @property
    def window_pos(self):  # Position on the actual game window

        return self.em.scene.convert_world_to_window_coord(self.ghost_position)

    def draw(self, surf):
        
        pass