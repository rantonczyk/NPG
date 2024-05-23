import pygame
from sys import exit
from enum import Enum

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Keyboard Master')
background_menu = pygame.image.load('graphics/background_menu.png').convert()
background_easy = pygame.image.load('graphics/background_easy.png').convert()
background_medium = pygame.image.load('graphics/background_medium.png').convert()
background_hard = pygame.image.load('graphics/background_hard.png').convert()
background_learning = pygame.image.load('graphics/background_learning.png').convert()
background_hall = pygame.image.load('graphics/background_hall.png').convert()
dumek_easy = pygame.image.load('graphics/dymek_easy.png').convert()
dymek_medium = pygame.image.load('graphics/dymek_medium.png').convert()
dymek_hard = pygame.image.load('graphics/dymek_hard.png').convert()
dymek_learning = pygame.image.load('graphics/dymek_learning.png').convert()
game_font = pygame.font.Font('fonts/Inconsolata-Bold.ttf',60)
play_text = game_font.render('Play', False, 'Black')
play_rect = play_text.get_rect(center = (400,300))
mouse_pos = pygame.mouse.get_pos()


class Current_pos(Enum): #enum pozwala zamiast liczb używać niżej wypisanych nazw w celu poprawienia czytelności kodu
    MENU = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    MODE_CHOICE = 5
    HALL = 6
    ABOUT_US =7
    LEARNING = 8
class Interface():
    def __init__(self):
        self.game_state = Current_pos.MENU  
    def drawing(self):
        if self.game_state == Current_pos.MENU: #na podstawie stanu rozgrywki wyświetlane są odpowiednie elementy interfejsu
            screen.blit(background_menu, (0, 0))
            but_play.draw_button()
            but_hall.draw_button()
            but_about_us.draw_button()
        elif self.game_state == Current_pos.MODE_CHOICE:
            screen.blit(background_easy, (0, 0))
            but_easy.draw_button()
            but_medium.draw_button()
            but_hard.draw_button()
            but_learning.draw_button()
            but_quit.draw_button()
        elif self.game_state == Current_pos.ABOUT_US:
            screen.blit(background_menu, (0, 0))
            but_quit.draw_button()
        elif self.game_state == Current_pos.HALL:
            screen.blit(background_hall, (0, 0))
            but_quit.draw_button()
        elif self.game_state == Current_pos.EASY:
            screen.blit(background_easy, (0, 0))
            but_back.draw_button()
        elif self.game_state == Current_pos.MEDIUM:
            screen.blit(background_medium, (0, 0))
            but_back.draw_button()
        elif self.game_state == Current_pos.HARD:
            screen.blit(background_hard, (0, 0))
            but_back.draw_button()
        elif self.game_state == Current_pos.LEARNING:
            screen.blit(background_learning, (0, 0))
            but_back.draw_button()

interface = Interface()
     
class Button:
    def __init__(self, text: str, position: tuple, graphic, action, font_color ='Black', font=game_font) -> None: 
        self.text = text
        self.font_color = font_color
        self.position = position
        self.font = font
        self.button_text = game_font.render(self.text, False, self.font_color)
        self.button_rect = self.button_text.get_rect(center = (self.position))
        self.graphic = pygame.image.load(graphic).convert_alpha()
        self.graphic_rect = self.graphic.get_rect(center = (self.position))
        self.action = action
        
        
    def draw_button(self):
        # pygame.draw.rect(screen, self.infill_color, self.button_rect,10 )
        # pygame.draw.rect(screen, self.infill_color, self.button_rect)
        # pygame.draw.rect(screen,'Black', self.button_rect,2 )
        screen.blit(self.graphic,self.graphic_rect)
        screen.blit(self.button_text,self.button_rect)
        
    def click_check(self):
        if self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1: 
            interface.game_state = self.action
        
but_play = Button("Graj", (400, 300), 'graphics/dymek_easy.png', Current_pos.MODE_CHOICE, "Black")
but_hall = Button("Wyniki", (400, 430),'graphics/dymek_easy.png', Current_pos.HALL, "Black")
but_about_us = Button("O nas", (400, 560), 'graphics/dymek_easy.png',Current_pos.ABOUT_US, "Black")
but_quit = Button("Wyjdź", (600, 690), 'graphics/dymek_easy.png', Current_pos.MENU, "Black")
but_easy = Button("Łatwy", (600, 240), 'graphics/dymek_easy.png', Current_pos.EASY, "Black")
but_medium = Button("Średni", (600,370), 'graphics/dymek_easy.png',Current_pos.MEDIUM, "Black")
but_hard = Button("Trudny", (600, 500), 'graphics/dymek_easy.png', Current_pos.HARD, "Black")
but_learning = Button("Nauka", (600, 110), 'graphics/dymek_easy.png', Current_pos.LEARNING, "Black")
but_back = Button("Powrót", (150, 700), 'graphics/dymek_hard.png', Current_pos.MODE_CHOICE, "Black")
buttons = [but_play, but_hall, but_about_us, but_quit, but_easy, but_medium, but_hard, but_learning, but_back]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.click_check()
                         
    mouse_pos = pygame.mouse.get_pos()
    
    interface.drawing()
  
    pygame.display.update()
    clock.tick(60)

