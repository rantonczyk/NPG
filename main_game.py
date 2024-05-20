import sys, pygame, random
pygame.init()
pygame.font.init()

# czcionka i prowizoryczna lista wyrazów
font = pygame.font.SysFont("fonts/Inconsolata-Bold.ttf", 32)
words = ["a", "abc", "trzy", "radek","michal","dwósłowne chasło","konstantynopol"]

# główne parametry ekranu
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
bg_learning = pygame.image.load("graphics/background_learning.png")
clock = pygame.time.Clock()

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

# sprawdzenie czy wpisane słowo znajduje się na ekranie
def check_if_correct(text: str) -> None:
    for elem in falling_object_list[:]:
        if elem.text == text:
            falling_object_list.remove(elem)
            break

# deklaracje potrzebnych zmiennych
input_box = pygame.Rect(width / 2 - 100, height - 100, 140, 32)
text = ''
falling_object_list = []
new_object_timer = 0

# główna pętla
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
        falling_object_list.append(Falling_object())
        new_object_timer = 0

    # wypełnienie ekranu
    screen.blit(bg_learning, (0, 0))

    # opadanie elementów wraz z ich wypełnieniem oraz sprawdzenie, czy są na dole ekranu
    for elem in falling_object_list[:]:
        elem.fall()
        screen.blit(elem.image, elem.pos)
        screen.blit(elem.text_surface, elem.text_pos)
        if elem.pos.bottom > height:
            falling_object_list.remove(elem)
    
    # wyrysowanie okna do wpisywania wyrazów
    txt_surface = font.render(text, False, 'black')
    text_box_width = max(200, txt_surface.get_width()+10)
    input_box.w = text_box_width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, 'black', input_box, 2)

    pygame.display.flip()
    clock.tick(50)
    new_object_timer += 1
