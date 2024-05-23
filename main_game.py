import random, pygame, sys
pygame.init()

<<<<<<< HEAD
# czcionka i prowizoryczna lista wyrazów
font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)

# words = ["a", "abc", "trzy", "radek","michal","dwósłowne chasło","konstantynopol"]

# wybieranie słów z bazy
mode = "hard"
with open("word_base/" + mode + ".txt", "r", encoding="UTF-8") as file:
    words = file.read().split("\n")

# główne parametry ekranu
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
bg_learning = pygame.image.load("graphics/background_learning.png")
=======
>>>>>>> origin/funkcyjnosc_gry
clock = pygame.time.Clock()
size = width, height = 1200, 800
screen = pygame.display.set_mode((1200, 800))

<<<<<<< HEAD
# klasa przechowująca informacje o każdym z dymków
class Falling_object:
    # konstruktor
    def __init__(self):
        self.image = pygame.image.load("graphics/dymek_learning.png")
        self.pos = self.image.get_rect().move(random.randrange(width - 250), 0)
        self.text = words[random.randrange(len(words))]
        self.text_surface = font.render(self.text, False, (0, 0, 0))
        self.text_pos = self.text_surface.get_rect()
        self.text_pos.center = self.pos.center
    # przesuwanie całości w dół
    def fall(self):
        self.pos = self.pos.move(0, 1)
        self.text_pos.center = self.pos.center
=======
background_easy = pygame.image.load('graphics/background_easy.png').convert()
background_medium = pygame.image.load('graphics/background_medium.png').convert()
background_hard = pygame.image.load('graphics/background_hard.png').convert()
background_learning = pygame.image.load('graphics/background_learning.png').convert()
>>>>>>> origin/funkcyjnosc_gry

dymek_easy = pygame.image.load('graphics/dymek_easy.png')
dymek_medium = pygame.image.load('graphics/dymek_medium.png')
dymek_hard = pygame.image.load('graphics/dymek_hard.png')
dymek_learning = pygame.image.load('graphics/dymek_learning.png')

def play_game(mode: str) -> None:

    # słownik grafik do każdego z trybów
    graphics = {"LEARNING": (background_learning, dymek_learning),
                "EASY": (background_easy, dymek_easy),
                "MEDIUM": (background_medium, dymek_medium),
                "HARD": (background_hard, dymek_hard)}

    # czcionka i prowizoryczna lista wyrazów
    text_font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)
    words = ["a", "abc", "trzy", "radek","michal","dwósłowne chasło","konstantynopol"]

    # klasa przechowująca informacje o każdym z dymków
    class Falling_object:
        # konstruktor
        def __init__(self, mode):
            self.image = graphics[mode][1]
            self.pos = self.image.get_rect().move(random.randrange(width - 250), 0)
            self.text = words[random.randrange(len(words))]
            self.text_surface = text_font.render(self.text, False, (0, 0, 0))
            self.text_pos = self.text_surface.get_rect()
            self.text_pos.center = self.pos.center
        # przesuwanie całości w dół
        def fall(self):
            self.pos = self.pos.move(0, 1)
            self.text_pos.center = self.pos.center

    # sprawdzenie czy wpisane słowo znajduje się na ekranie
    def check_if_correct(text: str) -> None:
        for elem in falling_object_list[:]:
            if elem.text == text:
                falling_object_list.remove(elem)
                break

    new_object_timer = 0
    input_box = pygame.Rect(width / 2 - 100, height - 100, 140, 32)
    text = ''
    falling_object_list = []

    while True:
        # sprawdzanie, czy naciśnięto jakiś przycisk i odpowiednie akcje z tym związane
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    check_if_correct(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        # cykliczne tworzenie nowych obiektów
        if new_object_timer == 100:
            falling_object_list.append(Falling_object(mode))
            new_object_timer = 0

        # wypełnienie ekranu
        screen.blit(graphics[mode][0], (0, 0))

        # opadanie elementów wraz z ich wypełnieniem oraz sprawdzenie, czy są na dole ekranu
        for elem in falling_object_list[:]:
            elem.fall()
            screen.blit(elem.image, elem.pos)
            screen.blit(elem.text_surface, elem.text_pos)
            if elem.pos.bottom > height:
                falling_object_list.remove(elem)
        
        # wyrysowanie okna do wpisywania wyrazów
        txt_surface = text_font.render(text, False, 'black')
        text_box_width = max(200, txt_surface.get_width()+10)
        input_box.w = text_box_width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, 'black', input_box, 2)

        pygame.display.flip()
        clock.tick(60)
        new_object_timer += 1
