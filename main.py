import pygame
import button
import sys
pygame.font.init()

screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption('Chess Game')


#load button images
img = pygame.image.load('startbutton.png').convert_alpha()
textfont=pygame.font.SysFont("monospace", 50)
#create button instances
start_button = button.Button(450, 450, img, 0.8)

#game loop
run = True
while run:
    screen.fill((202, 228, 241))

    if start_button.draw(screen):
	    print('Welcome to the Chess Game')
    #event handler
    for event in pygame.event.get():
#quit game
	    if event.type == pygame.QUIT:
		    run = False
    textTBD=textfont.render("Welcome to the chess game:)", 1, (255,255,255))
    screen.blit(textTBD,(100,100))

    pygame.display.update()

pygame.quit()