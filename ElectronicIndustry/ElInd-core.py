from TechnologyTree import TechnologyTree
from PopulationStats import PopulationStats
from ConsumerProducts import ConsumerProducts
from FiveYearPlan import FiveYearPlan
from UI import UserInterface

class Game:
    def __init__(self):
        self.year = 1918
        self.rubles = 1000 # Начальное количество рублей
        self.dollars = 500 # Начальное количество долларов
        self.products = {} # Хранит информацию о произведенных товарах
        self.consumer_products_made = {} # Статистика произведенных товаров
        self.last_command = None # Добавляем сохранение последней команды
        self.production_multiplier = 1 # Базовый множитель производительности
        self.PRODUCTION_UPGRADE_COST_RUBLES = 5000 # Стоимость улучшения в рублях
        self.PRODUCTION_UPGRADE_COST_DOLLARS = 1000 # Стоимость улучшения в долларах
        self.PRODUCTION_UPGRADE_FACTOR = 2 # Во сколько раз увеличивается производство
        self.DEPRECIATION_RATE = 0.1 # 10% обесценивание в год
        self.ui = UserInterface()
        self.tecnologies = TechnologyTree()
        self.five_year_plan = FiveYearPlan()
        self.population_stats = PopulationStats()
        self.consumer_products = ConsumerProducts()
        self.research_in_progress = {}  # Добавляем словарь для отслеживания процесса исследования {tech_name: years_spent}
        self.BASE_POPULATION = 150  # Базовое население в млн (1926 год)
        self.POPULATION_PRICE_FACTOR = 1.5  # Коэффициент влияния населения на цену
        self.command_capacity = 1 # Количество команд в год

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
        
        # Обновляем базовые цены технологий
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
        self.ui.clear_screen()
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
                if parts[1].lower() not in self.consumer_products.devices:
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
        if tech_name not in self.tecnologies.TECH_DESCRIPTIONS:
            print(f"{c['red']}Информация о технологии '{tech_name}' не найдена.{c['end']}")
            return

        tech_info = self.tecnologies.TECH_DESCRIPTIONS[tech_name]
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
        if product_name not in self.consumer_products.devices:
            return False, "Неизвестный товар"
            
        product = self.consumer_products.devices[product_name]
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
        if product_name not in self.consumer_products.devices:
            self.ui.print(self.ui.red, f"Неизвестный товар: {product_name}")
            return False
            
        product = self.consumer_products.devices[product_name]
        
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
        
        for name, product in self.consumer_products.devices.items():
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

if __name__ == "__main__":
    game = Game()
    game.start()