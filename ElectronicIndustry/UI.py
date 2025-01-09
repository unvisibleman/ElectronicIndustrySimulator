import os

class UserInterface:
    def __init__(self):
        # Цветовые коды для терминала
        self.COLORS = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
        
        # Создаем атрибуты для удобного доступа к цветам
        self.red = self.COLORS['red']
        self.green = self.COLORS['green']
        self.yellow = self.COLORS['yellow']
        self.blue = self.COLORS['blue']
        self.magenta = self.COLORS['magenta']
        self.cyan = self.COLORS['cyan']
        self.white = self.COLORS['white']
        self.bold = self.COLORS['bold']
        self.end = self.COLORS['end']

    def clear_screen(self):
        """Очищает экран"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print(self, *args):
        """
        Печатает текст с применением цветов и стилей.
        Использование:
        ui.print(ui.red, ui.bold, 'текст')
        ui.print('обычный текст')
        """
        text = ''
        styles = []
        
        for arg in args:
            if arg in self.COLORS.values():
                styles.append(arg)
            else:
                text += str(arg)
        
        # Применяем стили и автоматически добавляем end
        print(''.join(styles) + text + self.end)

    def header(self, text, style='normal'):
        """Выводит заголовок"""
        if style == 'event':
            print(f"\n{self.bold}{self.yellow}{'='*50}{self.end}")
            print(f"{self.bold}{self.yellow}{text.center(50)}{self.end}")
            print(f"{self.bold}{self.yellow}{'='*50}{self.end}")
        else:
            print(f"\n{self.bold}{self.cyan}{text}{self.end}")

    def divider(self, style='normal'):
        """Выводит разделитель"""
        if style == 'simple':
            print(f"{self.white}{'-'*50}{self.end}")
        elif style == 'event':
            print(f"{self.yellow}{'='*50}{self.end}")
        else:
            print(f"{self.cyan}{'-'*50}{self.end}")

    def show_status(self, game):
        """Показывает текущий статус игры"""
        self.header(f"Год: {game.year}")
        print(f"{self.white}Население: {game.population_stats.get_population():.1f} млн")
        print(f"Рубли: {game.rubles:.2f}")
        print(f"Доллары: {game.dollars:.2f}")
        
        if game.production_multiplier > 1:
            print(f"{self.cyan}Множитель производства: x{game.production_multiplier}{self.end}")
        
        self.divider()

        # Показываем текущий план
        if game.five_year_plan.current_plan:
            print(game.five_year_plan.get_status())
            self.divider()

        # Показываем имеющиеся продукты
        if game.products:
            print(f"{self.cyan}Имеющиеся продукты:{self.end}")
            for product, amount in game.products.items():
                if amount >= 1:  # Показываем только если есть хотя бы 1 единица
                    print(f"  • {product}: {amount:.1f}")
            self.divider()