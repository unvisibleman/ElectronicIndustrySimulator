import numpy as np

class PopulationStats:
    def __init__(self):
        self.initial_population = 150  # Начальное население в млн (1926 год)
        self.growth_rate = 0.01  # Базовый темп роста
        self.base_year = 1926  # Базовый год для расчета
        self.population = self.initial_population

    def update_population(self, current_year):
        """Обновляет численность населения"""
        years_passed = current_year - self.base_year
        self.population = self.initial_population * np.exp(self.growth_rate * years_passed)
        return self.population

    def get_population(self):
        """Возвращает текущую численность населения"""
        return round(self.population, 2)