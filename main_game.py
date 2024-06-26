import random, pygame, sys
from enum import Enum
import statistics as stats

pygame.init()

# czcionki
font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)
bigger_font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 48)
big_font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 64)

# główne parametry ekranu
clock = pygame.time.Clock()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
game_font = pygame.font.Font('fonts/Inconsolata-Bold.ttf', 60)

# wczytanie potrzebnych grafik

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
dymek_resized = pygame.image.load('graphics/dymek_resized.png')

# klasa dekodująca aktualny stan gry
# enum pozwala zamiast liczb używać niżej wypisanych nazw w celu poprawienia czytelności kodu

class Current_pos(Enum):
    MENU = 1 # menu
    EASY = 2 # tryb łatwy
    MEDIUM = 3 # tryb średni
    HARD = 4 # tryb trudny
    MODE_CHOICE = 5 # wybór trybu gry
    HALL = 6 # statystyki
    ABOUT_US = 7 # strona o nas
    LEARNING = 8 # tryb nauki
    SCORE_RESET = 9 # reset statystyk
    RESET_SCORE_YES = 10 # potwierdzenie resetu
    RETURN = 11 # powrot
    SAVE = 12 # zapis stanu gry
    DELETE_SAVE = 13 # "nadpisanie" stanu gry, efektywnie jest on usuwany
    CONTINUE = 14
    CUSTOM = 15
    CUSTOM_ASK = 16
    LOSE = 17

class Button:
    def __init__(self, text: str, position: tuple, graphic, action, font_color='Black', font=game_font) -> None:
        self.text = text
        self.font_color = font_color
        self.position = position
        self.font = font
        self.button_text = game_font.render(self.text, False, self.font_color)
        self.button_rect = self.button_text.get_rect(center=(self.position))
        self.graphic = pygame.image.load(graphic).convert_alpha()
        self.graphic_rect = self.graphic.get_rect(center=(self.position))
        self.action = action

    # wyrysowanie przycisku
    def draw_button(self):
        screen.blit(self.graphic, self.graphic_rect)
        screen.blit(self.button_text, self.button_rect)

# sprawdzenie, czy dany przycisk został wciśnięty
def click_check(button: Button, mouse_pos) -> None:
    if button.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
        interface.game_state = button.action

# tytaj proszę zamieszczać swoje przyciski

but_play = Button("Graj", (400, 300), 'graphics/dymek_easy.png', Current_pos.MODE_CHOICE, "Black")
but_hall = Button("Wyniki", (400, 430), 'graphics/dymek_easy.png', Current_pos.HALL, "Black")
but_about_us = Button("O nas", (400, 560), 'graphics/dymek_easy.png', Current_pos.ABOUT_US, "Black")
but_quit = Button("Wyjdź", (600, 690), 'graphics/dymek_easy.png', Current_pos.MENU, "Black")
but_easy = Button("Łatwy", (800, 200), 'graphics/dymek_easy.png', Current_pos.EASY, "Black")
but_medium = Button("Średni", (800, 330), 'graphics/dymek_easy.png', Current_pos.MEDIUM, "Black")
but_hard = Button("Trudny", (800, 460), 'graphics/dymek_easy.png', Current_pos.HARD, "Black")
but_learning = Button("Nauka", (400, 265), 'graphics/dymek_easy.png', Current_pos.LEARNING, "Black")
but_quit_score = Button("Wyjdź", (250, 690), 'graphics/dymek_easy.png', Current_pos.MENU, "Black")
but_reset_score = Button("Wyczyść", (950, 690), 'graphics/dymek_easy.png', Current_pos.SCORE_RESET, "Black")
but_reset_score_yes = Button("Tak", (600, 550), 'graphics/dymek_hard.png', Current_pos.RESET_SCORE_YES, "Black")
but_reset_score_no = Button("Nie", (600, 670), 'graphics/dymek_easy.png', Current_pos.HALL, "Black")
but_back = Button("Zakończ", (150, 700), 'graphics/dymek_hard.png', Current_pos.RETURN, "Black") # powrot
but_yes = Button("Tak", (400, 450), 'graphics/dymek_hard.png', Current_pos.SAVE, "Black") #powrot
but_no = Button("Nie", (800, 450), 'graphics/dymek_hard.png', Current_pos.DELETE_SAVE, "Black") #powrot
but_continue = Button("Kontynuuj", (400, 700), 'graphics/dymek_resized.png', Current_pos.CONTINUE, "Black")
but_custom = Button("Własny", (400, 395), 'graphics/dymek_easy.png', Current_pos.CUSTOM_ASK, "Black")
but_play_custom = Button("Graj", (600, 500), 'graphics/dymek_easy.png', Current_pos.CUSTOM, "Black")

