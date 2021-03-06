from random import *
from time import sleep
import pygame
pygame.init()

class Snakegame:

    def __init__(self, size):
        self.size = size
        self.board = []
        for i in range(self.size):
            self.board.append([0] * self.size)
        self.snake = []
        self.currentDirection = randint(0, 4)
        self.surface = self.initiate_game()
        self.deathevent = pygame.event.Event(pygame.USEREVENT)
        self.multiplier = 0

    def add_snake(self):
        x = randint(5, self.size - 5)
        y = randint(5, self.size - 5)
        self.snake.append([x, y])

    def move_snake(self):

        head = self.snake[0]
        newhead = [0, 0]

        if self.currentDirection == 0:
            newhead[0] = head[0]
            newhead[1] = head[1] + 1
        elif self.currentDirection == 1:
            newhead[0] = head[0] + 1
            newhead[1] = head[1]
        elif self.currentDirection == 2:
            newhead[0] = head[0] - 1
            newhead[1] = head[1]
        else:
            newhead[0] = head[0]
            newhead[1] = head[1] - 1

        if min(newhead) < 0 or max(newhead) > self.size - 1 or self.snake_contains(newhead):
            pygame.event.post(self.deathevent)
            self.snake = []
            return

        self.snake = [newhead] + self.snake
        self.snake.pop()

    def snake_contains(self, coordinate):
        for piece in self.snake:
            if piece == coordinate:
                return True
        return False

    def grow_snake(self):
        tail = self.snake[-1]
        self.snake.append([tail])

    def update_gameboard(self):

        has_apple = False

        # Remove previous snake from the board
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 1:
                    self.board[x][y] = 0
                elif self.board[x][y] == 2:
                    has_apple = True

        if not has_apple:
            self.grow_snake()

        self.move_snake()
        # Add new snake to the board
        for i in range(0, len(self.snake)):
            self.board[self.snake[i][0]][self.snake[i][1]] = 1

        # Add apple to the board
        if not has_apple:
            self.place_apple()

    def place_apple(self):
        available_coords = []
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 0:
                    available_coords.append([x, y])
        rnd_coords = available_coords[randint(0, len(available_coords) - 1)]
        self.board[rnd_coords[0]][rnd_coords[1]] = 2

    def initiate_game(self):

        self.place_apple()

        background_colour = (255, 255, 255)

        screen = pygame.display.set_mode((500, 550))
        pygame.display.set_caption("Snake")
        screen.fill(background_colour)

        # type = Surface
        return screen

    def draw_gameboard(self):
        if len(self.snake) == 0:
            pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0, 0, 500, 500))
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(x * 10, y * 10, 10, 10)
                if self.board[x][y] == 1:
                    pygame.draw.rect(self.surface, (0, 0, 0), rect)
                elif self.board[x][y] == 2:
                    pygame.draw.rect(self.surface, (255, 0, 0), rect)
        # print(self.board)

    def clear_window(self):
        pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(0, 0, 500, 500))
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0, 500, 500, 50))

    def get_score(self):
        return (len(self.snake) - 1) * self.multiplier

    def update_score(self):
        self.display_text("Score: " + str(self.get_score()), (255, 255, 255), (250, 525), font=pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf", 16))

    def run(self):

        start_screen_active = True
        speed = 0.1
        while True:
            pygame.display.flip()

            if start_screen_active:
                self.display_start()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                self.clear_window()
                speed = self.display_difficulty_selection()
                self.currentDirection = randint(0, 4)
                start_screen_active = False

            self.clear_window()
            self.update_gameboard()
            self.draw_gameboard()
            self.update_score()
            sleep(speed)
            self.change_direction()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.USEREVENT:
                    start_screen_active = True
                    self.clear_window()
                    pygame.event.clear()

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.currentDirection != 3:
            self.currentDirection = 0
        elif keys[pygame.K_UP] and self.currentDirection != 0:
            self.currentDirection = 3
        elif keys[pygame.K_LEFT] and self.currentDirection != 1:
            self.currentDirection = 2
        elif keys[pygame.K_RIGHT] and self.currentDirection != 2:
            self.currentDirection = 1

    def display_text(self, text, color, center, font=pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf", 24)):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = center
        self.surface.blit(text_surface, text_rect)

    def display_start(self):

        # Start button
        pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(200, 175, 100, 50))
        self.display_text("START", (0, 0, 0), (250, 200))

        # Quit button
        pygame.draw.rect(self.surface, (255, 0, 0), pygame.Rect(200, 275, 100, 50))
        self.display_text("QUIT", (0, 0, 0), (250, 300))

        pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(0, 500, 500, 50))

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    if 300 >= mouse_x >= 200 and 225 >= mouse_y >= 175:
                        self.add_snake()
                        return
                    elif 300 >= mouse_x >= 200 and 325 >= mouse_y >= 275:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        self.add_snake()
                        return

    def display_difficulty_selection(self):

        font = pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf", 24)

        # Difficulty 1
        pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(150, 100, 200, 50))
        self.display_text("EZ MODE", (0, 0, 0), (250, 125))

        # Difficulty 2
        pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(150, 175, 200, 50))
        self.display_text("NOT BAD", (0, 0, 0), (250, 200))

        # Difficulty 3
        pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(150, 250, 200, 50))
        self.display_text("SPEED DEMON", (0, 0, 0), (250, 275))

        # Difficulty 4
        pygame.draw.rect(self.surface, (0, 255, 0), pygame.Rect(150, 325, 200, 50))
        self.display_text("OVER 9000", (0, 0, 0), (250, 350))

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()
                    if 300 >= mouse_x >= 200 and 150 >= mouse_y >= 1:
                        self.multiplier = 2
                        return 0.1
                    elif 300 >= mouse_x >= 200 and 225 >= mouse_y >= 175:
                        self.multiplier = 5
                        return 0.08
                    elif 300 >= mouse_x >= 200 and 300 >= mouse_y >= 250:
                        self.multiplier = 7
                        return 0.06
                    elif 300 >= mouse_x >= 200 and 375 >= mouse_y >= 325:
                        self.multiplier = 10
                        return 0.043


sg = Snakegame(50)

sg.run()
