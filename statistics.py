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