# sprawdzenie, czy istnieje zapis gry
def is_save_available():
    try:
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "is_saved=1" in line:
                    return True
        return False
    except FileNotFoundError:
        return False
    
# główna klasa definiująca, co ma się w danym momencie gry wyświetlać i jakie funkcje są wtedy dostępne
class Interface():
    def __init__(self):
        self.game_state = Current_pos.MENU  
        self.buttons = [but_play, but_hall, but_about_us]
        self.last_mode = None
        self.save_info = (None, None)
    
    # na podstawie stanu rozgrywki wyświetlane są odpowiednie elementy interfejsu
    def drawing(self):
        if self.game_state == Current_pos.MENU:
            screen.blit(background_menu, (0, 0))
            if is_save_available():
                self.buttons = [but_play, but_hall, but_about_us, but_continue]
                but_continue.draw_button()
            else:
                self.buttons = [but_play, but_hall, but_about_us]
            but_play.draw_button()
            but_hall.draw_button()
            but_about_us.draw_button()
        elif self.game_state == Current_pos.MODE_CHOICE:
            screen.blit(background_easy, (0, 0))
            self.buttons = [but_easy, but_medium, but_hard, but_learning, but_quit, but_custom]
            but_easy.draw_button()
            but_medium.draw_button()
            but_hard.draw_button()
            but_learning.draw_button()
            but_custom.draw_button()
            but_quit.draw_button()
        elif self.game_state == Current_pos.ABOUT_US:
            screen.blit(background_menu, (0, 0))
            self.buttons = [but_quit]
            but_quit.draw_button()
            about_us_text = [

                "Jesteśmy zespołem pasjonatów programowania.",
                "Naszym celem jest tworzenie gier, które edukują i bawią.",
                "Dziękujemy za grę i mamy nadzieję, że Ci się podoba!",
                "",
                "Radek Antończyk, Michał Barnaś, Julia Brąglewicz,",
                "Kacper Basoń, Mateusz Dańków"
            ]
            for i, line in enumerate(about_us_text):
                text_surface = font.render(line, True, (0, 0, 0))
                screen.blit(text_surface, (190, 395 + i * 40))
        elif self.game_state == Current_pos.HALL:
            screen.blit(background_hall, (0, 0))
            # wypisanie statystyk EASY
            screen.blit(bigger_font.render(f"Łatwy", False, (48, 205, 214)), (550, 280))
            screen.blit(font.render(f"Ilość gier: {easy_stats.games_played}", False, (0, 0, 0)), (480, 330))
            screen.blit(font.render(f"Najlepszy wynik: {easy_stats.best_score}", False, (0, 0, 0)), (480, 360))
            screen.blit(font.render(f"Zniszczone dymki: {easy_stats.bubbles_destroyed}", False, (0, 0, 0)), (480, 390))
            # wypisanie statystyk MEDIUM
            screen.blit(bigger_font.render(f"Średni", False, (48, 73, 171)), (550, 440))
            screen.blit(font.render(f"Ilość gier: {medium_stats.games_played}", False, (0, 0, 0)), (480, 490))
            screen.blit(font.render(f"Najlepszy wynik: {medium_stats.best_score}", False, (0, 0, 0)), (480, 520))
            screen.blit(font.render(f"Zniszczone dymki: {medium_stats.bubbles_destroyed}", False, (0, 0, 0)), (480, 550))
            # wypisanie statystyk HARD
            screen.blit(bigger_font.render(f"Trudny", False, (213, 24, 54)), (550, 600))
            screen.blit(font.render(f"Ilość gier: {hard_stats.games_played}", False, (0, 0, 0)), (480, 650))
            screen.blit(font.render(f"Najlepszy wynik: {hard_stats.best_score}", False, (0, 0, 0)), (480, 680))
            screen.blit(font.render(f"Zniszczone dymki: {hard_stats.bubbles_destroyed}", False, (0, 0, 0)), (480, 710))
            self.buttons = [but_quit_score, but_reset_score]
            but_quit_score.draw_button()
            but_reset_score.draw_button()
        elif self.game_state == Current_pos.LOSE:
            screen.blit(background_easy,(0,0))
            self.buttons = [but_quit]
            but_quit.draw_button()
            screen.blit(big_font.render("Przegrana!!!",False,(100,0,100)),(470,300))
            screen.blit(big_font.render(f"Zniszczone dymki: {self.save_info[1]} ", False, (0, 0, 0)), (390, 390))
            screen.blit(big_font.render(f"punkty: {self.save_info[0]} ", False, (0, 0, 0)), (460, 440))
        elif self.game_state == Current_pos.RETURN: #powrot
            self.buttons = [but_yes, but_no]
            screen.blit(background_easy, (0, 0))
            screen.blit(big_font.render(f"Czy chcesz zapisać stan gry?", False, ((0, 0, 0))), (285, 300))
            but_yes.draw_button()
            but_no.draw_button()
        elif self.game_state == Current_pos.EASY:
            self.last_mode = "EASY"
            self.save_info = play_game("EASY")
        elif self.game_state == Current_pos.MEDIUM:
            self.last_mode = "MEDIUM"
            self.save_info = play_game("MEDIUM")
        elif self.game_state == Current_pos.HARD:
            self.last_mode = "HARD"
            self.save_info = play_game("HARD")
        elif self.game_state == Current_pos.LEARNING:
            self.save_info = play_game("LEARNING")
        elif self.game_state == Current_pos.CUSTOM:
            self.save_info = play_game("CUSTOM")
        elif self.game_state == Current_pos.CUSTOM_ASK:
            self.buttons = [but_play_custom]
            screen.blit(background_easy, (0, 0))
            screen.blit(bigger_font.render(f"Upewnij się, że w folderze", False, ((0, 0, 0))), (400, 200))
            screen.blit(bigger_font.render(f"word_base znajduje się", False, ((0, 0, 0))), (420, 250))
            screen.blit(bigger_font.render(f"plik 'custom.txt' z twoją", False, ((0, 0, 0))), (420, 300))
            screen.blit(bigger_font.render(f"bazą słów.", False, ((0, 0, 0))), (520, 350))
            but_play_custom.draw_button()
        elif self.game_state == Current_pos.SCORE_RESET:
            screen.blit(background_hall, (0, 0))
            self.buttons = [but_reset_score_yes, but_reset_score_no]
            screen.blit(bigger_font.render(f"Czy na pewno", False, (0, 0, 0)), (480, 320))
            screen.blit(bigger_font.render(f"chcesz usunąć", False, (0, 0, 0)), (480, 370))
            screen.blit(bigger_font.render(f"statystyki?", False, (0, 0, 0)), (480, 420))
            but_reset_score_no.draw_button()
            but_reset_score_yes.draw_button()
        elif self.game_state == Current_pos.RESET_SCORE_YES:
            easy_stats.reset_stats('stats/easy_stats.txt')
            medium_stats.reset_stats('stats/medium_stats.txt')
            hard_stats.reset_stats('stats/hard_stats.txt')
            self.game_state = Current_pos.HALL
        elif self.game_state == Current_pos.SAVE:
            # zapis jest z góry zapisany
            self.game_state = Current_pos.MENU
        elif self.game_state == Current_pos.DELETE_SAVE:
            save_game_state(0, 0, 0, 0, [], 0, 0)
            if self.last_mode == "EASY":
                easy_stats.update_stats(self.save_info[0], self.save_info[1], 'stats/easy_stats.txt')
            elif self.last_mode == "MEDIUM":
                medium_stats.update_stats(self.save_info[0], self.save_info[1], 'stats/medium_stats.txt')
            elif self.last_mode == "HARD":
                hard_stats.update_stats(self.save_info[0], self.save_info[1], 'stats/hard_stats.txt')
            self.game_state = Current_pos.MENU
        elif self.game_state == Current_pos.CONTINUE:
            self.save_info = play_game("CONTINUE", True)

