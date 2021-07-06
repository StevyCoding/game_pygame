import pygame as pg
from os import path
from setting import *
from sprite import *
from map import Map
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self,player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.portal_list = pg.sprite.Group()
        self.coin_list = pg.sprite.Group()
        self.player = player
        # How far this world has been scrolled left/right
        self.world_shift = SCREEN_WIDTH/2
        self.background = []

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.coin_list.update()
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.coin_list.draw(screen)
        self.portal_list.draw(screen)
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
    
    def __init__(self, player, game):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        self.game = game
        self.level_limit = -1000
        self.map = Map('level_map/level.txt')
        self.background = ['image/platform/background/savanna.png']
        self.loadBG = pg.image.load(self.background[0])
        self.loadBG_rect =self.loadBG.get_rect()
        self.loadBG_rect.x = self.loadBG_rect.x-self.player.vx
        self.loadBG_rect.y = self.loadBG_rect.y
    # initialize all variables and do all the setup for a new game
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'O':
                    portal = Portal(col,row)
                    self.portal_list.add(portal)
                if tile == '2':
                    ground = Ground(col,row)
                    self.platform_list.add(ground)
                if tile == '1':
                    wood = Wood(col,row)
                    self.platform_list.add(wood)
                if tile == 'P':
                    self.player.set_pos(col,row)
                if tile == 'M':
                    mob1 = Mob1(col,row)
                    self.enemy_list.add(mob1)
                if tile == 'T':
                    trap = Trap(col,row)
                    self.enemy_list.add(trap)
                if tile == 'Y':
                    totem = Totem(col,row,self.game)
                    self.enemy_list.add(totem)
                if tile == 'C':
                    coin = Coin(col,row)
                    self.coin_list.add(coin)
                if tile == 'L':
                    mask = Mask(col,row,self.game)
                    self.enemy_list.add(mask)                

    def update(self):
        if self.player.vx > 0 and self.player.rect.right >= SCREEN_WIDTH/2 and self.player.rect.right < SCREEN_WIDTH:
            self.world_shift += self.player.vx

        if self.player.rect.left < 0:
            self.player.rect.left= 0
        if self.player.rect.right > SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2+20 < self.map.width :
            self.player.rect.right = SCREEN_WIDTH/2
        elif self.player.rect.right>SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH

        if self.player.vx > 0 and self.player.rect.right == SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2 < self.map.width :
            for element in self.enemy_list:
                element.rect.x -= self.player.vx
            for element in self.platform_list:
                element.rect.x -= self.player.vx
            for coin in self.coin_list:
                coin.rect.x -= self.player.vx
            for portal in self.portal_list:
                portal.rect.x -= self.player.vx           
    def music(self):
            pg.mixer.music.load("sound/music/level1_music.mp3")
            pg.mixer.music.set_volume(0.4)
            pg.mixer.music.play(-1) 
    
    
