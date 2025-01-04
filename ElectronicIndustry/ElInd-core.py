import numpy as np
import os

class UI:
    def __init__(self):
        self.COLORS = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'end': '\033[0m'
        }
        
        # Создаем атрибуты для каждого цвета/стиля
        for name, code in self.COLORS.items():
            setattr(self, name, code)
    
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
    
    def header(self, text, style='event'):
        """
        Печатает заголовок определенного типа.
        Стили: event, war, achievement, bankruptcy
        """
        headers = {
            'event': f"\n{self.bold}!!! ВАЖНОЕ СОБЫТИЕ !!!{self.end}",
            'war': f"\n{self.bold}{self.red}!!! ВОЕННОЕ ПОЛОЖЕНИЕ !!!{self.end}",
            'achievement': f"\n{self.bold}{self.green}!!! ДОСТИЖЕНИЕ !!!{self.end}",
            'bankruptcy': f"\n{self.bold}{self.red}!!! БАНКРОТСТВО !!!{self.end}"
        }
        print(headers.get(style, headers['event']))
        self.print(text)
    
    def divider(self, style='simple'):
        """
        Печатает разделитель определенного типа.
        Стили: simple, double, status
        """
        dividers = {
            'simple': f"{self.white}------------------------{self.end}",
            'double': f"{self.white}========================{self.end}",
            'status': f"{self.white}-----------------------{self.end}"
        }
        print(dividers.get(style, dividers['simple']))

# Создаем глобальный экземпляр UI
ui = UI()

