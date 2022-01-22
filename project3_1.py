import os
import sys
import pygame
from pygame.locals import *
import math
import time
from mpi4py import MPI

#cluster
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


os.environ['DISPLAY'] = ':0.0'
os.system('caffeinate sleep 1')

red = (255,0,0)
black = (0,0,0)
white = (255,255,255)
screen = pygame.display.set_mode((screen_size),pygame.NOFRAME)
font = pygame.font.SysFont('Calibri',250,True, False)
font2 = pygame.font.SysFont('Helvetica',300,True, False)

#animation images on pi2
class MySprite1(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite1, self).__init__()

        self.images = []
        self.images.append(pygame.image.load('closed.jpg'))
        self.images.append(pygame.image.load('open.jpg'))
        self.images.append(pygame.image.load('fully_opened.jpg'))

        self.images.append(pygame.image.load('closed_door.jpg'))
        self.images.append(pygame.image.load('opned_door.jpg'))
        self.images.append(pygame.image.load('closed_door.jpg'))

        self.images.append(pygame.image.load('glitched_open.jpg'))
        self.images.append(pygame.image.load('glitched_open_2.jpg'))
        self.images.append(pygame.image.load('glitched_fully_opened_2.jpg'))
        self.images.append(pygame.image.load('glitched_fully_opened.jpg'))


        self.images.append(pygame.image.load('glitched_closed_door_2.jpg'))
        self.images.append(pygame.image.load('glitched_closed_door.jpg'))
        self.images.append(pygame.image.load('glitched_opned_door_2.jpg'))
        self.images.append(pygame.image.load('glitched_opned_door_3.jpg'))


        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],(1000,1000))
        self.index = 0
        self.rect = self.images[0].get_rect()


    def update(self):
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]

#animation images class on pi4
class MySprite2(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite2, self).__init__()

        self.images = []
        self.images.append(pygame.image.load('zoom.png'))
        self.images.append(pygame.image.load('glitched_zoom.png'))
        self.images.append(pygame.image.load('glitched_zoom0.png'))
        self.images.append(pygame.image.load('glitched_zoom1.png'))
        self.images.append(pygame.image.load('glitched_zoom2.png'))
        self.images.append(pygame.image.load('glitched_zoom3.png'))
        self.images.append(pygame.image.load('glitched_zoom4.png'))
        self.images.append(pygame.image.load('glitched_zoom5.png'))

        disp_info = pygame.display.Info()
        width = disp_info.current_w
        height = disp_info.current_h

        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],(1000,1000))
        self.index = 0
        self.rect = self.images[0].get_rect()

    def update(self):
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]

#pygame main
pygame.init()
my_sprite1 = MySprite1()
my_sprite2 = MySprite2()
my_group1 = pygame.sprite.Group(my_sprite1)
my_group2 = pygame.sprite.Group(my_sprite2)
clock = pygame.time.Clock()
running = True
PI = math.pi

#set up pygame screen
disp_info = pygame.display.Info()
width = disp_info.current_w
height = disp_info.current_h
screen_size = (width,height)

#set up animation frame
frame_count = 0
frame_rate = 60
day = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            running = False
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        for i in range(2000):
            screen.fill((255,255,255))
            if rank == 0:
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

                total_seconds = frame_count // frame_rate

                hours = total_seconds // 3600 % 24

                minutes = total_seconds // 60 % 60

                seconds = total_seconds % 60

                output_string = "Time: {0:02}:{1:02}:{2:02}".format(hours, minutes, seconds)
                text = font.render(output_string, True, white)
                screen.blit(text,[600,400])

                frame_count += 720
                clock.tick(frame_rate)

                pygame.display.update()
            elif rank == 1:
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                my_group1.update()
                screen.fill(black)
                clock.tick(5)
                text = font2.render("20",True,red)
                screen.blit(text,[200,200])
                pygame.display.update()
                my_group1.draw(screen)
                pygame.display.update()
                clock.tick(1)
            elif rank == 2:
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                my_group2.update()
                screen.fill(black)
                my_group2.draw(screen)
                pygame.display.update()
                clock.tick(1)
            else:
                os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                screen.fill(white)

                number = frame_count // frame_rate
                output_string = "Cases: {}".format(number)

                text = font.render(output_string, True, black)
                screen.blit(text, [200, 400])

                frame_count += 1 * (2 ** (day))
                day += 0.002

                #quit program when number hit 1 billion
                max = 1000000000000

                if frame_count >= max:
                    screen.fill(BLACK)
                    pygame.display.update()
                    break
            running = False


pygame.quit()
