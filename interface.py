import pygame
from sys import exit
from enum import Enum

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption('Keyboard Master')
background = pygame.image.load('graphics/background_menu_2.png').convert()
game_font = pygame.font.Font('fonts/Inconsolata-Bold.ttf',100)
play_text = game_font.render('Play', False, 'Black')
play_rect = play_text.get_rect(center = (400,300))

class Button:
    def __init__(self, text: str, position: tuple, infill_color, font_color, font=game_font) -> None:
        self.text = text
        self.position = position
        self.font = font
        self.font_color = font_color
        self.infill_color = infill_color
        self.button_rect = None
        self.button_text = None
        self.make_button()
        
    def make_button(self):
        self.button_text = game_font.render(self.text, False, self.font_color)
        self.button_rect = self.button_text.get_rect(center = (self.position))
    
    def draw_button(self):
        pygame.draw.rect(screen, self.infill_color, self.button_rect,10 )
        pygame.draw.rect(screen, self.infill_color, self.button_rect)
        pygame.draw.rect(screen,'Black', self.button_rect,1 )
        screen.blit(self.button_text,self.button_rect)
        
    
# def displayer(position):
#     if position == 1:
        
class Current_pos(Enum):
    MENU = 1
    PLAYGROUND = 2
    TRAINING = 3
    EASY = 4
    MEDIUM = 5
    HARD = 6
    HALL = 7
    INFO = 8
    PAUSED = 9


print('smuteczek')

but1 = Button("tekst", (100, 100), "Red", "Black")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, 'Red', play_rect,10)
    pygame.draw.rect(screen, 'Red', play_rect)
    pygame.draw.rect(screen, 'Black', play_rect,1)
    but1.draw_button()
    
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(play_text,play_rect)
    # print(pygame.mouse.get_pressed())
    if play_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
        current_pos = Current_pos.PLAYGROUND
        print('hell yeag!')
    pygame.display.update()
    clock.tick(60)

