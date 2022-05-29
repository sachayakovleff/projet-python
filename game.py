from pygame import mixer
from pygame import *
import pygame
import pyscroll
from pytmx.util_pygame import load_pygame

from player import Player
from monster import Monster


class Game:
    # game init
    def __init__(self):
        self.i = 0
        self.count = 0

        # load screen
        self.screen = pygame.display.set_mode((1550, 865))
        pygame.display.set_caption("Pygamon - adventure")

        # load map
        tmx_data = load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        # get player and monster positions on the map
        player_position = tmx_data.get_object_by_name("Player")
        monster_position = tmx_data.get_object_by_name("Monster")

        self.player = Player(player_position.x, player_position.y)
        self.monster = Monster(monster_position.x, monster_position.y)

        # get all collisions and interactions in the map loaded
        self.walls = []
        self.entries = []

        # initialize the collisions
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # add player and monster in pyscroll
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.monster)
        self.group.add(self.player)
        

        # get zone for changing map
        enter_sanctuary = tmx_data.get_object_by_name('enter_sanctuary')
        self.enter_sanctuary_rect = pygame.Rect(enter_sanctuary.x, enter_sanctuary.y, enter_sanctuary.width,
                                                enter_sanctuary.height)

        exit_sanctuary = load_pygame('sanctuary.tmx').get_object_by_name('exit_sanctuary')
        self.exit_sanctuary_rect = pygame.Rect(exit_sanctuary.x, exit_sanctuary.y, exit_sanctuary.width,
                                               exit_sanctuary.height)

    # get time frame for player animation
    def Handle_Count(self, count):
        i = 0
        if count < 20:
            i = 0
        if 20 <= count < 40:
            i = 1
        if 40 <= count < 60:
            i = 2
        return i

    # get key pressed
    def HandleKey(self, i):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.player.image = self.player.player_image.subsurface(self.player.getAnimationUp(i))
        if key[pygame.K_DOWN]:
            self.player.image = self.player.player_image.subsurface(self.player.getAnimationDown(i))
        if key[pygame.K_LEFT]:
            self.player.image = self.player.player_image.subsurface(self.player.getAnimationLeft(i))
        if key[pygame.K_RIGHT]:
            self.player.image = self.player.player_image.subsurface(self.player.getAnimationRight(i))
        if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False and key[pygame.K_UP] == False and key[
            pygame.K_DOWN] == False:
            self.player.image = self.player.player_image.subsurface(self.player.Facing())
        self.player.rect = self.player.image.get_rect()

    # Load sanctuary map
    def switch_sanctuary(self):
        tmx_data = load_pygame('sanctuary.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        self.walls = []
        self.entries = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        exit_sanctuary = tmx_data.get_object_by_name('exit_sanctuary')
        self.exit_sanctuary_rect = pygame.Rect(exit_sanctuary.x, exit_sanctuary.y, exit_sanctuary.width,
                                               exit_sanctuary.height)

        spawn_enter_sanctuary = tmx_data.get_object_by_name('spawn_sanctuary')
        self.player.position[0] = spawn_enter_sanctuary.x
        self.player.position[1] = spawn_enter_sanctuary.y - 20

    # Load world map
    def switch_world(self):
        tmx_data = load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 4

        self.walls = []
        self.entries = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)
        self.exit_sanctuary_rect = pygame.Rect(0, 0, 0, 0)
        enter_sanctuary = tmx_data.get_object_by_name('enter_sanctuary')
        self.enter_sanctuary_rect = pygame.Rect(enter_sanctuary.x, enter_sanctuary.y, enter_sanctuary.width,
                                                enter_sanctuary.height)

        spawn_exit_sanctuary = tmx_data.get_object_by_name('spawn_exit_sanctuary')
        self.player.position[0] = spawn_exit_sanctuary.x - 5
        self.player.position[1] = spawn_exit_sanctuary.y - 20

    # Update the collisions
    def update(self):
        self.group.update()

        if self.player.feet.colliderect(self.enter_sanctuary_rect):
            self.switch_sanctuary()

        if self.player.feet.colliderect(self.exit_sanctuary_rect):
            self.switch_world()

        for wall in self.walls:
            if self.player.feet.colliderect(wall):
                self.player.move_back()

    # Start the game
    def run(self):
        # game setup
        running = True

        clock = pygame.time.Clock()

        self.count = 0
        self.i = 0

        mixer.init()
        mixer.music.load('South Hyrule Field.mp3')
        mixer.music.play(loops=2)
        mixer.music.set_volume(0.20)
        # Game Loop
        while running:
            self.player.save_location()
            self.count += 1
            if self.count > 60:
                self.count = 0
            self.HandleKey(self.Handle_Count(self.count))
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
