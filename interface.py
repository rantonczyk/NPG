import pygame
from sys import exit
from enum import Enum
import main_game as main

# podstawowe parametry gry

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('Keyboard Master')
play_text = main.game_font.render('Play', False, 'Black')
play_rect = play_text.get_rect(center = (400,300))
mouse_pos = pygame.mouse.get_pos()

# tworzenie 3 obiektów klasy Stats

easyStats = main.stats.Stats()
mediumStats = main.stats.Stats()
hardStats = main.stats.Stats()

# główna pętla obsługująca interfejs gry

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in main.interface.buttons:
                main.click_check(button, mouse_pos)
                         
    mouse_pos = pygame.mouse.get_pos()
    
    main.interface.drawing()
  
    pygame.display.update()
    clock.tick(60)
