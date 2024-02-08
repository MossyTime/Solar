import sys
import pygame
from scripts.entities import PhysicsEntity
import random
from time import sleep

pygame.mixer.init()
pygame.mixer_music.load("Sol/data/ambience.mp3")
pygame.mixer.music.play(-1)
shoot_sound=pygame.mixer.Sound("Sol/data/beam_shoot.mp3")

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Solarr")
        self.screen=pygame.display.set_mode((1000,500))

        self.bg=pygame.image.load("Sol/data/background_1.png")

        self.clock=pygame.time.Clock()

        self.movement=[False,False]

        self.can_shoot=True

        self.rain_x=800

        self.rain=pygame.image.load("Sol/data/rain.png")
        self.rain=pygame.transform.scale(self.rain,(100,100))

        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface=self.my_font.render('You Murdered The Cloud. I Hope You Feel Good About Yourself.', False, (0, 0, 0))

        self.boss_health=[]
        for i in range(30):
            self.boss_health.append(1)

        self.text_hp=self.my_font.render("Cloud HP:"+str(len(self.boss_health)), False, (0, 0, 0))

        self.a_cloud=[]

        self.laser=pygame.image.load("Sol/data/beam_laser.png")
        self.beam=pygame.transform.scale(self.laser,(100,100))

        self.cloud=pygame.image.load("Sol/data/cloud.png")
        
        self.assets={
            "player":pygame.image.load("Sol/data/sun.png")
        }

        self.play_charge=True

        self.player=PhysicsEntity(self,"player",(-100,250),(50,50))

        self.collision_up=pygame.Rect(0,0,1000,10)
        self.collision_down=pygame.Rect(0,490,1000,10)
        self.collision_player=pygame.Rect((self.player.pos[0],self.player.pos[1]),(100,100))
        self.collision_laser=pygame.Rect((self.player.pos),(100,100))
        self.collision_rain=pygame.Rect(0,0,0,0)

    def shoot(self):
        laser_x=100
        for i in range(10):
            self.screen.blit(self.beam,(laser_x,self.player.pos[1]+100))
            laser_x+=100

    def run(self):
        while True:

            self.text_hp=self.my_font.render("Cloud HP:"+str(len(self.boss_health)), False, (0, 0, 0))
            self.screen.blit(self.text_hp,(0,0))
            pygame.display.flip()

            self.le_time=int(pygame.time.get_ticks()/1000)

            self.screen.fill((0,0,0))
            self.screen.blit(self.bg,(0,0))
            self.player.update((0,self.movement[1]*5-self.movement[0]*5))
            self.player.render(self.screen)

            self.collision_player=pygame.Rect((100,self.player.pos[1]+120),(50,50))

            if self.a_cloud==[]:
                self.a_cloud.append(1)
                self.cloud_y=random.randint(0,300)
                self.screen.blit(self.cloud,(800,self.cloud_y))
                self.collision_cloud=pygame.Rect((800,self.cloud_y),(50,50))

            elif pygame.Rect.colliderect(self.collision_laser,self.collision_cloud):
                self.a_cloud=[]
                self.collision_laser=pygame.Rect((100,self.player.pos[1]),(50,50))
                self.boss_health.pop()

                if self.boss_health==[]:
                    while True:
                        self.screen.blit(self.text_surface, (0,0))
                        pygame.display.flip()

                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                pygame.quit()
                                sys.exit()
            else:
                self.screen.blit(self.cloud,(800,self.cloud_y))
                self.collision_cloud=pygame.Rect((800,self.cloud_y),(50,50))
                self.collision_laser=pygame.Rect((100,self.player.pos[1]),(50,50))
        
            if self.le_time%2==0:
                self.screen.blit(self.rain,(self.rain_x,self.cloud_y+50))
                self.collision_rain=pygame.Rect((self.rain_x,self.cloud_y+100),(50,50))
                self.rain_x-=25
            else:
                self.rain_x=800  
            
            if pygame.Rect.colliderect(self.collision_player,self.collision_rain):
                self.text_surface=self.my_font.render('You Just Got Murdered By A Cloud Lmao.', False, (0, 0, 0))
                while True:
                        self.screen.blit(self.text_surface, (0,0))
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                
           
            if pygame.Rect.colliderect(self.collision_player,self.collision_up):
                pygame.draw.rect(self.screen,(0,0,250),self.collision_up)
                self.player.pos[1]+=20
            else:
                pygame.draw.rect(self.screen,(0,150,150),self.collision_up)

            if pygame.Rect.colliderect(self.collision_player,self.collision_down):
                pygame.draw.rect(self.screen,(0,0,250),self.collision_down)
                self.player.pos[1]-=20
            else:
                pygame.draw.rect(self.screen,(0,150,150),self.collision_down)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_w:
                        self.movement[0]=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_s:
                        self.movement[1]=True
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_w:
                        self.movement[0]=False
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_s:
                        self.movement[1]=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        if self.can_shoot==True:
                            self.collision_laser=pygame.Rect((100,self.player.pos[1]),(1000,100))
                            pygame.mixer.Sound.play(shoot_sound)
                            self.shoot()
            
            pygame.display.update()
            self.clock.tick(60)

        pygame.font.init()
Game().run()
