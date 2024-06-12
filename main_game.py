import random, pygame, sys
from enum import Enum
import statistics as stats
pygame.init()

# czcionka
font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)

# główne parametry ekranu
clock = pygame.time.Clock()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
game_font = pygame.font.Font('fonts/Inconsolata-Bold.ttf',60)

background_easy = pygame.image.load('graphics/background_easy.png').convert()
background_medium = pygame.image.load('graphics/background_medium.png').convert()
background_hard = pygame.image.load('graphics/background_hard.png').convert()
background_learning = pygame.image.load('graphics/background_learning.png').convert()
background_hall = pygame.image.load('graphics/background_hall.png').convert()
background_menu = pygame.image.load('graphics/background_menu.png').convert()

dymek_easy = pygame.image.load('graphics/dymek_easy.png')
dymek_medium = pygame.image.load('graphics/dymek_medium.png')
dymek_hard = pygame.image.load('graphics/dymek_hard.png')
dymek_learning = pygame.image.load('graphics/dymek_learning.png')

class Current_pos(Enum): #enum pozwala zamiast liczb używać niżej wypisanych nazw w celu poprawienia czytelności kodu
    MENU = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    MODE_CHOICE = 5
    HALL = 6
    ABOUT_US =7
    LEARNING = 8

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
        
    # def click_check(self, mouse_pos):
    #     if self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1: 
    #         interface.game_state = self.action

def click_check(button: Button, mouse_pos) -> None:
    if button.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1: 
        interface.game_state = button.action

but_play = Button("Graj", (400, 300), 'graphics/dymek_easy.png', Current_pos.MODE_CHOICE, "Black")
but_hall = Button("Wyniki", (400, 430),'graphics/dymek_easy.png', Current_pos.HALL, "Black")
but_about_us = Button("O nas", (400, 560), 'graphics/dymek_easy.png',Current_pos.ABOUT_US, "Black")
but_quit = Button("Wyjdź", (600, 690), 'graphics/dymek_easy.png', Current_pos.MENU, "Black")
but_easy = Button("Łatwy", (600, 240), 'graphics/dymek_easy.png', Current_pos.EASY, "Black")
but_medium = Button("Średni", (600,370), 'graphics/dymek_easy.png',Current_pos.MEDIUM, "Black")
but_hard = Button("Trudny", (600, 500), 'graphics/dymek_easy.png', Current_pos.HARD, "Black")
but_learning = Button("Nauka", (600, 110), 'graphics/dymek_easy.png', Current_pos.LEARNING, "Black")
but_back = Button("Powrót", (150, 700), 'graphics/dymek_hard.png', Current_pos.MODE_CHOICE, "Black")

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
            play_game("EASY")
        elif self.game_state == Current_pos.MEDIUM:
            play_game("MEDIUM")
        elif self.game_state == Current_pos.HARD:
            play_game("HARD")
        elif self.game_state == Current_pos.LEARNING:
            play_game("LEARNING")

interface = Interface()

easy_stats = stats.Stats()
medium_stats = stats.Stats()
hard_stats = stats.Stats()

easy_stats.get_stats('easy_stats.txt')
medium_stats.get_stats('medium_stats.txt')
hard_stats.get_stats('hard_stats.txt')

