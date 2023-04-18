
import pygame

class Scene:

    def __init__(self, game):

        self.game = game

        self.camera_pos = [0, 0]

    def set_camera(self, pos):

        self.camera_pos = pos

    @property
    def origin(self):

        return self.game.screen.get_rect().center+pygame.Vector2(-self.camera_pos[0],-self.camera_pos[1])

    def convert_window_to_world_coord(self,coord):
        
        coord = pygame.Vector2(coord)/self.game.scale
        dx, dy = self.origin
        S1 = (dx, dy)
        T1 = [0, 0]
        T2 = [6, 6]
        S2 = (S1[0] + 6, S1[1] + 6)
        TranslateFactor_x = (T2[0] * S1[0] - T1[0] * S2[0]) / (S1[0] - S2[0])
        ScalingFactor_x = (T2[0] - T1[0]) / (S2[0] - S1[0])
        TargetX = TranslateFactor_x + ScalingFactor_x * coord[0]
        TranslateFactor_y = (T2[1] * S1[1] - T1[1] * S2[1]) / (S1[1] - S2[1])
        ScalingFactor_y = (T2[1] - T1[1]) / (S2[1] - S1[1])
        TargetY = TranslateFactor_y + ScalingFactor_y * coord[1]

        return [TargetX, TargetY]
    
    
    def convert_screen_to_world_coord(self,coord):
        
        coord = pygame.Vector2(coord)
        dx, dy = self.origin
        S1 = (dx, dy)
        T1 = [0, 0]
        T2 = [6, 6]
        S2 = (S1[0] + 6, S1[1] + 6)
        TranslateFactor_x = (T2[0] * S1[0] - T1[0] * S2[0]) / (S1[0] - S2[0])
        ScalingFactor_x = (T2[0] - T1[0]) / (S2[0] - S1[0])
        TargetX = TranslateFactor_x + ScalingFactor_x * coord[0]
        TranslateFactor_y = (T2[1] * S1[1] - T1[1] * S2[1]) / (S1[1] - S2[1])
        ScalingFactor_y = (T2[1] - T1[1]) / (S2[1] - S1[1])
        TargetY = TranslateFactor_y + ScalingFactor_y * coord[1]

        return [TargetX, TargetY]

    def convert_world_to_screen_coord(self,coord):

        return self.origin + coord

    def convert_world_to_window_coord(self,coord):

        return pygame.Vector2(self.origin + coord)*self.game.scale
