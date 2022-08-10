from os import environ
# disable hello message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pong import PongGame

def main():
    pygame.init()
    
    # create display object - window with given size
    screen = pygame.display.set_mode((800,600))
       
    # set that window's title
    pygame.display.set_caption("Pong")
    
    # create game object 
    game = PongGame()
    
    # time stuff
    gameClock = pygame.time.Clock()
    deltaTime = 0
    
    # player input
    player_input = 0
    
    IsRunning = True 
    while IsRunning:
        
        # time in secounds how much time paddes since previous frame
        deltaTime = (gameClock.get_time()/1000)
        
        # iterate through pygame's events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IsRunning = False
                return
        # handle input 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player_input = -1
        elif keys[pygame.K_DOWN]:
            player_input = 1
        else:
            player_input = 0
        
        
        #
        out = game.process_frame(screen,
                           deltaTime,
                           player_input,
                           -1 if game.paddle1.y > game.ball.y else 1)
    
        
        # update screen
        pygame.display.update()
        
        gameClock.tick(240)

if __name__ == "__main__":
    main()