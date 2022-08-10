from os import environ
# disable hello message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random
from dataclasses import dataclass

@dataclass
class GameInfo:
    player0_hits: int
    player1_hits: int
    player0_score: int
    player1_score: int

@dataclass
class Ball:
    MAX_VELOCITY_X = 800
    MAX_VELOCITY_Y = 600
    START_VEL_FACTOR_Y = .1
    
    COLOR = (255, 0, 0)
    x: float
    y: float
    
    diameter: int
    velocity_x: float
    velocity_y: float
    
    def reset(self, wnd_width, wnd_height):
        self.x = wnd_width//2
        self.y = wnd_height//2
        self.velocity_x = -Ball.MAX_VELOCITY_X
        self.velocity_y = Ball.START_VEL_FACTOR_Y * random.uniform(-Ball.MAX_VELOCITY_Y, Ball.MAX_VELOCITY_Y)
    
    def draw(self, display: pygame.Surface):
        pygame.draw.rect(display,
                        Ball.COLOR,
                        (int(self.x), int(self.y), self.diameter, self.diameter))
    
    def move(self, deltaTime: float):
        self.x += self.velocity_x * deltaTime
        self.y += self.velocity_y * deltaTime

@dataclass
class Paddle:
    VELOCITY = 500
    COLOR = (255, 255, 255)
    
    x: int
    y: int
    width: int
    height: int
    
    def reset(self, wnd_width, wnd_height):
        self.y = wnd_height //2 -self.height//2
    
    def draw(self, display: pygame.Surface):
        pygame.draw.rect(display,
                        Paddle.COLOR,
                        (self.x, self.y, self.width, self.height))
    
    def move(self, deltaTime: float, _input: int = -1|0|1):
        self.y -= deltaTime * Paddle.VELOCITY * _input; 
    
    def handle_collision(self, ball: Ball, paddle0: bool):
        #  AABB collision
        if(self.x < ball.x + ball.diameter and
            self.x + self.width > ball.x and
            self.y < ball.y + ball.diameter and
            self.y + self.height > ball.y):
            # bounce ball
            ball.velocity_x *= -1
            
            # reset x pos - avoid wall stuck
            if paddle0:
                ball.x = self.x + self.width
            else:
                ball.x = self.x - ball.diameter
            
            # get x position of objects centers
            ball_center = ball.y + (ball.diameter/2)
            paddle_center = self.y + (self.height/2)
            
            # calculate new velocity
            ball.velocity_y = ((ball_center - paddle_center) / (self.height/2)) * Ball.MAX_VELOCITY_Y
            
            return True
        return False
         
