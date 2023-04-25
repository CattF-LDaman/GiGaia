import pygame

def rotate(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, 360-angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def replace_color(sprite, c_from, c_to):

    csp = pygame.PixelArray(sprite)
    csp.replace(tuple(c_from),tuple(c_to))
    csp.close()
    return sprite