# Create platforms for the level
class Level_02(Level):
    def __init__(self, player, game):
        # Call the parent constructor
        Level.__init__(self, player)
        self.game = game
        self.map = Map('level_map/level2.txt')
        self.loadBG = pg.image.load('image/platform/background/desert.jpg')
        self.loadBG = pg.transform.scale(self.loadBG,(1344,675))
        self.loadBG_rect =self.loadBG.get_rect()
        self.loadBG_rect.x = self.loadBG_rect.x-self.player.vx
        self.loadBG_rect.y = self.loadBG_rect.y
    # initialize all variables and do all the setup for a new game
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '2':
                    ground = Ground(col,row)
                    self.platform_list.add(ground)
                if tile == '1':
                    wood = Wood(col,row)
                    self.platform_list.add(wood)
                if tile == 'P':
                    self.player.set_pos(col,row)
                if tile == 'M':
                    mob1 = Mob1(col,row)
                    self.enemy_list.add(mob1)
                if tile == 'T':
                    trap = Trap(col,row)
                    self.enemy_list.add(trap)
                if tile == 'O':
                    portal = Portal(col,row)
                    self.portal_list.add(portal)
                if tile == 'Y':
                    totem = Totem(col,row,self.game)
                    self.enemy_list.add(totem)
                if tile == 'C':
                    coin = Coin(col,row)
                    self.coin_list.add(coin)
                if tile == 'L':
                    mask = Mask(col,row,self.game)
                    self.enemy_list.add(mask)                                   

    def update(self):
        if self.player.vx > 0 and self.player.rect.right >= SCREEN_WIDTH/2:
            self.world_shift += self.player.vx

        if self.player.rect.left < 0:
            self.player.rect.left= 0
        if self.player.rect.right > SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2 < self.map.width :
            self.player.rect.right = SCREEN_WIDTH/2
        elif self.player.rect.right>SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH

        if self.player.vx > 0 and self.player.rect.right == SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2+20 < self.map.width :
            for element in self.enemy_list:
                element.rect.x -= self.player.vx
            for element in self.platform_list:
                element.rect.x -= self.player.vx
            for coin in self.coin_list:
                coin.rect.x -= self.player.vx 
            for portal in self.portal_list:
                portal.rect.x -= self.player.vx           
    def music(self):
            pg.mixer.music.load("sound/music/level2_music.mp3")
            pg.mixer.music.set_volume(0.4)
            pg.mixer.music.play(-1) 

class Level_03(Level):
    def __init__(self, player, game):
        # Call the parent constructor
        Level.__init__(self, player)
        self.game = game
        self.map = Map('level_map/level3.txt')
        self.loadBG = pg.image.load('image/platform/background/sky.jpg')
        self.loadBG = pg.transform.scale(self.loadBG,(1344,608))
        self.loadBG_rect =self.loadBG.get_rect()
        self.loadBG_rect.x = self.loadBG_rect.x-self.player.vx
        self.loadBG_rect.y = self.loadBG_rect.y
    # initialize all variables and do all the setup for a new game
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '2':
                    ground = Ground(col,row)
                    self.platform_list.add(ground)
                if tile == '1':
                    wood = Wood(col,row)
                    self.platform_list.add(wood)
                if tile == 'P':
                    self.player.set_pos(col,row)
                if tile == 'M':
                    mob1 = Mob1(col,row)
                    self.enemy_list.add(mob1)
                if tile == 'T':
                    trap = Trap(col,row)
                    self.enemy_list.add(trap)
                if tile == 'O':
                    portal = Portal(col,row)
                    self.portal_list.add(portal)
                if tile == 'Y':
                    totem = Totem(col,row,self.game)
                    self.enemy_list.add(totem)
                if tile == 'C':
                    coin = Coin(col,row)
                    self.coin_list.add(coin)
                if tile == 'L':
                    mask = Mask(col,row,self.game)
                    self.enemy_list.add(mask)                
    def update(self):
        if self.player.vx > 0 and self.player.rect.right >= SCREEN_WIDTH/2:
            self.world_shift += self.player.vx

        if self.player.rect.left < 0:
            self.player.rect.left= 0
        if self.player.rect.right > SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2 < self.map.width :
            self.player.rect.right = SCREEN_WIDTH/2
        elif self.player.rect.right>SCREEN_WIDTH:
            self.player.rect.right = SCREEN_WIDTH

        if self.player.vx > 0 and self.player.rect.right == SCREEN_WIDTH/2 and self.world_shift+SCREEN_WIDTH/2+20 < self.map.width :
            for element in self.enemy_list:
                element.rect.x -= self.player.vx
            for element in self.platform_list:
                element.rect.x -= self.player.vx
            for coin in self.coin_list:
                coin.rect.x -= self.player.vx
            for portal in self.portal_list:
                portal.rect.x -= self.player.vx         
    def music(self):
            pg.mixer.music.load("sound/music/level3_music.mp3")
            pg.mixer.music.set_volume(0.4)
            pg.mixer.music.play(-1) 