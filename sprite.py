import pygame as pg
from setting import *


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(HERO_RIGHT_RUN+"hero_result.png")
        self.run_right_animation = ["hero_run_0_result.png", "hero_run_1_result.png", "hero_run_2_result.png", "hero_run_3_result.png",
                                    "hero_run_4_result.png", "hero_run_5_result.png", "hero_run_6_result.png", "hero_run_7_result.png", "hero_run_8_result.png",
                                    "hero_run_9_result.png", "hero_run_10_result.png", "hero_run_11_result.png", "hero_run_12_result.png", "hero_run_13_result.png",
                                    "hero_run_14_result.png", "hero_run_15_result.png", "hero_run_16_result.png", "hero_run_17_result.png", "hero_run_18_result.png", ]

        self.run_left_animation = ["hero_run_0.png", "hero_run_1.png", "hero_run_2.png", "hero_run_3.png",
                                   "hero_run_4.png", "hero_run_5.png", "hero_run_6.png", "hero_run_7.png", "hero_run_8.png",
                                   "hero_run_9.png", "hero_run_10.png", "hero_run_11.png", "hero_run_12.png", "hero_run_13.png",
                                   "hero_run_14.png", "hero_run_15.png", "hero_run_16.png", "hero_run_17.png", "hero_run_18.png"]

        self.jump_right_animation = ["hero_jump_1_result", "hero_jump_2_result", "hero_jump_3_result", "hero_jump_4_result", "hero_jump_5_result",
                                     "hero_jump_6_result", "hero_jump_7_result", "hero_jump_8_result", "hero_jump_9_result", "hero_jump_10_result", "hero_jump_10_result", "hero_jump_1_result",
                                     "hero_jump_11_result", "hero_jump_12_result", "hero_jump_13_result", "hero_jump_14_result", "hero_jump_15_result", "hero_jump_16_result"]

        self.jump_left_animation = ["hero_jump_1", "hero_jump_2", "hero_jump_3", "hero_jump_4", "hero_jump_5", "hero_jump_6", "hero_jump_7", "hero_jump_8", "hero_jump_9", "hero_jump_10", "hero_jump_11",
                                    "hero_jump_12", "hero_jump_13", "hero_jump_14", "hero_jump_15", "hero_jump_16"]

        self.death_animation_left = ["hero_death_0.png", "hero_death_1.png", "hero_death_2.png", "hero_death_3.png", "hero_death_4.png", "hero_death_5.png", "hero_death_6.png",
                                     "hero_death_7.png", "hero_death_8.png", "hero_death_8.png", "hero_death_10.png", "hero_death_11.png", "hero_death_12.png", "hero_death_13.png",
                                     "hero_death_14.png", "hero_death_15.png", "hero_death_16.png", ]
        self.jump_sound = pg.mixer.Sound("sound/hero/jump/Jump.wav")
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.game = game
        self.rect = self.image.get_rect()
        self.vx = 0
        self.vy = 0
        self.vertical_momentum = 0
        self.air_timer = 0
        self.health = 200
        self.last_update = pg.time.get_ticks()
        self.last_update_jump = pg.time.get_ticks()
        self.sense = True

    def set_pos(self, x, y):
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def collision_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tiles):
        collision_types = {'top': False, 'bottom': False,
                           'right': False, 'left': False}
        self.rect.x += self.vx
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.vx > 0:
                self.rect.right = tile.rect.left
                collision_types['right'] = True
            elif self.vx < 0:
                self.rect.left = tile.rect.right
                collision_types['left'] = True
        self.rect.y += self.vy
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.vy > 0:
                self.rect.bottom = tile.rect.top
                collision_types['bottom'] = True
            elif self.vy < 0:
                self.rect.top = tile.rect.bottom
                collision_types['top'] = True

        return collision_types

    def run_right_anim(self, collision):
        if self.air_timer < 6:
            self.image = pg.image.load(
                HERO_RIGHT_RUN+self.run_right_animation[self.i])
            if self.i+1 == len(self.run_right_animation):
                self.i = 0
            self.i += 1
        elif collision['bottom'] == False:
            self.image = pg.image.load(HERO_RIGHT_JUMP+"hero_jump_15_result.png")


    def run_left_anim(self, collision):
        if self.air_timer < 6:
            self.image = pg.image.load(
                HERO_LEFT_RUN+self.run_left_animation[self.j])
            if self.j+1 == len(self.run_left_animation):
                self.j = 0
            self.j += 1
        elif collision['bottom'] == False:
            self.image = pg.image.load(HERO_LEFT_JUMP+"hero_jump_15.png")

    def jump_right_anim(self):
        if self.air_timer < 6:
            self.image = pg.image.load(
                HERO_RIGHT_JUMP+self.jump_right_animation[self.k]+".png")
            self.k += 1
            if self.k == len(self.jump_right_animation):
                self.k -= 1

    def jump_left_anim(self):
        if self.air_timer < 6:
            self.image = pg.image.load(
                HERO_LEFT_JUMP+self.jump_left_animation[self.l]+".png")
            self.l += 1
            if self.l == len(self.jump_left_animation):
                self.l -= 1
            

    def death_anim(self):
        pass

    def control(self):
        self.vx = 0
        self.vy = 0
        keys = pg.key.get_pressed()
        now = pg.time.get_ticks()
        if now - self.last_update > 40:
            collisions = self.move(self.game.current_level.platform_list)
            self.last_update = now
            if keys[pg.K_LEFT]:
                self.vx -= 13.4
                self.sense = False
                self.run_left_anim(collisions)
            elif self.air_timer < 6 and self.sense == False and not keys[pg.K_LEFT]:
                self.image = pg.image.load(HERO_LEFT_RUN+"hero.png")

            if keys[pg.K_RIGHT]:
                self.vx += 13.4
                self.sense = True
                self.run_right_anim(collisions)
            elif self.air_timer < 6 and self.sense == True and not keys[pg.K_RIGHT]:
                self.image = pg.image.load(HERO_RIGHT_RUN+"hero_result.png")
            if keys[pg.K_SPACE]:
                if self.air_timer < 6:
                    self.vertical_momentum = -13
                    self.jump_sound.set_volume(0.2)
                    self.jump_sound.play()
                if self.sense == True:
                    self.jump_right_anim()
                elif self.sense == False:
                    self.jump_left_anim()

    def update(self):
        self.vy += self.vertical_momentum
        self.vertical_momentum += 0.5
        if self.vertical_momentum > 8:
            self.vertical_momentum = 8
        collisions = self.move(self.game.current_level.platform_list)

        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("image/explosion/explosion1.png")
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.meteor_image_liste = ["image/explosion/explosion1.png", "image/explosion/explosion2.png", "image/explosion/explosion3.png", "image/explosion/explosion4.png",
                                   "image/explosion/explosion5.png"]
        self.explosion_sound = pg.mixer.Sound("sound/explosion/Explosion3.wav")
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            now = self.last_update
            self.frame += 1
            if self.frame == len(self.meteor_image_liste):
                self.kill()
                self.game.game_over = True
            else:
                center = self.rect.center
                self.image = pg.image.load(self.meteor_image_liste[self.frame])
                self.rect = self.image.get_rect()
                self.rect.center = center

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y,game):
        super().__init__()
        self.game = game
        self.attack = 25
        self.image = pg.image.load("image/bullet/fire.png")
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.type ="bullet"
        self.vx = 0
        self.vy = 5
    def update(self):
        self.rect.y -= self.vy
        if self.game.player.vx > 0 and self.game.player.rect.right == 685 and self.game.current_level.world_shift+SCREEN_WIDTH/2+20 < self.game.current_level.map.width:
            self.rect.x -= self.game.player.vx
            print(self.game.player.rect.right)
        if self.rect.bottom < 0:
            self.kill()
            

