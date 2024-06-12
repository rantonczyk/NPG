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

    def update_stats(self, score, filename):
        # Aktualizacja statystyk po zakończeniu gry
        self.games_played += 1
        self.current_score = score
        if score > self.best_score:
            self.best_score = score

        try:
            with open(filename, 'w') as file:
                file.write(f"games_played={self.games_played}\n")
                file.write(f"best_score={self.best_score}\n")
                file.write(f"current_score={self.current_score}\n")
        except Exception as e:
            print(f"An unexpected error occurred while writing to the file: {e}")


    def get_stats(self, filename):
        # Pobranie statystyk przy uruchomieniu trybu
        try:
            with open(filename, 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    if key == 'games_played':
                        self.games_played = int(value)
                    elif key == 'best_score':
                        self.best_score = int(value)
                    elif key == 'current_score':
                        self.current_score = int(value)
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except ValueError:
            print("Error in file format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