def play_game(mode: str) -> None:

    # słownik z parametrami do każdego z trybów
    parameters = {"LEARNING": (background_learning, dymek_learning, 0),
                "EASY": (background_easy, dymek_easy, 0.75),
                "MEDIUM": (background_medium, dymek_medium, 1),
                "HARD": (background_hard, dymek_hard, 1.5)}

    # czcionka i prowizoryczna lista wyrazów
    text_font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)
    
    # wybieranie słów z bazy("LEARNING" otwiera wszystkie trzy)
    if mode != "LEARNING":
        with open("word_base/" + mode + ".txt", "r", encoding="UTF-8") as file:
            words = file.read().split("\n")
    else:
        with open("word_base/easy.txt", "r", encoding="UTF-8") as file:
            words = file.read().split("\n")
        with open("word_base/medium.txt", "r", encoding="UTF-8") as file:
            words += file.read().split("\n")
        with open("word_base/hard.txt", "r", encoding="UTF-8") as file:
            words += file.read().split("\n")

    # klasa przechowująca informacje o każdym z dymków
    class Falling_object:
        # konstruktor
        def __init__(self, mode):
            self.image = parameters[mode][1]
            self.pos = self.image.get_rect().move(random.randrange(width - 250), 0)
            self.text = words[random.randrange(len(words))]
            self.text_surface = text_font.render(self.text, False, (0, 0, 0))
            self.text_pos = self.text_surface.get_rect()
            self.text_pos.center = self.pos.center
        # przesuwanie całości w dół
        def fall(self):
            self.pos = self.pos.move(0, 1)
            self.text_pos.center = self.pos.center

    # sprawdzenie, czy jest rozpoczęta nowa gra, czy kontynuowana
    # if(is_continued):
    #     get_info_from_save_file
    # else:
    new_object_timer = 0
    falling_object_list = []
    score = 0
    lives = 3
    bubbles_destroyed = 0


    # sprawdzenie czy wpisane słowo znajduje się na ekranie
    def check_if_correct(text: str, score: float, bubbles_destroyed: int) -> tuple:
        for elem in falling_object_list[:]:
            if elem.text == text:
                score += len(elem.text) * parameters[mode][2]
                bubbles_destroyed += 1
                falling_object_list.remove(elem)
                break
        return score, bubbles_destroyed

    input_box = pygame.Rect(width / 2 - 100, height - 100, 140, 32)
    text = ''

    while True:
        # sprawdzanie, czy naciśnięto jakiś przycisk i odpowiednie akcje z tym związane
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_check(but_back, mouse_pos)
                if interface.game_state == Current_pos.MODE_CHOICE:
                    if mode == "EASY":
                        easy_stats.update_stats(score, bubbles_destroyed, 'easy_stats.txt')
                    elif mode == "MEDIUM":
                        medium_stats.update_stats(score, bubbles_destroyed, 'medium_stats.txt')
                    elif mode == "HARD":
                        hard_stats.update_stats(score, bubbles_destroyed, 'hard_stats.txt')
                    # gracz wyszedł z gry -> zapisanie STANU GRY
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score, bubbles_destroyed = check_if_correct(text, score, bubbles_destroyed)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        
        mouse_pos = pygame.mouse.get_pos()

        # cykliczne tworzenie nowych obiektów
        if new_object_timer == 100:
            falling_object_list.append(Falling_object(mode))
            new_object_timer = 0

        # wypełnienie ekranu
        screen.blit(parameters[mode][0], (0, 0))

        # opadanie elementów wraz z ich wypełnieniem oraz sprawdzenie, czy są na dole ekranu
        for elem in falling_object_list[:]:
            elem.fall()
            screen.blit(elem.image, elem.pos)
            screen.blit(elem.text_surface, elem.text_pos)
            if elem.pos.bottom > height:
                lives -= 1
                falling_object_list.remove(elem)
                if mode != "LEARNING":
                    falling_object_list.remove(falling_object_list[0])
                    falling_object_list.remove(falling_object_list[0])
        
        # tylko w trybach wyzwania
            if mode != "LEARNING":
                if lives == 0:
                    # print game over
                    # save statistics
                    # exit to main menu
                    interface.game_state = Current_pos.MENU
                    return

        # wyrysowanie okna do wpisywania wyrazów i przycisku powrotnego
        txt_surface = text_font.render(text, False, 'black')
        text_box_width = max(200, txt_surface.get_width()+10)
        input_box.w = text_box_width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, 'black', input_box, 2)
        but_back.draw_button()

        # wypisanie aktualnego wyniku i liczby żyć
        if mode != "LEARNING":
            screen.blit(dymek_hard, (950, 655))
            screen.blit(text_font.render(f"Życia: {lives}", False, (0, 0, 0)), (980, 675))
            screen.blit(text_font.render(f"Punkty: {score}", False, (0, 0, 0)), (980, 705))

        pygame.display.flip()
        clock.tick(60)
        new_object_timer += 1