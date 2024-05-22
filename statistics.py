import json

# Klasa przechowująca statystyki gry
class Stats:
    def __init__(self):
        # Inicjalizacja statystyk poprzez reset
        self.reset_stats()

    def reset_stats(self):
        # Resetowanie statystyk gry
        self.games_played = 0
        self.best_score = 0
        self.current_score = 0

    def get_stats(self):
        # Pobieranie bieżących statystyk
        return {
            "games_played": self.games_played,
            "best_score": self.best_score,
            "current_score": self.current_score
        }

# Klasa gry do wpisywania
class TypingGame:
    def __init__(self):
        # Inicjalizacja statystyk
        self.stats = Stats()

    def play_game(self):
        # Gra odbywa się tutaj, a wynik jest zapisywany w score
        score = self.calculate_score()
        self.stats.update_stats(score)

    def update_stats(self, score):
        # Aktualizacja statystyk po zakończeniu gry
        self.stats.update_stats(score)