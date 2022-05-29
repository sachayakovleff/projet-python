import pygame


class Player(pygame.sprite.Sprite):
    # Initialize Player values
    def __init__(self, x, y):
        super().__init__()
        self.position = [x, y]
        self.animation_down = []
        self.animation_right = []
        self.animation_left = []
        self.animation_up = []

        self.facing = 2
        self.i = 0

        self.initializeanimation()
        self.player_image = pygame.image.load('player.png')
        self.image = self.player_image.subsurface(33, 0, 32, 32)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.update(0, 0, 1, 1)

        self.feet = pygame.Rect(0, 0, 12, 12)
        self.old_position = self.position.copy()
        self.speed = 3

    # save last location (to return to if player collide a wall
    def save_location(self):
        self.old_position = self.position.copy()

    # save each animation of the player in an array
    def initializeanimation(self):
        self.animation_up.append((0, 96, 32, 32))
        self.animation_up.append((33, 96, 32, 32))
        self.animation_up.append((66, 96, 32, 32))

        self.animation_left.append((0, 32, 32, 32))
        self.animation_left.append((33, 32, 32, 32))
        self.animation_left.append((66, 32, 32, 32))

        self.animation_right.append((0, 64, 32, 32))
        self.animation_right.append((33, 64, 32, 32))
        self.animation_right.append((66, 64, 32, 32))

        self.animation_down.append((0, 1, 32, 32))
        self.animation_down.append((33, 0, 32, 32))
        self.animation_down.append((66, 1, 32, 32))

    # get animations
    def getAnimationUp(self, i):

        self.i = i
        self.facing = 8
        self.position[1] -= self.speed
        return self.animation_up[i]

    # get animations
    def getAnimationRight(self, i):
        self.i = i
        self.facing = 6
        self.position[0] += self.speed
        return self.animation_right[i]

    # get animations
    def getAnimationLeft(self, i):
        self.i = i
        self.facing = 4
        self.position[0] -= self.speed
        return self.animation_left[i]

    # get animations
    def getAnimationDown(self, i):
        self.i = i
        self.facing = 2
        self.position[1] += self.speed
        return self.animation_down[i]

    # save the direction the player is facing (north east south west) to get animation to display if he stops moving
    def Facing(self):
        if self.facing == 2:
            return self.animation_down[1]
        if self.facing == 6:
            return self.animation_right[1]
        if self.facing == 4:
            return self.animation_left[1]
        if self.facing == 8:
            return self.animation_up[1]

    # update player position and rect
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # return to last known position if the player collides a wall
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