# inicjalizacja zmiennych
interface = Interface()

easy_stats = stats.Stats()
medium_stats = stats.Stats()
hard_stats = stats.Stats()

easy_stats.get_stats('stats/easy_stats.txt')
medium_stats.get_stats('stats/medium_stats.txt')
hard_stats.get_stats('stats/hard_stats.txt')

# zapisanie stanu gry do pliku
def save_game_state(mode, new_object_timer, score, lives, falling_object_list, bubbles_destroyed, is_saved=1):
    with open('game_state.txt', 'w') as file:
        file.write(f"is_saved={is_saved}\n")
        file.write(f"mode={mode}\n")
        file.write(f"new_object_timer={new_object_timer}\n")
        file.write(f"score={score}\n")
        file.write(f"bubbles_destroyed={bubbles_destroyed}\n")
        file.write(f"lives={lives}\n")
        for bubble in falling_object_list:
            file.write(f"x_coordinate={bubble.pos.x}\n")
            file.write(f"y_coordinate={bubble.pos.y}\n")
            file.write(f"text={bubble.text}\n")

# wczytanie zapisu z pliku
def load_game_state():
    try:
        with open('game_state.txt', 'r') as file:
            lines = file.readlines()
            state = {}
            bubbles = []
            for line in lines:
                if line.strip():
                    key, value = line.strip().split('=')

                    if key == 'is_saved':
                        state[key] = int(value)
                    elif key == 'mode':
                        state[key] = value
                    elif key == 'new_object_timer' or key == 'lives' or key == 'bubbles_destroyed':
                        state[key] = int(value)
                    elif key == 'score':
                        state[key] = float(value)
                    elif key == 'x_coordinate':
                        x_coord = int(value)
                        y_coord = int(lines[lines.index(line) + 1].strip().split('=')[1])
                        text = lines[lines.index(line) + 2].strip().split('=')[1]
                        bubbles.append(Falling_object(state['mode'], x_coord, y_coord, text))
            state['bubbles'] = bubbles
    except FileNotFoundError:
        print("Plik nie istnieje, gra nie może się rozpocząć.")
    return state

