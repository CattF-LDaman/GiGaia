
from GiGaia.GiCore.Game.Entities.entity import Entity as EntityBase

from GiGaia.GiCore.Game.World.coords import sub_coords, mult_coord, sum_coords
class Entity(EntityBase):

    def __init__(self, entity_manager, eid, position, props={}):
        super().__init__(eid, position)

        self.em = self.entity_manager = entity_manager
        self.state = self.em.state
        self.game = self.em.game

        self.exists = True

        self.set_properties(props)

        self.ghost_position = self.position.copy()

        if self.props["name"] and self.eid != self.state.player_eid:
            self.state.ui.entity_name(self)

    def update_props(self, changes):

        self.props.update(changes)

    def update_position(self, new_pos):

        self.position = new_pos

    def destroy(self):

        self.em.remove(self.eid)

    @property
    def draw_pos(self):  # Position on the game screen

        return self.em.scene.convert_world_to_screen_coord(self.ghost_position if self.game.config.networking.entity_ghosting else self.position)

    @property
    def window_pos(self):  # Position on the actual game window

        return self.em.scene.convert_world_to_window_coord(self.position if self.game.config.networking.entity_ghosting else self.position)

    @property
    def is_me(self):
        return self.eid == self.state.player_eid

    @property
    def ghost_speed(self):

        return self.game.config.networking.entity_ghost_speed if not self.is_me else self.game.config.networking.player_ghost_speed

    def update_ghost(self):

        if self.game.config.networking.entity_ghosting:
            self.ghost_position = list(sum_coords(mult_coord(sub_coords(self.position, self.ghost_position), self.game.dt*self.ghost_speed),self.ghost_position))#new_pos.copy()

    def draw(self, surf):
        
        pass