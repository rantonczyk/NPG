class Stats:
    def __init__(self):
        # Inicjalizacja zmiennych przechowujących statystyki
        self.games_played = 0
        self.best_score = 0
        self.current_score = 0

    def reset_stats(self):
        # Zresetowanie statystyk
        self.games_played = 0
        self.best_score = 0
        self.current_score = 0

    def update_stats(self, score):
        # Aktualizacja statystyk po zakończeniu gry
        self.games_played += 1
        self.current_score = score
        if score > self.best_score:
            self.best_score = score

    def get_stats(self):
        # Pobranie bieżących statystyk
        return {
            "games_played": self.games_played,
            "best_score": self.best_score,
            "current_score": self.current_score
        }
