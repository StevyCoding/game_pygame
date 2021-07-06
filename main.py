import pygame as pg
import sys
import os
from sprite import *
from setting import *
from level import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        size = [SCREEN_WIDTH, SCREEN_HEIGHT]
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption("welekeo")

    def new(self):
        self.player = Player(self)

        # Create all the levels
        self.level_list = [Level_03(self.player,self),Level_02(self.player,self),Level_03(self.player,self)]
        # Set the current level
        self.current_level_no = 0
        self.current_level = self.level_list[self.current_level_no]
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        #variable to manage bullet spam and collision
        self.bullet_last_update = pg.time.get_ticks()
        self.bullet = pg.sprite.Group()
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            

    def mob_attack(self):
        for ennemy in self.current_level.enemy_list:
            ennemy.move()      
            if ennemy.rect.colliderect(self.player):
                self.player.kill()
                ennemy.kill()
                self.expl = Explosion(self.player.rect.center,self)
                self.expl2 = Explosion(ennemy.rect.center,self)
                self.expl.explosion_sound.play()
                self.all_sprites.add(self.expl)
                self.all_sprites.add(self.expl2)
                self.expl.update()
    def change_level(self):
        for portal in self.current_level.portal_list:
            if portal.rect.colliderect(self.player):
                self.score += 1000
                self.current_level_no +=1
                self.current_level =  self.level_list[self.current_level_no]
                Level_01(self.player,self)
                Level_02(self.player,self)
                Level_03(self.player,self)
                self.current_level.music()
    def scoring(self):
        for coin in self.current_level.coin_list:
            if coin.rect.colliderect(self.player):
                coin.music()
                coin.kill()
                self.score += 25
    def draw_text(self,surf,text,size,x,y):
        self.font_name =pg.font.match_font('arial')
        self.font = pg.font.Font(self.font_name,size)
        self.text_surface = self.font.render(text,True,BLACK)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midtop = (x,y)
        surf.blit(self.text_surface,self.text_rect)
    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(WHITE)
        self.draw_text(self.screen,"welekeo author: Steve Nono-Womdim", 48, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text(self.screen,"Arrows to move, Space to jump", 22,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text(self.screen,"Press a key to play", 22,SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    
    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(WHITE)
        self.draw_text(self.screen,"GAME OVER",64,SCREEN_WIDTH/2,SCREEN_HEIGHT/4)
        self.draw_text(self.screen,"arrow key to move and space to jump",22,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.draw_text(self.screen,"pressed a key to begin",22,SCREEN_WIDTH/2,SCREEN_HEIGHT*3/4)
        self.draw_text(self.screen,"your score "+str(self.score),22,SCREEN_WIDTH/2,SCREEN_HEIGHT*3/5)
        pg.display.flip()
        while self.game_over == True:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over = False
                    self.running = False
                if event.type == pg.KEYUP:
                    self.game_over= False
                    self.new()
                    self.current_level.music()
                    self.score=0
    
    def wait_for_key(self):
        waiting = True
        while waiting :
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    def run(self):
        self.new()
        self.show_start_screen()
        self.current_level.music()
        while self.running:
            self.clock.tick(60)
            self.event()
            self.player.control()
            self.mob_attack()
            self.current_level.update()
            self.all_sprites.update()
            self.screen.blit(self.current_level.loadBG,self.current_level.loadBG_rect)
            self.draw_text(self.screen,str(self.score),40,SCREEN_WIDTH/2,10)
            self.all_sprites.draw(self.screen)
            self.current_level.draw(self.screen)
            #self.draw_grid()
            self.change_level()
            self.scoring()
            pg.display.flip()
            if self.game_over:
                self.show_go_screen()

    def quit(self):
        if not self.running:
            pg.quit()
            sys.exit()


game = Game()
game.run()
game.quit()