# klasa przechowująca informacje o każdym z dymków
class Falling_object:
    # konstruktor
    def __init__(self, mode, x=None, y=None, text=None):
        self.image = parameters[mode][1]
        if x is None or y is None:
            self.pos = self.image.get_rect().move(random.randrange(width - 250), 0)
        else:
            self.pos = self.image.get_rect().move(x, y)
        self.text = text
        self.text_surface = font.render(self.text, False, (0, 0, 0))
        self.text_pos = self.text_surface.get_rect()
        self.text_pos.center = self.pos.center

    # przesuwanie całości w dół
    def fall(self):
        self.pos = self.pos.move(0, 1)
        self.text_pos.center = self.pos.center

# słownik z parametrami do każdego z trybów
parameters = {"LEARNING": (background_learning, dymek_learning, 0),
                "EASY": (background_easy, dymek_easy, 0.75),
                "MEDIUM": (background_medium, dymek_medium, 1),
                "HARD": (background_hard, dymek_hard, 1.5),
                "CUSTOM": (background_learning, dymek_learning, 1)}

# główna funkcja realizująca działanie gry

def play_game(mode: str, is_continued=False) -> tuple[float, int]:

    # klasa przechowująca informacje o każdym z dymków
    # "nadpisanie" już istniejącej klasy
    class Falling_object:
        def __init__(self, mode, x=None, y=None, text=None):
            self.image = parameters[mode][1]
            if x is None or y is None:
                self.pos = self.image.get_rect().move(random.randrange(width - 250), 0)
            else:
                self.pos = self.image.get_rect().move(x, y)
            if text is None:
                self.text = words[random.randrange(len(words))]
            else:
                self.text = text
            self.text_surface = font.render(self.text, False, (0, 0, 0))
            self.text_pos = self.text_surface.get_rect()
            self.text_pos.center = self.pos.center

        # przesuwanie całości w dół
        def fall(self):
            self.pos = self.pos.move(0, 1)
            self.text_pos.center = self.pos.center

    # sprawdzenie, czy rozpoczynamy nową grę i inicjalizacja parametrów gry
    stan = load_game_state()
    if stan['is_saved'] and is_continued:
        mode = stan['mode']
        new_object_timer = stan['new_object_timer']
        score = stan['score']
        lives = stan['lives']
        bubbles_destroyed = stan['bubbles_destroyed']
        falling_object_list = stan['bubbles']
    else:
        new_object_timer = 0
        score = 0
        lives = 3
        bubbles_destroyed = 0
        falling_object_list = []

    # tworzenie listy słów
    # "LEARNING" otwiera wszystkie trzy
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

    # sprawdzenie czy wpisane słowo znajduje się na ekranie
    def check_if_correct(text: str, score: float, bubbles_destroyed: int) -> tuple:
        for elem in falling_object_list[:]:
            if elem.text == text:
                score += len(elem.text) * parameters[mode][2]
                falling_object_list.remove(elem)
                bubbles_destroyed += 1
                break
        return score, bubbles_destroyed

    # kolejne parametry
    input_box = pygame.Rect(width / 2 - 100, height - 100, 140, 32)
    text = ''
    code = 0
    
    # sprawdzanie, czy naciśnięto jakiś przycisk i odpowiednie akcje z tym związane
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_check(but_back, mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    score, bubbles_destroyed= check_if_correct(text, score, bubbles_destroyed)
                    text = ''
                    if code == 10:
                        lives = 999
                    code = 0
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                    code = 0
                elif event.key == pygame.K_UP and code < 2:
                    code += 1
                elif event.key == pygame.K_DOWN and code >= 2 and code < 4:
                    code += 1
                elif event.key == pygame.K_LEFT and (code == 4 or code == 6):
                    code += 1
                elif event.key == pygame.K_RIGHT and (code == 5 or code == 7):
                    code += 1
                elif event.key == pygame.K_b and code == 8:
                    code += 1
                    text += event.unicode
                elif event.key == pygame.K_a and code == 9:
                    code += 1
                    text += event.unicode
                else:
                    text += event.unicode
                    code = 0

        # koniec gry wywołany naciśnięciem przycisku "Zakończ"
        if interface.game_state == Current_pos.RETURN:
            if mode == "LEARNING":
                interface.game_state = Current_pos.MODE_CHOICE
                return 0, 0
            save_game_state(mode, new_object_timer, score, lives, falling_object_list,bubbles_destroyed)
            return score, bubbles_destroyed

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
                if mode != "LEARNING" or "CUSTOM":
                    falling_object_list.remove(falling_object_list[0])
                    falling_object_list.remove(falling_object_list[0])

        # tylko w trybach wyzwania, koniec żyć - koniec gry
        if mode in ["EASY", "MEDIUM", "HARD", "CUSTOM"]:
            if lives == 0:
                # print game over
                if mode == "EASY":
                    easy_stats.update_stats(score, bubbles_destroyed, 'stats/easy_stats.txt')
                elif mode == "MEDIUM":
                    medium_stats.update_stats(score, bubbles_destroyed, 'stats/medium_stats.txt')
                elif mode == "HARD":
                    hard_stats.update_stats(score, bubbles_destroyed, 'stats/hard_stats.txt')
                interface.game_state = Current_pos.LOSE
                # reset pliku zapisu, ustawienie flagi is_saved = 0
                save_game_state(mode, new_object_timer, score, 3, falling_object_list,bubbles_destroyed ,0)
                return score,bubbles_destroyed

        # wyrysowanie okna do wpisywania wyrazów i przycisku powrotnego
        txt_surface = font.render(text, False, 'black')
        text_box_width = max(200, txt_surface.get_width() + 10)
        input_box.w = text_box_width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, 'black', input_box, 2)
        but_back.draw_button()

        # wypisanie aktualnego wyniku i liczby żyć
        if mode != "LEARNING":
            screen.blit(dymek_hard, (950, 655))
            screen.blit(font.render(f"Życia: {lives}", False, (0, 0, 0)), (980, 675))
            screen.blit(font.render(f"Punkty: {score}", False, (0, 0, 0)), (980, 705))

        pygame.display.flip()
        clock.tick(60)
        new_object_timer += 1