class Game:
    def __init__(self):
        self.ui = ui
        
        self.year = 1918
        self.current_plan = None
        self.tecnologies = TechnologyTree()
        self.rubles = 1000  # Начальное количество рублей
        self.dollars = 500   # Начальное количество долларов
        self.population_stats = PopulationStats()
        self.products = {}  # Хранит информацию о произведенных товарах
        self.DEPRECIATION_RATE = 0.1  # 10% обесценивание в год
        self.last_command = None  # Добавляем сохранение последней команды
        self.research_in_progress = {}  # Добавляем словарь для отслеживания процесса исследования {tech_name: years_spent}
        self.BASE_POPULATION = 150  # Базовое население в млн (1926 год)
        self.POPULATION_PRICE_FACTOR = 1.5  # Коэффициент влияния населения на цену
        self.command_capacity = 1 # Количество команд в год
        self.production_multiplier = 1  # Базовый множитель производства
        self.PRODUCTION_UPGRADE_COST_RUBLES = 5000  # Стоимость улучшения в рублях
        self.PRODUCTION_UPGRADE_COST_DOLLARS = 1000  # Стоимость улучшения в долларах
        self.PRODUCTION_UPGRADE_FACTOR = 2  # Во сколько раз увеличивается производство
        
        # Добавляем описания технологий
        self.TECH_DESCRIPTIONS = {
            "пассивка": {
                "описание": "Пассивные электронные компоненты - резисторы, конденсаторы, катушки индуктивности",
                "уровни": {
                    "начальная": "Производство простейших компонентов низкой точности",
                    "средняя": "Улучшенная точность и стабильность характеристик",
                    "продвинутая": "Прецизионные компоненты с высокой надежностью"
                }
            },
            "радиолампы": {
                "описание": "Электровакуумные приборы для усиления и генерации электрических сигналов",
                "уровни": {
                    "начальная": "Простые триоды и диоды",
                    "средняя": "Многосеточные лампы, тетроды и пентоды",
                    "продвинутая": "Специальные типы ламп, высокочастотные и мощные приборы"
                }
            },
            "полупроводники": {
                "описание": "Полупроводниковые приборы - диоды, транзисторы",
                "уровни": {
                    "начальная": "Простые германиевые диоды и транзисторы",
                    "средняя": "Кремниевые транзисторы, стабилитроны",
                    "продвинутая": "Мощные транзисторы, тиристоры, специальные приборы"
                }
            },
            "чбэлт": {
                "описание": "Черно-белые электронно-лучевые трубки для телевизоров и мониторов",
                "уровни": {
                    "начальная": "Простые ЭЛТ с низким разрешением",
                    "средняя": "ЭЛТ с улучшенной фокусировкой и яркостью",
                    "продвинутая": "Высококачественные ЭЛТ с высоким разрешением"
                }
            },
            "нмл": {
                "описание": "Накопители на магнитной ленте - устройства хранения данных",
                "уровни": {
                    "начальная": "Простые устройства с низкой плотностью записи",
                    "средняя": "Улучшенные механизмы и повышенная надежность",
                    "продвинутая": "Высокоскоростные НМЛ с высокой плотностью записи"
                }
            },
            "ис": {
                "описание": "Интегральные схемы малой степени интеграции",
                "уровни": {
                    "начальная": "Простые логические элементы",
                    "средняя": "Операционные усилители, счетчики",
                    "продвинутая": "Сложные функциональные блоки"
                }
            },
            "цветнойэлт": {
                "описание": "Цветные электронно-лучевые трубки для телевизоров",
                "уровни": {
                    "начальная": "Базовые цветные ЭЛТ",
                    "средняя": "Улучшенная цветопередача и яркость",
                    "продвинутая": "Высококачественные ЭЛТ с точной цветопередачей"
                }
            },
            "мис": {
                "описание": "Микросхемы средней степени интеграции - до 100 элементов на кристалле",
                "уровни": {
                    "начальная": "Простые функциональные узлы",
                    "средняя": "Сложные логические блоки",
                    "продвинутая": "Процессорные элементы и память"
                }
            },
            "нгмд": {
                "описание": "Накопители на гибких магнитных дисках",
                "уровни": {
                    "начальная": "8-дюймовые дискеты",
                    "средняя": "5.25-дюймовые дискеты",
                    "продвинутая": "3.5-дюймовые дискеты высокой плотности"
                }
            },
            "сис": {
                "описание": "Схемы с высокой степенью интеграции - до 1 000 элементов на кристалле",
                "уровни": {
                    "начальная": "Простые микропроцессоры",
                    "средняя": "Микроконтроллеры",
                    "продвинутая": "Специализированные процессоры"
                }
            },
            "бис": {
                "описание": "Большие интегральные схемы - до 10 000 элементов на кристалле",
                "уровни": {
                    "начальная": "Простые микропроцессоры",
                    "средняя": "Сопроцессоры и контроллеры",
                    "продвинутая": "Мощные процессоры и память"
                }
            },
            "нжмд": {
                "описание": "Накопители на жестких магнитных дисках",
                "уровни": {
                    "начальная": "Диски малой емкости",
                    "средняя": "Улучшенные механизмы и контроллеры",
                    "продвинутая": "Высокоскоростные диски большой емкости"
                }
            },
            "сбис": {
                "описание": "Сверхбольшие интегральные схемы - более 10 000 элементов на кристалле",
                "уровни": {
                    "начальная": "Базовые СБИС",
                    "средняя": "Сложные процессоры",
                    "продвинутая": "Многоядерные процессоры и видеочипы"
                }
            }
        }

        # Добавляем информацию о денежных реформах
        self.MONETARY_REFORMS = {
            1924: {
                "name": "Денежная реформа 1922—1924 годов",
                "ratio": 10,
                "description": "Введение твёрдой валюты - червонца"
            },
            1947: {
                "name": "Денежная реформа 1947 года",
                "ratio": 10,
                "description": "Послевоенная конверсия рублей"
            },
            1961: {
                "name": "Денежная реформа 1961 года",
                "ratio": 10,
                "description": "Изменение масштаба цен"
            }
        }

        # Рецепты производства товаров народного потребления и военной техники
        self.CONSUMER_PRODUCTS = {
            "радиоприемник_ламповый": {
                "components": {
                    "пассивка": 5,
                    "радиолампы": 5
                },
                "price": 1000,  # базовая цена в рублях
                "description": "Ламповый радиоприемник"
            },
            "телевизор_чб_ламповый": {
                "components": {
                    "пассивка": 20,
                    "радиолампы": 10,
                    "чбэлт": 1
                },
                "price": 2500,
                "description": "Черно-белый ламповый телевизор"
            },
            "военная_радиостанция": {
                "components": {
                    "пассивка": 6,
                    "радиолампы": 6,
                },
                "price": 5000,
                "description": "Военная радиостанция"
            },
            "рлс_пво": {
                "components": {
                    "пассивка": 10,
                    "радиолампы": 15,
                },
                "price": 15000,
                "description": "РЛС ПВО"
            },
            "эвм_1": {
                "components": {
                    "пассивка": 100,
                    "радиолампы": 100,
                    "чбэлт": 1
                },
                "price": 50000,
                "description": "ЭВМ первого поколения (ламповая)"
            },
            "радиоприемник_транзисторный": {
                "components": {
                    "пассивка": 8,
                    "полупроводники": 6
                },
                "price": 800,
                "description": "Транзисторный радиоприемник"
            },
            "телевизор_чб_транзисторный": {
                "components": {
                    "пассивка": 15,
                    "полупроводники": 12,
                    "чбэлт": 1
                },
                "price": 2000,
                "description": "Черно-белый транзисторный телевизор"
            },
            "телевизор_цветной": {
                "components": {
                    "пассивка": 30,
                    "полупроводники": 20,
                    "цветнойэлт": 1,
                    "ис": 5
                },
                "price": 5000,
                "description": "Цветной телевизор"
            },
            "радиоприемник_гибридный": {
                "components": {
                    "пассивка": 6,
                    "полупроводники": 4,
                    "ис": 2
                },
                "price": 600,
                "description": "Радиоприемник на микросхемах"
            },
            "эвм_2": {
                "components": {
                    "пассивка": 200,
                    "полупроводники": 500,
                    "чбэлт": 1,
                    "нмл": 1
                },
                "price": 40000,
                "description": "ЭВМ второго поколения (транзисторная)"
            },
            "эвм_3": {
                "components": {
                    "пассивка": 300,
                    "ис": 200,
                    "чбэлт": 1,
                    "нмл": 2
                },
                "price": 35000,
                "description": "ЭВМ третьего поколения (на микросхемах)"
            },
            "инженерный_калькулятор": {
                "components": {
                    "пассивка": 5,
                    "ис": 3,
                    "мис": 1,
                },
                "price": 2500,
                "description": "Инженерный калькулятор"
            },
            "программируемый_калькулятор": {
                "components": {
                    "пассивка": 8,
                    "ис": 5,
                    "мис": 2,
                    "сис": 1,
                },
                "price": 4000,
                "description": "Программируемый калькулятор"
            },
            "эвм_4": {
                "components": {
                    "пассивка": 200,
                    "бис": 50,
                    "чбэлт": 1,
                    "нгмд": 1
                },
                "price": 30000,
                "description": "ЭВМ четвертого поколения (на БИС)"
            },
            "бытовой_компьютер": {
                "components": {
                    "пассивка": 30,
                    "бис": 15,
                    "чбэлт": 1,
                    "нмл": 1
                },
                "price": 3000,
                "description": "Бытовой компьютер с магнитофоном"
            },
            "персональный_компьютер": {
                "components": {
                    "пассивка": 30,
                    "сис": 8,
                    "нгмд": 2,
                    "цветнойэлт": 1
                },
                "price": 8000,
                "description": "Базовый персональный компьютер с дисководом"
            },
            "профессиональный_компьютер": {
                "components": {
                    "пассивка": 40,
                    "сис": 12,
                    "нгмд": 2,
                    "нжмд": 1,
                    "цветнойэлт": 1
                },
                "price": 12000,
                "description": "Профессиональный компьютер с жестким диском"
            },
            "современный_компьютер": {
                "components": {
                    "пассивка": 50,
                    "сис": 5,
                    "бис": 10,
                    "сбис": 15,
                    "нгмд": 1,
                    "нжмд": 1,
                    "цветнойэлт": 1
                },
                "price": 15000,
                "description": "Мощный компьютер на СБИС"
            }
        }
        
        # Статистика произведенных товаров
        self.consumer_products_made = {}

        self.five_year_plan = FiveYearPlan()

    def start(self):
        print("Добрый день! Вы - глава электронной промышленности СССР. Ваша задача - построить электронную промышленность СССР!")
        self.help_command();
        self.main_loop()

    def apply_monetary_reform(self, reform):
        """Применяет денежную реформу ко всем ценам и балансам"""
        ratio = reform["ratio"]
        old_rubles = self.rubles
        
        # Обновляем баланс игрока
        self.rubles = self.rubles / ratio
        
        # Обновляем базовые цены продуктов
        for product in self.tecnologies.PRODUCT_PRICES:
            self.tecnologies.PRODUCT_PRICES[product] /= ratio
            
        # Обновляем стоимость исследований
        for tech in self.tecnologies.resources_required:
            self.tecnologies.resources_required[tech] /= ratio
            
        # Обновляем цены технологий (для продажи)
        for tech in self.tecnologies.TECH_PRICES:
            self.tecnologies.TECH_PRICES[tech] /= ratio
            
        # Обновляем стоимость расширения производства
        self.PRODUCTION_UPGRADE_COST_RUBLES /= 10

        # Выводим информацию об изменениях
        self.ui.header(f"Денежная реформа {self.year} года!", 'event')
        self.ui.print(self.ui.yellow, reform["description"])
        
        self.ui.print(
            self.ui.white, "Ваши средства: ",
            self.ui.yellow, f"{old_rubles:.2f} руб. ",
            self.ui.white, "→ ",
            self.ui.green, f"{self.rubles:.2f} руб."
        )
        
        # Показываем изменения стоимости исследований
        example_research = list(self.tecnologies.resources_required.keys())[0]  # Берем первую технологию
        self.ui.print(
            self.ui.white, f"Исследование {example_research}: ",
            self.ui.yellow, f"{self.tecnologies.resources_required[example_research]:.2f} руб."
        )
        
        self.ui.divider('double')

    def main_loop(self):
        while True:
            c = self.ui.COLORS
            # Проверка денежных реформ
            if self.year in self.MONETARY_REFORMS:
                self.apply_monetary_reform(self.MONETARY_REFORMS[self.year])

            # Проверка исторических событий
            if self.year == 1924:
                self.ui.header('Начало выпуска журнала Радио!', 'event')
                self.ui.divider('simple')
            elif self.year == 1932:
                self.ui.header('Получены первые сведения о возможной угрозе войны с Германией!', 'event')
                self.ui.divider('simple')
            elif self.year == 1941:
                self.ui.header('Началась Великая Отечественная война!', 'war')
                print(f"{c['red']}На эвакуацию заводов требуется 1000 рублей{c['end']}")
                self.rubles -= 1000
                if self.check_bankruptcy():
                    return
                self.ui.divider('simple')
            elif self.year > 1941 and self.year < 1945:
                self.ui.header('Великая Отечественная война продолжается!', 'war')  
                print(f"{c['red']}Фронту требуется 200 рублей{c['end']}")
                self.rubles -= 200
                if self.check_bankruptcy():
                    return
                self.ui.divider('simple')
            elif self.year == 1945:
                self.ui.header('Великая Отечественная война закончилась!', 'achievement')
                self.ui.divider('simple')
            elif self.year == 1952:
                self.ui.header('Наши ученые построили первую в стране ЭВМ! Теперь вы можете использовать 2 команды в год!', 'achievement')
                self.command_capacity = 2
                self.ui.divider('simple')
            elif self.year == 1956:
                self.ui.header('Начато проектирование первого искусственного спутника Земли!', 'event')
                print(f"{c['red']}На это потребуется 200 рублей{c['end']}")
                self.rubles -= 200
                if self.check_bankruptcy():
                    return
                self.ui.divider('simple')
            elif self.year == 1957:
                self.ui.header('Успешный запуск первого искусственного спутника Земли!', 'achievement')
                self.ui.divider('simple')
            elif self.year == 1958:
                self.ui.header('Начато проектирование пилотируемого космического корабля!', 'event')
                print(f"{c['red']}На это потребуется 300 рублей{c['end']}")
                self.rubles -= 300
                if self.check_bankruptcy():
                    return
                self.ui.divider('simple')
            elif self.year == 1961:
                self.ui.header('Юрий Гагарин стал первым человеком в космосе!', 'achievement')
                self.ui.divider('simple')
            elif self.year == 1984:
                self.ui.header('Начало выпуска журнала Микропроцессорные средства и системы!', 'event')
                self.ui.divider('simple')
            elif self.year == 1991:
                self.ui.header('В этот год могла произойти контрреволюция!', 'achievement')
                self.ui.divider('simple')

            # Проверка пятилетнего плана
            if self.five_year_plan.check_plan_end(self.year):
                completion = self.five_year_plan.check_completion(self.population_stats)
                if completion is False:
                    self.ui.header("ПРОВАЛ ПЯТИЛЕТКИ", style='bankruptcy')
                    self.ui.print(self.ui.red, "\nПлан не выполнен! Игра окончена.")
                    self.ui.print(self.ui.white, f"Итоговый статус: {self.five_year_plan.get_status()}")
                    return
                elif completion is True:
                    self.ui.header("ПЯТИЛЕТКА ВЫПОЛНЕНА!", style='achievement')
                    self.ui.print(self.ui.white, f"Итоговый статус: {self.five_year_plan.get_status()}")
            
            # Проверяем начало нового плана
            if self.five_year_plan.start_plan(self.year):
                self.ui.header(f"Начало нового плана: {self.five_year_plan.get_status()}", style='event')
            
            commands = 0
            while commands < self.command_capacity:
                self.population_stats.update_population(self.year)
                self.show_status()
                
                # Проверка банкротства после каждого хода
                if self.check_bankruptcy():
                    return
                    
                command = input(f"{c['cyan']}Введите команду: {c['end']}")
                result = self.process_command(command)
                if result == "valid":
                    commands += 1
                elif result == "exit":
                    print(f"{c['green']}Спасибо за игру!{c['end']}")
                    return
            self.year += 1

    def show_status(self):
        c = self.ui.COLORS
        print(f"{c['bold']}{c['blue']}Год: {self.year}{c['end']}")
        print(f"Деньги: {c['green']}{self.rubles:.2f} руб{c['end']}, {c['yellow']}${self.dollars:.2f}{c['end']}")
        print(f"{c['cyan']}Текущая пятилетка: {self.five_year_plan.get_status()}{c['end']}")
        
        # Доступные технологии
        print(f"\n{c['magenta']}Доступные технологии:{c['end']}")
        available_techs = self.tecnologies.get_available_technologies(self.year)
        tech_status = self.tecnologies.get_status()
        
        # Фильтруем доступные технологии, исключая освоенные
        new_techs = [tech for tech in available_techs if tech not in tech_status]
        
        if new_techs:
            for tech in new_techs:
                print(f"  • {tech}")
        else:
            print("  Нет доступных технологий")
        
        # Освоенные технологии
        print(f"\n{c['cyan']}Освоенные технологии:{c['end']}")
        if tech_status:
            for tech, details in tech_status.items():
                if "уровень" in details and details["уровень"] != "исследуется":
                    level_color = {
                        "начальная": c['white'],
                        "средняя": c['yellow'],
                        "продвинутая": c['green']
                    }.get(details["уровень"], c['white'])
                    
                    print(f"  • {c['bold']}{tech}{c['end']} {level_color}{details['уровень']}{c['end']} Освоено в: {details['год освоения']}")
                elif "уровень" in details and details["уровень"] == "исследуется":
                    print(f"  • {c['bold']}{tech}{c['end']} - {c['yellow']}{details['прогресс']}{c['end']}")
        else:
            print("  Нет освоенных технологий")
        
        print(f"\n{c['green']}Население: {self.population_stats.get_population():.2f} млн. человек{c['end']}")
        self.ui.divider('status')

    def process_command(self, command):
        self.clear_screen()
        try:
            if command.strip().lower() in ["выход", "exit", "quit"]:
                return "exit"

            if command.strip().lower() == "повтор":
                if self.last_command is None:
                    print("Нет предыдущей команды для повтора")
                    return "invalid"
                command = self.last_command
                print(f"Повтор команды: {command}")
            else:
                self.last_command = command  # Сохраняем текущую команду

            parts = command.strip().split()
            if not parts:
                print("Пустая команда. Введите 'помощь' для списка команд.")
                return "invalid"

            cmd = parts[0].lower()

            # Информационные команды
            if cmd == "помощь":
                self.help_command()
                return "help"  # Специальное возвращаемое значение для команды помощи
            elif cmd == "что_такое":
                if len(parts) != 2:
                    print("Использование: что_такое ТЕХНОЛОГИЯ")
                    return "invalid"
                self.show_tech_info(parts[1].lower())
                return "help"
            elif cmd == "каталог":
                self.show_consumer_products_status()
                return "help"

            # Команды действий
            elif cmd == "собрать":
                if len(parts) != 2:
                    print("Использование: собрать ТОВАР")
                    return "invalid"
                # Проверяем существование товара перед сборкой
                if parts[1].lower() not in self.CONSUMER_PRODUCTS:
                    print(f"Неизвестный товар: {parts[1]}")
                    return "invalid"
                self.assemble_consumer_product(parts[1].lower())
                return "valid"

            elif cmd == "исследовать":
                if len(parts) < 2:
                    print("Использование: исследовать ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]")
                    return "invalid"
                self.tecnologies.update_current_year(self.year)
                total_cost = 0
                for tech in parts[1:]:
                    print(f"\nИсследование {tech}:")
                    cost = self.tecnologies.research(tech.lower(), self.rubles - total_cost)
                    total_cost += cost
                self.rubles -= total_cost  # Вычитаем общую стоимость исследований
                return "valid"
            elif cmd == "произвести":
                if len(parts) < 2:
                    print("Использование: произвести ТЕХНОЛОГИЯ или произвести все")
                    return "invalid"
                
                if parts[1].lower() == "все":
                    self.produce_all_available()
                else:
                    for tech in parts[1:]:
                        print(f"\nПроизводство {tech}:")
                        self.produce_product(tech.lower())
                return "valid"
            elif cmd == "продажа_технологий":
                if len(parts) < 2:
                    print("Использование: продажа_технологий ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]")
                    return "invalid"
                for tech in parts[1:]:
                    self.sell_technology(tech.lower())
                return "valid"
            elif cmd == "купить_технологию":
                if len(parts) != 2:
                    print("Использование: купить_технологию ТЕХНОЛОГИЯ")
                    return "invalid"
                self.buy_technology(parts[1].lower())
                return "valid"
            elif cmd == "пропуск":
                if len(parts) > 1:
                    print("Команда 'пропуск' не требует дополнительных аргументов")
                    return "invalid"
                print("Ход пропущен")
                return "valid"
            elif cmd == "расширить_производство":
                if len(parts) == 2 and parts[1].lower() in ["рубли", "доллары"]:
                    currency = "rubles" if parts[1].lower() == "рубли" else "dollars"
                    if self.expand_production(currency):
                        return "valid"
                    return "invalid"
                else:
                    self.ui.print(self.ui.yellow, 
                        "Использование: расширить_производство [рубли|доллары]")
                    return "invalid"
            else:
                print("Неизвестная команда. Введите 'помощь' для списка команд.")
                return "invalid"
        except Exception as e:
            print(f"Произошла ошибка при выполнении команды: {str(e)}")
            return "invalid"

    def help_command(self):
        c = self.ui.COLORS
        print(f"\n{c['bold']}{c['cyan']}Доступные команды:{c['end']}")
        print(f"{c['yellow']}помощь{c['end']} - вывести справку по командам")
        print(f"{c['yellow']}что_такое ТЕХНОЛОГИЯ{c['end']} - получить описание технологии")
        print(f"{c['yellow']}план ГОД{c['end']} - начать пятилетний план")
        print(f"{c['yellow']}отчет{c['end']} - вывести отчет о пятилетнем плане")
        print(f"{c['yellow']}исследовать ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]{c['end']} - исследовать одну или несколько технологий")
        print(f"{c['yellow']}купить_технологию ТЕХНОЛОГИЯ{c['end']} - купить технологию за доллары")
        print(f"{c['yellow']}произвести ТЕХНОЛОГИЯ{c['end']} - произвести продукт")
        print(f"{c['yellow']}произвести все{c['end']} - произвести все освоенные технологии")
        print(f"{c['yellow']}собрать ТОВАР{c['end']} - собрать товар народного потребления")
        print(f"{c['yellow']}каталог{c['end']} - показать доступные товары")
        print(f"{c['yellow']}продажа_технологий ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]{c['end']} - продажа одной или нескольких технологий за рубеж")
        print(f"{c['yellow']}расширить_производство [рубли|доллары]{c['end']} - увеличить объемы производства")
        print(f"{c['yellow']}пропуск{c['end']} - пропустить текущий ход")
        print(f"{c['yellow']}повтор{c['end']} - повторить предыдущую команду")
        print(f"{c['red']}выход (или exit, quit){c['end']} - завершить игру")
    
    def calculate_depreciation(self, base_price, year_learned, tech_name=None):
        """Расчет цены с учетом устаревания, численности населения и количества продаж"""
        # Рассчитываем базовое устаревание
        years_passed = self.year - year_learned
        
        # Если это расчет для продажи технологии, учитываем количество предыдущих продаж
        if tech_name:
            sales_count = self.tecnologies.technology_sales.get(tech_name, 0)
            # Увеличиваем скорость устаревания на 20% за каждую предыдущую продажу
            depreciation_multiplier = 1 + (sales_count * self.tecnologies.SALES_DEPRECIATION_MULTIPLIER)
            years_passed *= depreciation_multiplier
        
        depreciation = base_price * (1 - self.DEPRECIATION_RATE * years_passed)
        base_deprecated_price = max(depreciation, base_price * 0.1)  # Минимальная цена 10% от базовой

        # Корректируем цену с учетом роста населения
        population_ratio = self.population_stats.get_population() / self.BASE_POPULATION
        population_multiplier = pow(population_ratio, self.POPULATION_PRICE_FACTOR)
        
        final_price = base_deprecated_price * population_multiplier
        return final_price

    def produce_product(self, product_name):
        tech_status = self.tecnologies.get_status()
        if product_name not in tech_status:
            print("Технология для производства не освоена.")
            return
            
        tech_details = tech_status[product_name]
        if tech_details.get("уровень") == "исследуется":
            print(f"Технология {product_name} еще исследуется. Текущий прогресс: {tech_details['прогресс']}")
            return
            
        year_learned = tech_details["год освоения"]
        current_level = tech_details["уровень"]
        
        # Используем индивидуальную базовую цену
        base_price = self.tecnologies.PRODUCT_PRICES[product_name]
        
        # Модификаторы в зависимости от уровня технологии
        if current_level == "средняя":
            base_price *= 1.5
        elif current_level == "продвинутая":
            base_price *= 2.0
        
        # Рассчитываем итоговую цену с учетом устаревания и населения
        price = self.calculate_depreciation(base_price, year_learned)
        
        for _ in range(self.production_multiplier):
            self.products[product_name] = self.products.get(product_name, 0) + 1
        self.rubles += price
        print(f"Произведен {product_name}. Доход от продажи: {price:.2f} рублей")

    # Продажа технологий за рубеж
    def sell_technology(self, tech_name):
        if tech_name in self.tecnologies.get_status():
            tech_status = self.tecnologies.get_status()[tech_name]
            year_learned = tech_status["год освоения"]
            
            # Используем индивидуальную базовую цену
            base_price = self.tecnologies.TECH_PRICES[tech_name]
            
            if tech_status["уровень"] == "средняя":
                base_price *= 2.0
            elif tech_status["уровень"] == "продвинутая":
                base_price *= 3.0
            
            # Получаем текущее количество продаж
            sales_count = self.tecnologies.technology_sales.get(tech_name, 0)
            
            # Рассчитываем цену с учетом всех факторов
            price = self.calculate_depreciation(base_price, year_learned, tech_name)
            
            self.dollars += price
            
            # Увеличиваем счетчик продаж
            self.tecnologies.technology_sales[tech_name] = sales_count + 1
            
            # Выводим информацию о продаже
            self.ui.print(f"Продажа технологии {tech_name} (продана {sales_count + 1} раз). Получено: ${price:.2f}")
            
            # Если продаж больше 3, выводим предупреждение
            if sales_count + 1 >= 3:
                self.ui.print(self.ui.yellow, "Внимание! Технология значительно устарела из-за множественных продаж.")
        else:
            self.ui.print(self.ui.red, "Технология не освоена.")

    def check_bankruptcy(self):
        c = self.ui.COLORS
        if self.rubles < 0:
            self.ui.header('Казна пуста! Промышленность в упадке!', 'bankruptcy')
            print(f"{c['yellow']}Итоговая статистика:{c['end']}")
            print(f"{c['white']}Год: {self.year}{c['end']}")
            
            # Форматированный вывод технологий в итоговой статистике
            print(f"\n{c['white']}Освоенные технологии:{c['end']}")
            tech_status = self.tecnologies.get_status()
            if tech_status:
                for tech, details in tech_status.items():
                    if "уровень" in details and details["уровень"] != "исследуется":
                        level_color = {
                            "начальная": c['white'],
                            "средняя": c['yellow'],
                            "продвинутая": c['green']
                        }.get(details["уровень"], c['white'])
                        print(f"  • {tech} - {level_color}{details['уровень']}{c['end']} ({details['год освоения']})")
            else:
                print("  Нет освоенных технологий")
            
            print(f"{c['white']}Население: {self.population_stats.get_population():.2f} млн. человек{c['end']}")
            self.ui.divider('double')
            print(f"{c['red']}Игра окончена!{c['end']}")
            return True
        return False

    def buy_technology(self, tech_name):
        c = self.ui.COLORS
        if tech_name not in self.tecnologies.get_available_technologies(self.year):
            print(f"{c['red']}Эта технология пока недоступна для покупки!{c['end']}")
            return

        if tech_name in self.tecnologies.get_status():
            print(f"{c['yellow']}Эта технология уже освоена!{c['end']}")
            return

        # Определяем стоимость технологии
        base_price = self.tecnologies.TECH_PRICES[tech_name] * 2  # Покупка дороже чем продажа
        tech_level = self.tecnologies.technologies[tech_name][0]
        
        if tech_level == "средняя":
            base_price *= 2.0
        elif tech_level == "продвинутая":
            base_price *= 3.0

        # Корректируем цену с учетом года
        year_available = self.tecnologies.technologies[tech_name][1]
        years_since_available = self.year - year_available
        if years_since_available > 0:
            price_reduction = min(0.5, years_since_available * 0.1)  # Максимальная скидка 50%
            final_price = base_price * (1 - price_reduction)
        else:
            final_price = base_price

        print(f"{c['cyan']}Стоимость покупки технологии {tech_name}: {final_price:.2f} долларов{c['end']}")
        
        if self.dollars < final_price:
            print(f"{c['red']}Недостаточно долларов для покупки технологии!{c['end']}")
            return

        confirm = input(f"{c['yellow']}Подтвердите покупку (да/нет): {c['end']}")
        if confirm.lower() != "да":
            print(f"{c['yellow']}Покупка отменена{c['end']}")
            return

        self.dollars -= final_price
        # Устанавливаем технологию как освоенную
        level, year_available, _ = self.tecnologies.technologies[tech_name]
        self.tecnologies.technologies[tech_name] = (level, year_available, self.year)
        print(f"{c['green']}Технология {tech_name} успешно куплена!{c['end']}")

    def show_tech_info(self, tech_name):
        c = self.ui.COLORS
        if tech_name not in self.TECH_DESCRIPTIONS:
            print(f"{c['red']}Информация о технологии '{tech_name}' не найдена.{c['end']}")
            return

        tech_info = self.TECH_DESCRIPTIONS[tech_name]
        print(f"\n{c['bold']}{c['cyan']}Технология: {tech_name}{c['end']}")
        print(f"{c['white']}{tech_info['описание']}{c['end']}")
        
        # Добавляем информацию о стоимости исследования
        if tech_name in self.tecnologies.resources_required:
            cost = self.tecnologies.resources_required[tech_name]
            print(f"\n{c['yellow']}Стоимость исследования: {cost} руб.{c['end']}")
        
        print(f"\n{c['yellow']}Уровни развития:{c['end']}")
        for level, desc in tech_info['уровни'].items():
            level_color = {
                "начальная": c['white'],
                "средняя": c['yellow'],
                "продвинутая": c['green']
            }.get(level, c['white'])
            print(f"  • {level_color}{level}{c['end']}: {desc}")
        
        # Если технология уже освоена, показываем текущий уровень
        tech_status = self.tecnologies.get_status()
        if tech_name in tech_status and "уровень" in tech_status[tech_name]:
            current_level = tech_status[tech_name]["уровень"]
            if current_level != "исследуется":
                print(f"\n{c['green']}Текущий уровень: {current_level}{c['end']}")
            else:
                print(f"\n{c['yellow']}Статус: {tech_status[tech_name]['прогресс']}{c['end']}")
        
        self.ui.divider('simple')

    def can_produce_consumer_product(self, product_name):
        """Проверка возможности производства товара"""
        if product_name not in self.CONSUMER_PRODUCTS:
            return False, "Неизвестный товар"
            
        product = self.CONSUMER_PRODUCTS[product_name]
        tech_status = self.tecnologies.get_status()
        
        # Проверяем, освоены ли все необходимые технологии
        missing_tech = []
        for component in product["components"].keys():
            if component not in tech_status:
                missing_tech.append(component)
            elif tech_status[component].get("уровень") == "исследуется":
                missing_tech.append(f"{component} (исследуется)")
                
        if missing_tech:
            return False, f"Не освоены технологии: {', '.join(missing_tech)}"
            
        return True, None

    def assemble_consumer_product(self, product_name):
        """Попытка собрать товар народного потребления"""
        if product_name not in self.CONSUMER_PRODUCTS:
            self.ui.print(self.ui.red, f"Неизвестный товар: {product_name}")
            return False
            
        product = self.CONSUMER_PRODUCTS[product_name]
        
        # Проверка возможности производства
        can_produce, reason = self.can_produce_consumer_product(product_name)
        if not can_produce:
            self.ui.print(self.ui.yellow, reason)
            return False
            
        # Проверка наличия компонентов
        missing_components = []
        for component, amount in product["components"].items():
            if self.products.get(component, 0) < amount:
                missing_components.append(
                    f"{component} (нужно {amount}, есть {self.products.get(component, 0)})"
                )
        
        if missing_components:
            self.ui.print(self.ui.yellow, f"Для производства {product['description']} не хватает компонентов:")
            for comp in missing_components:
                self.ui.print(self.ui.white, f"  • {comp}")
            return False
            
        # Списание компонентов
        for component, amount in product["components"].items():
            self.products[component] -= amount
            
        # Начисление прибыли
        price = self.calculate_consumer_product_price(product)
        self.rubles += price
        
        # Учет в статистике
        self.consumer_products_made[product_name] = self.consumer_products_made.get(product_name, 0) + 1
        
        self.ui.print(self.ui.green, 
            f"Произведен {product['description']}! Получено {price:.2f} руб.")
        
        # Добавляем учет производства в план
        self.five_year_plan.add_production(product_name)
        
        return True

    def calculate_consumer_product_price(self, product):
        """Расчет итоговой цены товара с учетом спроса и времени"""
        base_price = product["price"]
        
        # Модификатор в зависимости от новизны технологий
        tech_status = self.tecnologies.get_status()
        newest_tech_year = max(tech_status[comp]["год освоения"] 
                             for comp in product["components"].keys())
        
        years_since_newest = self.year - newest_tech_year
        if years_since_newest <= 5:
            base_price *= 1.5  # Повышенный спрос на новые технологии
        elif years_since_newest >= 15:
            base_price *= 0.7  # Сниженный спрос на устаревшие технологии
            
        # Учет численности населения
        population_ratio = self.population_stats.get_population() / self.BASE_POPULATION
        price = base_price * pow(population_ratio, self.POPULATION_PRICE_FACTOR)
        
        return price

    def show_consumer_products_status(self):
        """Вывод информации о доступных товарах народного потребления"""
        self.ui.print(self.ui.cyan, "\nДоступные товары:")
        
        available_products = False
        tech_status = self.tecnologies.get_status()
        
        for name, product in self.CONSUMER_PRODUCTS.items():
            # Проверяем, освоены ли все необходимые технологии
            all_tech_available = True
            unavailable_tech = []
            
            for component in product["components"].keys():
                if component not in tech_status:
                    all_tech_available = False
                    unavailable_tech.append(component)
                elif tech_status[component].get("уровень") == "исследуется":
                    all_tech_available = False
                    unavailable_tech.append(f"{component} (исследуется)")
            
            # Показываем только товары с освоенными технологиями
            if all_tech_available:
                available_products = True
                self.ui.print(self.ui.bold, 
                    f"\n{product['description']} (команда: собрать {name}):")
                self.ui.print(self.ui.white, "Требуемые компоненты:")
                
                for component, amount in product["components"].items():
                    have_amount = self.products.get(component, 0)
                    color = self.ui.green if have_amount >= amount else self.ui.red
                    self.ui.print(f"  • {component}: {color}{have_amount}/{amount}{self.ui.end}")
                
                # Показываем статистику производства
                if name in self.consumer_products_made:
                    self.ui.print(self.ui.yellow, 
                        f"Всего произведено: {self.consumer_products_made[name]}")
                
                # Показываем примерную стоимость
                estimated_price = self.calculate_consumer_product_price(product)
                self.ui.print(self.ui.cyan, f"Примерная стоимость: {estimated_price:.2f} руб.")
        
        if not available_products:
            self.ui.print(self.ui.yellow, "  Нет доступных товаров - необходимо освоить новые технологии")

    def produce_all_available(self):
        """Производит все доступные технологии"""
        tech_status = self.tecnologies.get_status()
        produced_anything = False
        
        self.ui.print(self.ui.cyan, "\nМассовое производство:")
        
        # Производим все освоенные технологии
        for tech_name in tech_status:
            if tech_status[tech_name].get("уровень") != "исследуется":
                self.ui.print(self.ui.white, f"\nПроизводство {tech_name}:")
                self.produce_product(tech_name)
                produced_anything = True
        
        if not produced_anything:
            self.ui.print(self.ui.yellow, "Нет освоенных технологий для производства")
            return False
        return True

    def clear_screen(self):
        """Очищает экран"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def expand_production(self, currency="rubles"):
        """Расширяет производство за рубли или доллары"""
        if currency == "rubles":
            cost = self.PRODUCTION_UPGRADE_COST_RUBLES
            if self.rubles < cost:
                self.ui.print(self.ui.red, 
                    f"Недостаточно рублей! Требуется: {cost:.2f} руб.")
                return False
            self.rubles -= cost
        else:  # dollars
            cost = self.PRODUCTION_UPGRADE_COST_DOLLARS
            if self.dollars < cost:
                self.ui.print(self.ui.red, 
                    f"Недостаточно долларов! Требуется: ${cost:.2f}")
                return False
            self.dollars -= cost

        self.production_multiplier *= self.PRODUCTION_UPGRADE_FACTOR
        self.ui.print(self.ui.green, 
            f"Производство расширено! Новый множитель: x{self.production_multiplier}")
        return True


class TechnologyTree:
    def __init__(self):
        # Add this line at the beginning of __init__
        self.research_in_progress = {}
        
        # Дерево технологий: {название технологии: (уровень, доступный с года, год освоения)}
        self.technologies = {
            "пассивка": ("начальная", 1918, None),
            "радиолампы": ("начальная", 1918, None),
            "полупроводники": ("начальная", 1947, None),
            "чбэлт": ("начальная", 1949, None),
            "нмл": ("начальная", 1949, None),
            "ис": ("начальная", 1961, None),
            "цветнойэлт": ("начальная", 1967, None),
            "мис": ("начальная", 1970, None),
            "нгмд": ("начальная", 1971, None),
            "сис": ("начальная", 1975, None),
            "бис": ("начальная", 1980, None),
            "нжмд": ("начальная", 1986, None),
            "сбис": ("начальная", 1990, None),
        }
        
        # Время исследования технологий
        self.research_time = {
            "пассивка": 0,
            "радиолампы": 0,
            "полупроводники": 1,
            "чбэлт": 1,
            "нмл": 1,
            "ис": 1,
            "цветнойэлт": 1,
            "мис": 1,
            "нгмд": 1,
            "сис": 1,
            "бис": 1,
            "нжмд": 1,
            "сбис": 1,
        }

        # Уровни технологии, связанные с каждой технологией
        self.levels = {
            "начальная": {
                "upgrade": "средняя",
                "description": "Базовый уровень технологии."
            },
            "средняя": {
                "upgrade": "продвинутая",
                "description": "Технология, которую освоили, с большими показателями производительности."
            },
            "продвинутая": {
                "upgrade": None,
                "description": "Максимальный уровень технологии."
            }
        }

        # Ресурсы, необходимые для исследований
        self.resources_required = {
            "пассивка": 50,
            "радиолампы": 150,
            "полупроводники": 200,
            "чбэлт": 250,
            "нмл": 300,
            "ис": 400,
            "цветнойэлт": 500,
            "мис": 350,
            "нгмд": 300,
            "сис": 450,
            "бис": 600,
            "нжмд": 700,
            "сбис": 800,
        }

        # Добавляем словарь для отслеживания количества продаж каждой технологии
        self.technology_sales = {}
        
        # Коэффициент ускорения устаревания за каждую продажу
        self.SALES_DEPRECIATION_MULTIPLIER = 0.2  # 20% ускорение устаревания за каждую продажу

        # Базовые цены для каждой технологии
        self.TECH_PRICES = {
            "пассивка": 500,        # Базовые компоненты
            "радиолампы": 1000,     # Сложное производство
            "полупроводники": 2000,  # Высокотехнологичное производство
            "чбэлт": 1500,          # Сложная технология
            "нмл": 1200,            # Механика + электроника
            "ис": 2500,             # Высокая сложность
            "цветнойэлт": 2000,     # Развитие ЧБ ЭЛТ
            "мис": 3000,            # Развитие ИС
            "нгмд": 1800,           # Развитие НМЛ
            "сис": 3500,            # Развитие МИС
            "бис": 4000,            # Развитие СИС
            "нжмд": 2500,           # Развитие НГМД
            "сбис": 5000            # Высшая сложность
        }
        
        # Базовые цены производимых товаров
        self.PRODUCT_PRICES = {
            "пассивка": 800,        # Массовое производство
            "радиолампы": 1500,     # Сложное производство
            "полупроводники": 2500, # Высокотехнологичное производство
            "чбэлт": 2000,         # Телевизоры и мониторы
            "нмл": 1800,           # Накопители данных
            "ис": 3000,            # Интегральные схемы
            "цветнойэлт": 3500,    # Цветные телевизоры
            "мис": 4000,           # Микросхемы
            "нгмд": 2500,          # Дискеты
            "сис": 5000,           # Сложные схемы
            "бис": 6000,           # Большие схемы
            "нжмд": 4000,          # Жесткие диски
            "сбис": 8000           # Сверхбольшие схемы
        }

    def get_available_technologies(self, current_year):
        """Возвращает список технологий, которые можно освоить в текущем году."""
        available_technologies = []
        for tech, (level, year_available, _) in self.technologies.items():
            if current_year >= year_available:
                status = ""
                if tech in self.research_in_progress:
                    years_spent = self.research_in_progress[tech]
                    years_total = self.research_time[tech]
                    status = f" (исследуется: {years_spent}/{years_total} лет)"
                available_technologies.append(tech + status)
        return available_technologies

    def get_status(self):
        """Возвращает статус освоенных технологий."""
        status = {}
        for tech, (level, year_available, year_learned) in self.technologies.items():
            if year_learned is not None:  # Показать только освоенные технологии
                status[tech] = {
                    "уровень": level,
                    "доступен с": year_available,
                    "год освоения": year_learned,
                    "описание": self.levels[level]["description"]
                }
            elif tech in self.research_in_progress:  # Добавляем информацию о текущих исследованиях
                years_spent = self.research_in_progress[tech]
                years_total = self.research_time[tech]
                status[tech] = {
                    "уровень": "исследуется",
                    "прогресс": f"{years_spent}/{years_total} лет"
                }
        return status

    def research(self, tech_name, available_rubles):
        tech_name = tech_name.lower()
        if tech_name in self.technologies:
            current_level, year_available, year_learned = self.technologies[tech_name]
            
            # Проверяем, можно ли улучшить технологию
            if current_level not in self.levels or self.levels[current_level]["upgrade"] is None:
                print(f"{tech_name} уже достигла максимального уровня развития.")
                return 0  # Возвращаем 0, так как деньги не потрачены
                
            if year_available > self.current_year:
                print(f"{tech_name} еще недоступна. Можно освоить позже.")
                return 0
            
            required_cost = self.resources_required[tech_name]
            print(f"Стоимость исследования: {required_cost} руб.")
                
            if required_cost > available_rubles:
                print(f"Недостаточно рублей для исследования. Доступно: {available_rubles} руб.")
                return 0

            # Проверяем, исследуется ли уже эта технология
            if tech_name not in self.research_in_progress:
                self.research_in_progress[tech_name] = 0
                print(f"Начато исследование {tech_name}. Требуется лет: {self.research_time[tech_name]}")
                return required_cost # Возвращаем стоимость исследования
            
            # Увеличиваем счетчик лет исследования
            self.research_in_progress[tech_name] += 1
            years_left = self.research_time[tech_name] - self.research_in_progress[tech_name]

            if years_left > 0:
                print(f"Исследование {tech_name} продолжается. Осталось лет: {years_left}")
                return required_cost # Возвращаем стоимость исследования

            # Исследование завершено
            next_level = self.levels[current_level]["upgrade"]
            self.technologies[tech_name] = (next_level, year_available, self.current_year)
            del self.research_in_progress[tech_name] # Удаляем из списка исследуемых
            print(f"{tech_name} улучшена до уровня {next_level}.")
            return required_cost # Возвращаем 0, так как деньги не потрачены
        else:
            print("Технология не найдена.")
            return 0 # Возвращаем 0, так как деньги не потрачены

    def update_current_year(self, year):
        self.current_year = year

class FiveYearPlan:
    def __init__(self):
        self.plans = {
            (1928, 1932): {
                "name": "Первая пятилетка",
                "goals": {"радиоприемник_ламповый": 1},
                "completed": {}
            },
            (1933, 1937): {
                "name": "Вторая пятилетка",
                "goals": {"радиоприемник_ламповый": 1},
                "completed": {}
            },
            (1938, 1942): {
                "name": "Третья пятилетка",
                "goals": {"военная_радиостанция": 1},
                "completed": {}
            },
            (1942, 1945): {
                "name": "Военное время",
                "goals": {"рлс_пво": 1},
                "completed": {}
            },
            (1946, 1950): {
                "name": "Четвертая пятилетка",
                "goals": {"радиоприемник_ламповый": 1},
                "completed": {}
            },
            (1951, 1955): {
                "name": "Пятая пятилетка",
                "goals": {"телевизор_чб_ламповый": 1},
                "completed": {}
            },
            (1956, 1960): {
                "name": "Шестая пятилетка",
                "goals": {"эвм_1": 1},
                "completed": {}
            },
            (1961, 1965): {
                "name": "Седьмая пятилетка",
                "goals": {"эвм_3": 1},
                "completed": {}
            },
            (1966, 1970): {
                "name": "Восьмая пятилетка",
                "goals": {"телевизор_цветной": 1},
                "completed": {}
            },
            (1971, 1975): {
                "name": "Девятая пятилетка",
                "goals": {"инженерный_калькулятор": 1},
                "completed": {}
            },
            (1976, 1980): {
                "name": "Десятая пятилетка",
                "goals": {"бытовой_компьютер": 1},
                "completed": {}
            },
            (1981, 1985): {
                "name": "Десятая пятилетка",
                "goals": {"персональный_компьютер": 1},
                "completed": {}
            },
            (1986, 1990): {
                "name": "Одинадцатая пятилетка",
                "goals": {"профессиональный_компьютер": 1},
                "completed": {}
            }

        }
        self.current_plan = None
        self.OVERACHIEVEMENT_BONUS = 0.002  # Увеличение темпа роста при перевыполнении

    def check_plan_end(self, year):
        """Проверяет, закончился ли текущий план"""
        if not self.current_plan:
            return False
        _, end_year = self.current_plan
        return year > end_year

    def start_plan(self, year):
        """Начинает новый план, если для года существует пятилетка"""
        for period, plan in self.plans.items():
            start_year, end_year = period
            if start_year <= year <= end_year:
                self.current_plan = period
                if not plan["completed"]:
                    plan["completed"] = {product: 0 for product in plan["goals"]}
                return True
        return False

    def add_production(self, product_name, amount=1):
        """Учитывает произведенную продукцию в текущем плане"""
        if not self.current_plan or product_name not in self.plans[self.current_plan]["goals"]:
            return False
        
        self.plans[self.current_plan]["completed"][product_name] += amount
        return True

    def check_completion(self, population_stats):
        """Проверяет выполнение текущего плана"""
        if not self.current_plan:
            return None
        
        plan = self.plans[self.current_plan]
        all_completed = True
        overachieved = True
        
        for product, required in plan["goals"].items():
            completed = plan["completed"].get(product, 0)
            if completed < required:
                all_completed = False
                overachieved = False
                break
            elif completed == required:
                overachieved = False
        
        if overachieved:
            # Увеличиваем темп роста населения при перевыполнении
            population_stats.growth_rate += self.OVERACHIEVEMENT_BONUS
        
        return all_completed

    def get_status(self):
        """Возвращает статус текущего плана"""
        if not self.current_plan:
            return "Нет текущего плана"
        
        plan = self.plans[self.current_plan]
        start_year, end_year = self.current_plan
        status = [f"\n{plan['name']} ({start_year}-{end_year}):"]
        
        for product, required in plan["goals"].items():
            completed = plan["completed"].get(product, 0)
            status.append(f"  • {product}: {completed}/{required}")
        
        return "\n".join(status)

class PopulationStats:
    def __init__(self):
        self.initial_population = 150  # Начальное население в млн (1926 год)
        self.growth_rate = 0.01  # Темп роста
        self.base_year = 1926  # Базовый год для расчета
        self.population = self.initial_population  # Текущее население

    def update_population(self, current_year):
        years_passed = current_year - self.base_year
        self.population = self.initial_population * np.exp(self.growth_rate * years_passed)
        return self.population

    def get_population(self):
        return round(self.population, 2)  # Округляем до 2 знаков после запятой


if __name__ == "__main__":
    game = Game()
    game.start()