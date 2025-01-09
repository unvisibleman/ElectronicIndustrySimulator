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
        self.OVERACHIEVEMENT_BONUS = 0.0015  # Увеличение темпа роста при перевыполнении


    def check_plan_end(self, year):
        """Проверяет, закончился ли текущий план"""
        if not self.current_plan:
            return False
        _, end_year = self.current_plan
        return year > end_year

    def start_plan(self, year):
        """Начинает новый план"""
        for period, plan in self.plans.items():
            start_year, end_year = period
            if start_year <= year <= end_year:
                self.current_plan = period
                if not plan["completed"]:
                    plan["completed"] = {product: 0 for product in plan["goals"]}
                return True
        return False

    def add_production(self, product_name, amount=1):
        """Учитывает произведенную продукцию"""
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

__all__ = ['FiveYearPlan']