class Bullet2(pg.sprite.Sprite):
    def __init__(self, x, y,game):
        super().__init__()
        self.game = game
        self.attack = 25
        self.image = pg.image.load("image/bullet/fire_left.png")
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.type ="bullet"
        self.vx = 5
        self.vy = 0
    def update(self):
        self.rect.x -= self.vx
        if self.game.player.vx > 0 and self.game.player.rect.right == 685 and self.game.current_level.world_shift+SCREEN_WIDTH/2+20 < self.game.current_level.map.width:
            self.rect.x -= self.game.player.vx
            print(self.game.player.rect.right)
        if self.rect.right < 0:
            self.kill()
            

class Mob1(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.attack = 25
        self.image = pg.image.load("image/mob/mob1_left/mob1_flip.png")
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.type ="mob1"
        self.vx = 0
        self.vy = 0
        self.enable = False
        self.counter = 0
        self.direction = False
    def move(self):
        self.rect.x += self.vx
        if self.direction == False: 
            self.vx = 3
            self.counter +=1
            if self.counter == 200: 
                self.direction = True
        elif self.direction == True:
            self.vx = -3
            self.counter -=1  
            if self.counter == 0: 
                self.direction = False
class Mob2:
    def __init__(self, x, y):
        super().__init__()
        self.attack = 25
        self.image = pg.image.load("image/mob/mob1_left/mob2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.type ="mob2"
        self.vx = 0
        self.vy = 0
        self.enable = False
        self.counter = 0
        self.direction = False

class Trap(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("image/platform/trap/trap.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.type = "trap"
        self.y = y
        self.rect.x = x * TILESIZE 
        self.rect.y = y * TILESIZE + 14
    def move(self):
        pass

class Totem(pg.sprite.Sprite):
    def __init__(self, x, y,game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("image/mob/totem/totem.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.type = "totem"
        self.y = y
        self.rect.x = x * TILESIZE - 18
        self.rect.y = y * TILESIZE - 94
        self.last_update = pg.time.get_ticks()
    def move(self):
        now = pg.time.get_ticks()
        self.bullet = Bullet(self.rect.centerx-14,self.rect.centery,self.game)
        if now-self.last_update > 2000:
            self.last_update = now
            self.game.bullet.add(self.bullet)
            self.game.all_sprites.add(self.bullet)
        hit = pg.sprite.spritecollide(self.game.player,self.game.bullet, False)
        if hit:
            self.game.player.kill()
            self.expl = Explosion(self.game.player.rect.center,self.game)
            self.expl.explosion_sound.play()
            self.expl.update()
            self.game.all_sprites.add(self.expl)

  
class Mask(pg.sprite.Sprite):
    def __init__(self, x, y,game):
        super().__init__()
        self.game = game
        self.image = pg.image.load("image/mob/mask/mask.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.type = "totem"
        self.y = y
        self.rect.x = x * TILESIZE - 16
        self.rect.y = y * TILESIZE - 32
        self.last_update = pg.time.get_ticks()
    def move(self):
        now = pg.time.get_ticks()
        self.bullet = Bullet2(self.rect.centerx-14,self.rect.centery,self.game)
        if now-self.last_update > 2000:
            self.last_update = now
            self.game.bullet.add(self.bullet)
            self.game.all_sprites.add(self.bullet)
        hit = pg.sprite.spritecollide(self.game.player,self.game.bullet, False)
        if hit:
            self.game.player.kill()
            self.expl = Explosion(self.game.player.rect.center,self.game)
            self.expl.explosion_sound.play()
            self.expl.update()
            self.game.all_sprites.add(self.expl)          
       
    
        
class Ground(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("image/platform/ground/ground.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wood(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("image/platform/ground/wood.png")
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("image/platform/portal/portal.png")
        self.image = pg.transform.scale(self.image,(TILESIZE*3,TILESIZE*3))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE - 32
        self.rect.y = y * TILESIZE - 64

class Coin(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("image/platform/coin/coin.png")
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.coin_sound = pg.mixer.Sound("sound/coin/Coin.wav")
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE  
        self.rect.y = y * TILESIZE 
    def music(self):
        self.coin_sound.set_volume(0.2)
        self.coin_sound.play()