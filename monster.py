import pygame


## faire bouger le monstre
## le faire despawn quand self.health = 0
## approcher le joueur quand il est dans la zone du monster ou faire un monster qui lance un projectile sur une ligne
## mettre une probabilité qui lache un rubis
## (donc trouver un sprite rubis)
## faire une bourse pour le player (compteur)
## (Bonus) lancer une musique d'affrontement quand tu entres dans la zone du monster
## musique quand tu empoches un rubis
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.position = [x, y]
        self.health = 100
        self.max_health = 100
        self.attack = 5
        self.image = pygame.image.load("Monster.png").convert_alpha()
        self.image.set_colorkey([0, 0, 0])
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        #self.image = self.image.subsurface(self.rect)

        self.feet = pygame.Rect(0, 0, 12, 12)
        self.old_position = self.position.copy()



    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
