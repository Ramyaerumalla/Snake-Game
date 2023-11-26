import pygame
from pygame.locals import *
import time
import random

size = 40
Background_color = 198,3,252

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size*3
        self.y = size*3
        
    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip() 
        
    def move(self):
        self.x = random.randint(0,24)*size
        self.y = random.randint(0,19)*size   

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'
        
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        
    def draw(self):
        #self.parent_screen.fill((Background_color))
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip() 
        
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
        
    def walk(self): 
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        self.draw() 
        
class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,800))
        
        pygame.mixer.init()
        self.play_back_groung_music()
        self.surface.fill((Background_color))
        self.Snake = Snake(self.surface, 1)
        self.Snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False
        
    def play_back_groung_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
        
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))    
        
    def play(self):
        self.render_background()
        self.Snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        # snake colliding with apple
        if self.is_collision(self.Snake.x[0], self.Snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.Snake.increase_length()
            self.apple.move()
            
        # snake colliding with itself
        for i in range(3,self.Snake.length):
            if self.is_collision(self.Snake.x[0],self.Snake.y[0],self.Snake.x[i],self.Snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"
            
        # snake colliding with boundaries of window
        if not (0 <= self.Snake.x[0] <= 1000 and 0 <= self.Snake.y[0] <= 800):
            sound = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(sound)
            raise "Hit the boundry error"  
            
    def show_game_over(self):
        self.render_background()
        self.surface.fill(Background_color)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is Over : Your score is {self.Snake.length}", True, (255, 255, 255))
        self.surface.blit(line1,(200,300))
        line2 = font.render("To play again press enter. to exit press Escape :",True,(255, 255, 255))
        self.surface.blit(line2,(200,350))  
        pygame.display.flip() 
        pygame.mixer.music.pause()
              
            
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.Snake.length}", True, (255, 255, 255)) 
        self.surface.blit(score, (830,10))
        
    def reset(self):
        self.Snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        
    def run(self):
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False   
                    
                    if not pause:    
                        if event.key == K_UP:
                            self.Snake.move_up()
                        if event.key == K_DOWN:
                            self.Snake.move_down()
                        if event.key == K_LEFT:
                            self.Snake.move_left()
                        if event.key == K_RIGHT:
                            self.Snake.move_right()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()    
            time.sleep(0.3)
    
if __name__ ==  "__main__":
    game = Game()
    game.run()
    
    
                
    