class PongGame:
    def __init__(self, window_width: int = 800, window_heigth: int = 600):
        import os
        
        # set variables 
        self.window_width = window_width
        self.window_height = window_heigth
        
        # init pygame libs
        pygame.init()
        pygame.freetype.init()
        
        # create pong background 
        self.background = pygame.Surface((window_width, window_heigth))
        self.background.fill((0,0,0, 255))
        
        STRIPES_LENGTH = 50
        STRIPES_WIDTH = 10
        STRIPES_MARGIN = 10
        
        # generate stripes
        for i in range(0, window_heigth // (STRIPES_LENGTH + STRIPES_MARGIN)):
            pygame.draw.rect(self.background,
                            (255,255,255, 255),
                            ((window_width - STRIPES_WIDTH)//2,
                            (STRIPES_LENGTH + STRIPES_MARGIN) * i,
                            STRIPES_WIDTH, STRIPES_LENGTH))
        
        # import nice pixel font if found
        if os.path.exists("assets/fonts/PressStart2P-Regular.ttf"):
            self.font = pygame.freetype.Font("assets/fonts/PressStart2P-Regular.ttf")
        else:
            self.font = pygame.font.SysFont("Verdana")
            
        # setting up paddles
        PADDLE_MARGIN = 10
        PADDLE_HEIGHT = 80
        PADDLE_WIDTH = 10
        self.paddle0 = Paddle(PADDLE_MARGIN,
                            (window_heigth - PADDLE_HEIGHT)//2,
                            PADDLE_WIDTH,
                            PADDLE_HEIGHT)
        self.paddle1 = Paddle(window_width - PADDLE_MARGIN - PADDLE_WIDTH,
                            (window_heigth-PADDLE_HEIGHT)//2,
                            PADDLE_WIDTH,
                            PADDLE_HEIGHT)
        
        # setup ball
        self.ball = Ball(window_width//2,
                        window_heigth//2,
                        20,
                        -Ball.MAX_VELOCITY_X,
                        Ball.START_VEL_FACTOR_Y*random.uniform(-Ball.MAX_VELOCITY_Y, Ball.MAX_VELOCITY_Y))
        
        # set game information
        self.player0_hits = 0
        self.player1_hits = 0
        self.player0_score = 0
        self.player1_score = 0

    def __reset_hits(self):
        self.player0_hits = 0
        self.player1_hits = 0

    def reset_obj(self):
        # reset ball
        self.ball.reset(self.window_width, self.window_height)
        self.paddle0.reset(self.window_width, self.window_height)
        self.paddle1.reset(self.window_width, self.window_height)
    
    def reset_stats(self):
        # reset game info
        self.player0_hits = 0
        self.player1_hits = 0
        self.player0_score = 0
        self.player1_score = 0

    def process_frame(self, display: pygame.Surface, deltaTime: float, input_0 = -1|0|1, input_1 = 1|0|1, drawHits: bool = False, drawScores: bool = True):
        
        # move paddles
        self.paddle0.move(deltaTime, input_0)
        self.paddle1.move(deltaTime, input_1)
        
        # clamp paddles y position to screen boundies
        self.paddle0.y = min(max(0, self.paddle0.y), self.window_height - self.paddle0.height)
        self.paddle1.y = min(max(0, self.paddle1.y), self.window_height - self.paddle1.height)
        
        # move ball
        self.ball.move(deltaTime)
        
        # check wall collision
        if(self.ball.y <= 0 or (self.ball.y + self.ball.diameter) >= self.window_height):
            # bounce ball
            self.ball.velocity_y *= -1
            
        # avoid wall stuck - clamp ball y
        self.ball.y = min(max(0, self.ball.y), self.window_height-self.ball.diameter)
        
        # check for paddles collisions    
        if self.paddle0.handle_collision(self.ball, True):
            self.player0_hits += 1 
        elif self.paddle1.handle_collision(self.ball, False):
            self.player1_hits += 1
        
        #region drawing
        # draw background
        display.blit(self.background, (0,0))
        
        # draw objects
        self.paddle0.draw(display)
        self.paddle1.draw(display)
        self.ball.draw(display)
        
        # draw number of hits
        if(drawHits):
            txt = str(self.player0_hits + self.player1_hits)
            
            # draw at center
            text_rect = self.font.get_rect(txt, size = 70)
            text_rect.topleft = ((self.window_width - text_rect.width)//2, 0)

            self.font.render_to(display, text_rect, txt, (255, 255, 255), (0, 0, 0), size = 70)
        
        if(drawScores):
            FONT_SIZE = 40
            # player0
            txt = str(self.player0_score)
            
            # draw at center
            text_rect = self.font.get_rect(txt, size =  FONT_SIZE)
            text_rect.topleft = (self.window_width//4 - text_rect.width//2, 0)
            
            # render txt
            self.font.render_to(display, text_rect, txt, (255,255,255), size =  FONT_SIZE)
            
            # player1
            txt = str(self.player1_score)
            
            # draw at center
            text_rect = self.font.get_rect(txt, size =  FONT_SIZE)
            text_rect.topleft = (self.window_width*.75- text_rect.width//2, 0)
            
            # render txt
            self.font.render_to(display, text_rect, txt, (255,255,255), size = FONT_SIZE)
            
        #endregion
        
        # check for ball out of map
        if(self.ball.x < 0):
            self.player1_score += 1
            self.__reset_hits()
            self.reset_obj()
        elif(self.ball.x + self.ball.diameter > self.window_width):
            self.player0_score += 1
            self.__reset_hits()
            self.reset_obj()
            
        return GameInfo(self.player0_hits, self.player1_hits,
                        self.player1_hits, self.player1_score)