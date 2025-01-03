import numpy as np

class Game:
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
        
        # Добавляем форматирование заголовков и разделителей
        c = self.COLORS
        self.HEADERS = {
            'event': f"\n{c['bold']}!!! ВАЖНОЕ СОБЫТИЕ !!!{c['end']}",
            'war': f"\n{c['bold']}{c['red']}!!! ВОЕННОЕ ПОЛОЖЕНИЕ !!!{c['end']}",
            'achievement': f"\n{c['bold']}{c['green']}!!! ДОСТИЖЕНИЕ !!!{c['end']}",
            'bankruptcy': f"\n{c['bold']}{c['red']}!!! БАНКРОТСТВО !!!{c['end']}"
        }
        
        self.DIVIDERS = {
            'simple': f"{c['white']}------------------------{c['end']}",
            'double': f"{c['white']}========================{c['end']}",
            'status': f"{c['white']}-----------------------{c['end']}"
        }
        
        self.year = 1918
        self.five_year_plans = []
        self.current_plan = None
        self.tecnologies = TechnologyTree()
        self.rubles = 1000  # Начальное количество рублей
        self.dollars = 500   # Начальное количество долларов
        self.population_stats = PopulationStats()
        self.products = {}  # Хранит информацию о произведенных товарах
        self.BASE_PRODUCT_PRICE = 1000  # Базовая цена товара в рублях
        self.BASE_TECHNOLOGY_PRICE = 500  # Базовая цена технологии в долларах
        self.DEPRECIATION_RATE = 0.1  # 10% обесценивание в год
        self.last_command = None  # Добавляем сохранение последней команды
        self.research_in_progress = {}  # Добавляем словарь для отслеживания процесса исследования {tech_name: years_spent}
        self.BASE_POPULATION = 150  # Базовое население в млн (1926 год)
        self.POPULATION_PRICE_FACTOR = 1.5  # Коэффициент влияния населения на цену
        self.command_capacity = 1 # Количество команд в год
        
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
                "описание": "Микросхемы средней степени интеграции",
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
                "описание": "Схемы с высокой степенью интеграции",
                "уровни": {
                    "начальная": "Простые микропроцессоры",
                    "средняя": "Микроконтроллеры",
                    "продвинутая": "Специализированные процессоры"
                }
            },
            "бис": {
                "описание": "Большие интегральные схемы",
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
                "описание": "Сверхбольшие интегральные схемы",
                "уровни": {
                    "начальная": "Базовые СБИС",
                    "средняя": "Сложные процессоры",
                    "продвинутая": "Многоядерные процессоры и видеочипы"
                }
            }
        }

    def start(self):
        print("Добрый день! Вы - глава электронной промышленности СССР. Ваша задача - построить электронную промышленность СССР!")
        self.help_command();
        self.main_loop()

    def main_loop(self):
        while True:
            c = self.COLORS
            # Проверка исторических событий
            if self.year == 1924:
                print(self.HEADERS['event'])
                print(f"{c['yellow']}Начало выпуска журнала Радио!{c['end']}")
                print(self.DIVIDERS['simple'])
            elif self.year == 1932:
                print(self.HEADERS['event'])
                print(f"{c['yellow']}Получены первые сведения о возможной угрозе войны с Германией!{c['end']}")
                print(self.DIVIDERS['simple'])
            elif self.year == 1941:
                print(self.HEADERS['war'])
                print(f"{c['red']}Началась Великая Отечественная война!{c['end']}")
                print(f"{c['red']}На эвакуацию заводов требуется 10000 рублей{c['end']}")
                self.rubles -= 10000
                if self.check_bankruptcy():
                    return
                print(self.DIVIDERS['simple'])
            elif self.year > 1941 and self.year < 1945:
                print(self.HEADERS['war'])
                print(f"{c['red']}Великая Отечественная война продолжается!{c['end']}")
                print(f"{c['red']}Фронту требуется 2000 рублей{c['end']}")
                self.rubles -= 2000
                if self.check_bankruptcy():
                    return
                print(self.DIVIDERS['simple'])
            elif self.year == 1945:
                print(self.HEADERS['achievement'])
                print(f"{c['yellow']}Великая Отечественная война закончилась!{c['end']}")
                print(self.DIVIDERS['simple'])
            elif self.year == 1952:
                print(self.HEADERS['achievement'])
                print(f"{c['green']}Наши ученые построили первую в стране ЭВМ! Теперь вы можете использовать 2 команды в год!{c['end']}")
                self.command_capacity = 2
                print(self.DIVIDERS['simple'])
            elif self.year == 1956:
                print(self.HEADERS['event'])
                print("Начато проектирование первого искусственного спутника Земли!")
                print("На это потребуется 10000 рублей")
                self.rubles -= 10000
                if self.check_bankruptcy():
                    return
                print(self.DIVIDERS['simple'])
            elif self.year == 1957:
                print(self.HEADERS['achievement'])
                print("Успешный запуск первого искусственного спутника Земли!")
                print(self.DIVIDERS['simple'])
            elif self.year == 1958:
                print(self.HEADERS['event'])
                print("Начато проектирование пилотируемого космического корабля!")
                print("На это потребуется 10000 рублей")
                self.rubles -= 10000
                if self.check_bankruptcy():
                    return
                print(self.DIVIDERS['simple'])
            elif self.year == 1961:
                print(self.HEADERS['achievement'])
                print("Юрий Гагарин стал первым человеком в космосе!")
                print(self.DIVIDERS['simple'])
            elif self.year == 1984:
                print(self.HEADERS['event'])
                print("Начало выпуска журнала Микропроцессорные средства и системы!")
                print(self.DIVIDERS['simple'])
            elif self.year == 1991:
                print(self.HEADERS['achievement'])
                print("В этот год могла произойти контрреволюция!")
                print(self.DIVIDERS['simple'])

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
        c = self.COLORS
        print(f"{c['bold']}{c['blue']}Год: {self.year}{c['end']}")
        print(f"{c['green']}Рубли: {self.rubles:.2f}{c['end']}, {c['yellow']}Доллары: {self.dollars:.2f}{c['end']}")
        print(f"{c['cyan']}Текущая пятилетка: {self.current_plan}{c['end']}")
        
        # Доступные технологии
        print(f"\n{c['magenta']}Доступные технологии:{c['end']}")
        available_techs = self.tecnologies.get_available_technologies(self.year)
        if available_techs:
            for tech in available_techs:
                print(f"  • {tech}")
        else:
            print("  Нет доступных технологий")
        
        # Освоенные технологии
        print(f"\n{c['cyan']}Освоенные технологии:{c['end']}")
        tech_status = self.tecnologies.get_status()
        if tech_status:
            for tech, details in tech_status.items():
                if "уровень" in details and details["уровень"] != "исследуется":
                    level_color = {
                        "начальная": c['white'],
                        "средняя": c['yellow'],
                        "продвинутая": c['green']
                    }.get(details["уровень"], c['white'])
                    
                    print(f"  • {c['bold']}{tech}{c['end']} - {level_color}{details['уровень']}{c['end']} - Год освоения: {details['год освоения']}")
                elif "уровень" in details and details["уровень"] == "исследуется":
                    print(f"  • {c['bold']}{tech}{c['end']} - {c['yellow']}{details['прогресс']}{c['end']}")
        else:
            print("  Нет освоенных технологий")
        
        print(f"\n{c['green']}Население: {self.population_stats.get_population():.2f} млн. человек{c['end']}")
        print(self.DIVIDERS['status'])

    def process_command(self, command):
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

            if cmd == "помощь":
                self.help_command()
                return "help"  # Специальное возвращаемое значение для команды помощи
            elif cmd == "план":
                if len(parts) != 2:
                    print("Использование: план ГОД")
                    return "invalid"
                try:
                    year = int(parts[1])
                    self.start_five_year_plan(year)
                    return "valid"
                except ValueError:
                    print("Год должен быть числом")
                    return "invalid"
            elif cmd == "отчет":
                if len(parts) > 1:
                    print("Команда 'отчет' не требует дополнительных аргументов")
                    return "invalid"
                self.report_progress()
                return "valid"
            elif cmd == "исследовать":
                if len(parts) < 2:
                    print("Использование: исследовать ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]")
                    return "invalid"
                self.tecnologies.update_current_year(self.year)
                for tech in parts[1:]:
                    print(f"\nИсследование {tech}:")
                    self.tecnologies.research(tech.lower(), self.rubles)
                return "valid"
            elif cmd == "произвести":
                if len(parts) < 2:
                    print("Использование: произвести ТОВАР [ТОВАР ...]")
                    return "invalid"
                for product in parts[1:]:
                    print(f"\nПроизводство {product}:")
                    self.produce_product(product.lower())
                return "valid"
            elif cmd == "продажа_технологий":
                if len(parts) < 2:
                    print("Использование: продажа_технологий ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]")
                    return "invalid"
                for tech in parts[1:]:
                    print(f"\nПродажа {tech}:")
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
            elif cmd == "что_такое":
                if len(parts) != 2:
                    print("Использование: что_такое ТЕХНОЛОГИЯ")
                    return "invalid"
                self.show_tech_info(parts[1].lower())
                return "help"  # Не тратит игровой ход
            else:
                print("Неизвестная команда. Введите 'помощь' для списка команд.")
                return "invalid"
        except Exception as e:
            print(f"Произошла ошибка при выполнении команды: {str(e)}")
            return "invalid"

    def help_command(self):
        c = self.COLORS
        print(f"\n{c['bold']}{c['cyan']}Доступные команды:{c['end']}")
        print(f"{c['yellow']}помощь{c['end']} - вывести справку по командам")
        print(f"{c['yellow']}что_такое ТЕХНОЛОГИЯ{c['end']} - получить описание технологии")
        print(f"{c['yellow']}план ГОД{c['end']} - начать пятилетний план")
        print(f"{c['yellow']}отчет{c['end']} - вывести отчет о пятилетнем плане")
        print(f"{c['yellow']}исследовать ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]{c['end']} - исследовать одну или несколько технологий")
        print(f"{c['yellow']}купить_технологию ТЕХНОЛОГИЯ{c['end']} - купить технологию за доллары")
        print(f"{c['yellow']}произвести ТОВАР [ТОВАР ...]{c['end']} - производство одного или нескольких товаров")
        print(f"{c['yellow']}продажа_технологий ТЕХНОЛОГИЯ [ТЕХНОЛОГИЯ ...]{c['end']} - продажа одной или нескольких технологий за рубеж")
        print(f"{c['yellow']}пропуск{c['end']} - пропустить текущий ход")
        print(f"{c['yellow']}повтор{c['end']} - повторить предыдущую команду")
        print(f"{c['red']}выход (или exit, quit){c['end']} - завершить игру\n")

    def start_five_year_plan(self, year):
        # Инициализация пятилетнего плана
        self.current_plan = FiveYearPlan(year)
        print(f"Пятилетний план на {year} начат.")

    def report_progress(self):
        if self.current_plan:
            print(f"Отчет о пятилетнем плане {self.current_plan.year} - В процессе.")
        else:
            print("Нет активного пятилетнего плана.")
    
    def calculate_depreciation(self, base_price, year_learned):
        """Расчет цены с учетом устаревания и численности населения"""
        # Рассчитываем базовое устаревание
        years_passed = self.year - year_learned
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
        
        # Рассчитываем базовую цену с учетом уровня технологии
        base_price = self.BASE_PRODUCT_PRICE
        if current_level == "средняя":
            base_price *= 1.5
        elif current_level == "продвинутая":
            base_price *= 2.0
        
        # Рассчитываем итоговую цену с учетом устаревания и населения
        price = self.calculate_depreciation(base_price, year_learned)
        
        self.products[product_name] = self.products.get(product_name, 0) + 1
        self.rubles += price
        print(f"Произведен {product_name}. Доход от продажи: {price:.2f} рублей")

    # Продажа технологий за рубеж
    def sell_technology(self, tech_name):
        if tech_name in self.tecnologies.get_status():
            tech_status = self.tecnologies.get_status()[tech_name]
            year_learned = tech_status["год освоения"]
            
            # Рассчитываем цену с учетом устаревания и уровня технологии
            base_price = self.BASE_TECHNOLOGY_PRICE
            if tech_status["уровень"] == "средняя":
                base_price *= 2.0
            elif tech_status["уровень"] == "продвинутая":
                base_price *= 3.0
            
            price = self.calculate_depreciation(base_price, year_learned)
            
            self.dollars += price
            print(f"Продажа технологии {tech_name} принесла {price:.2f} долларов")
        else:
            print("Технология не освоена.")

    def check_bankruptcy(self):
        c = self.COLORS
        if self.rubles < 0:
            print(self.HEADERS['bankruptcy'])
            print(f"{c['red']}Казна пуста! Промышленность в упадке!{c['end']}")
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
            print(self.DIVIDERS['double'])
            print(f"{c['red']}Игра окончена!{c['end']}")
            return True
        return False

    def buy_technology(self, tech_name):
        c = self.COLORS
        if tech_name not in self.tecnologies.get_available_technologies(self.year):
            print(f"{c['red']}Эта технология пока недоступна для покупки!{c['end']}")
            return

        if tech_name in self.tecnologies.get_status():
            print(f"{c['yellow']}Эта технология уже освоена!{c['end']}")
            return

        # Определяем стоимость технологии
        base_price = self.BASE_TECHNOLOGY_PRICE * 2  # Покупка дороже чем продажа
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
        c = self.COLORS
        if tech_name not in self.TECH_DESCRIPTIONS:
            print(f"{c['red']}Информация о технологии '{tech_name}' не найдена.{c['end']}")
            return

        tech_info = self.TECH_DESCRIPTIONS[tech_name]
        print(f"\n{c['bold']}{c['cyan']}Технология: {tech_name}{c['end']}")
        print(f"{c['white']}{tech_info['описание']}{c['end']}")
        
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
        
        print(self.DIVIDERS['simple'])


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
            "пассивка": 100,
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
                return
                
            if year_available > self.current_year:
                print(f"{tech_name} еще недоступна. Можно освоить позже.")
                return
                
            if self.resources_required[tech_name] > available_rubles:
                print(f"Недостаточно рублей для исследования {tech_name}. Необходимо: {self.resources_required[tech_name]}, доступно: {available_rubles}.")
                return

            # Проверяем, исследуется ли уже эта технология
            if tech_name not in self.research_in_progress:
                self.research_in_progress[tech_name] = 0
                print(f"Начато исследование {tech_name}. Требуется лет: {self.research_time[tech_name]}")
                return

            # Увеличиваем счетчик лет исследования
            self.research_in_progress[tech_name] += 1
            years_left = self.research_time[tech_name] - self.research_in_progress[tech_name]

            if years_left > 0:
                print(f"Исследование {tech_name} продолжается. Осталось лет: {years_left}")
                return

            # Исследование завершено
            next_level = self.levels[current_level]["upgrade"]
            self.technologies[tech_name] = (next_level, year_available, self.current_year)
            del self.research_in_progress[tech_name]  # Удаляем из списка исследуемых
            print(f"{tech_name} улучшена до уровня {next_level}.")
        else:
            print("Технология не найдена.")

    def update_current_year(self, year):
        self.current_year = year

class FiveYearPlan:
    def __init__(self, year):
        self.year = year
        self.goals = {}

    def set_goal(self, goal_name, target):
        self.goals[goal_name] = target


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