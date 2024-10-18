import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (324, 235, 195)

class Boundary:
    def __init__(self, parent_screen):
        self.boundary_block = pygame.image.load("resources/block.jpg").convert()
        self.parent_screen = parent_screen
        self.x1 = 0
        self.x2 = 960
        self.y1 = 0
        self.y2 = 760

    def draw(self):
        for i in range(0, 1000, 40):
            self.parent_screen.blit(self.boundary_block, (i,self.y1))
            self.parent_screen.blit(self.boundary_block, (i,self.y2))
        for i in range(0, 800, 40):
            self.parent_screen.blit(self.boundary_block, (self.x1,i))
            self.parent_screen.blit(self.boundary_block, (self.x2,i))
        pygame.display.flip()


class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,23)*SIZE
        self.y = random.randint(0,18)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def draw(self):
        # self.parent_screen.fill((52, 235, 195))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()
    
    def increase_length(self):
        self.length += 1;
        self.x.append(-1)
        self.y.append(-1)
        

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000,800))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.boundary = Boundary(self.surface)
        # self.boundary.draw()
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg").convert()
        self.surface.blit(bg, (0,0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def wall_collision(self, x1, x2, y1, y2):
        if x1< 0 or x1>=x2 or y1 < 0 or y1>=y2:
            return True
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.boundary.draw()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()

        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Game Over"

        #snake colliding will boundary
        if self.wall_collision(self.snake.x[0],self.boundary.x2,self.snake.y[0],self.boundary.y2):
            self.play_sound('crash')
            raise "Game Over"
            # if self.snake.x[0] < 0 or self.snake.x[0]>=self.boundary.x2 or self.snake.y[0] < 0 or self.snake.y[0]>=self.boundary.y2:
    
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255,255,255))
        self.surface.blit(score, (800,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game Over! Score: {self.snake.length - 1}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("Hit 'Enter' to play again OR 'ESC' to exit",True, (255,255,255))
        self.surface.blit(line2, (200,350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.play(-1)
                        pause = False

                    if not pause:   
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True 
                self.reset()

            time.sleep(.3)

if __name__ == "__main__":
    game = Game()
    game.run()
    
    