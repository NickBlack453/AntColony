from abc import abstractmethod
from typing import List
from random import random, shuffle
from tkinter import *
import copy


# Конфигурация
class AntsColonyConfig:
    def __init__(self, maxQueens: int, queenBabies: int, queenResources: float, probSoldier: float, probAttack: float, pctAttack: float, powerAttack: int) -> None:
        self.maxQueens = maxQueens
        self.queenBabies = queenBabies
        self.queenResources = queenResources
        self.probSoldier = probSoldier
        self.probAttack = probAttack
        self.pctAttack = pctAttack
        self.powerAttack = powerAttack

# Состав колонии и ресурсы
class AntsColonyState:
    def __init__(self, queens: int, soldiers: int, workers: int, babies: int, resources: float) -> None:
        self.queens = queens
        self.soldiers = soldiers
        self.workers = workers
        self.babies = babies
        self.resources = resources

    def __str__(self) -> str:
        return 'Матки: {}, Солдаты: {}, Рабочие: {}, Личинки: {}, Ресурсы: {}'.format(self.queens, self.soldiers, self.workers, self.babies, self.resources)

    def count(self) -> int:
        return self.queens + self.soldiers + self.workers + self.babies

    def increase(self, antClass):
        if antClass == QueenAnt.__name__:
            self.queens += 1
        elif antClass == SoldierAnt.__name__:
            self.soldiers += 1
        elif antClass == WorkerAnt.__name__:
            self.workers += 1
        elif antClass == BabyAnt.__name__:
            self.babies += 1

    def decrease(self, antClass):
        if antClass == QueenAnt.__name__:
            self.queens -= 1
        elif antClass == SoldierAnt.__name__:
            self.soldiers -= 1
        elif antClass == WorkerAnt.__name__:
            self.workers -= 1
        elif antClass == BabyAnt.__name__:
            self.babies -= 1

    def produceResources(self, amount: float):
        self.resources += amount

    def consumeResources(self, amount: float):
        if self.resources > amount:
            self.resources -= amount
        else:
            self.resources = 0


# Интерфейс
class AntColonyInterface:
    config: AntsColonyConfig
    state: AntsColonyState

    @abstractmethod
    def addAnt(self, ant):
        pass

    @abstractmethod
    def removeAnt(self, ant):
        pass

    @abstractmethod
    def produceResources(self, amount: float):
        pass

    @abstractmethod
    def consumeResources(self, amount: float):
        pass

    @abstractmethod
    def canAddQueens(self) -> bool:
        pass

    @abstractmethod
    def simulate(self, days: int) -> int:
        pass

    @abstractmethod
    def printHistory(self):
        pass

    @abstractmethod
    def listHistory(self) -> List[str]:
        pass

    @abstractmethod
    def drawHistory(self, canvas: Canvas):
        pass

# Классы муравьёв
# Муравей
class Ant:
    DEFAULT_RESOURCE_CONSUMPTION = 1
    age = 0

    @staticmethod
    def resourcesConsumption() -> float:
        return Ant.DEFAULT_RESOURCE_CONSUMPTION

    def simulateDay(self, colony: AntColonyInterface):
        self.age += 1
        colony.consumeResources(self.resourcesConsumption())


# Матка
class QueenAnt(Ant):
    QUEEN_RESOURCE_CONSUMPTION = 10

    @staticmethod
    def resourcesConsumption() -> float:
        return QueenAnt.QUEEN_RESOURCE_CONSUMPTION

    def simulateDay(self, colony: AntColonyInterface):
        Ant.simulateDay(self, colony)

        for baby in range(colony.config.queenBabies):
            colony.addAnt(BabyAnt())


# Рабочий
class WorkerAnt(Ant):
    PRODUCED_RESOURCES = 3.0

    def simulateDay(self, colony: AntColonyInterface):
        Ant.simulateDay(self, colony)
        colony.produceResources(WorkerAnt.PRODUCED_RESOURCES)


# Солдат
class SoldierAnt(Ant):
    SOLDIER_RESOURCE_CONSUMPTION = 2

    @staticmethod
    def resourcesConsumption() -> float:
        return SoldierAnt.SOLDIER_RESOURCE_CONSUMPTION


# Личинка
class BabyAnt(Ant):
    BABY_RESOURCE_CONSUMPTION = 2
    BABY_DAYS = 30

    @staticmethod
    def resourcesConsumption() -> float:
        return BabyAnt.BABY_RESOURCE_CONSUMPTION

    def simulateDay(self, colony: AntColonyInterface):
        Ant.simulateDay(self, colony)

        if self.age >= BabyAnt.BABY_DAYS:
            colony.removeAnt(self)
            if colony.canAddQueens():
                colony.addAnt(QueenAnt())
            elif random() <= colony.config.probSoldier:
                colony.addAnt(SoldierAnt())
            else:
                colony.addAnt(WorkerAnt())

# Колония
class AntColony(AntColonyInterface):
    ants: List[Ant]
    history: List[AntsColonyState]

    def addAnt(self, ant: Ant):
        self.ants.append(ant)
        self.state.increase(ant.__class__.__name__)

    def removeAnt(self, ant):
        if ant in self.ants:
            self.ants.remove(ant)
            self.state.decrease(ant.__class__.__name__)

    def produceResources(self, amount: float):
        self.state.produceResources(amount)

    def consumeResources(self, amount: float):
        self.state.consumeResources(amount)

    def canAddQueens(self) -> bool:
        return self.state.queens < self.config.maxQueens and self.config.queenResources * (self.state.queens+1) < self.state.resources

    def __init__(self, config: AntsColonyConfig, state: AntsColonyState) -> None:
        self.config = config
        self.state = AntsColonyState(0, 0, 0, 0, state.resources)
        self.ants = []
        self.history = []

        for i in range(state.queens):
            self.addAnt(QueenAnt())

        for i in range(state.soldiers):
            self.addAnt(SoldierAnt())

        for i in range(state.workers):
            self.addAnt(WorkerAnt())

        for i in range(state.babies):
            self.addAnt(BabyAnt())

        assert self.state.queens == state.queens and self.state.soldiers == state.soldiers and self.state.workers == state.workers and self.state.babies == state.babies

    def simulate(self, days: int) -> int:
        for day in range(days):
            if random() <= self.config.probAttack:
                shuffle(self.ants)
                attackCount = int(self.state.count() * self.config.pctAttack / 100.0)

                for attacker in range(attackCount):
                    killed = 0
                    self.consumeResources(50)
                    for ant in self.ants:
                        if ant.__class__.__name__ == QueenAnt.__name__:
                            continue

                        if ant.__class__.__name__ == SoldierAnt.__name__:
                            self.removeAnt(ant)
                            break

                        self.removeAnt(ant)
                        killed += 1
                        if killed >= self.config.powerAttack:
                            break

            for ant in self.ants:
                if self.state.resources > 0:
                    ant.simulateDay(self)
                else:
                    self.removeAnt(ant)

            self.history.append(copy.copy(self.state))

            if self.state.count() == 0:
                return day + 1

        return day + 1

    def printHistory(self):
        for day in range(len(self.history)):
            print('{}. {}'.format(day+1, self.history[day]))

    def listHistory(self) -> List[str]:
        days = []
        for day in range(len(self.history)):
            days.append('{}. {}'.format(day+1, self.history[day]))
        return days

    def drawHistory(self, canvas: Canvas):
        canvas.delete('all')
        width = canvas.winfo_width()
        maxCount = 0
        for day in range(len(self.history)):
            count = self.history[day].count()
            if count > maxCount:
                maxCount = count

        for day in range(len(self.history)):
            rec = self.history[day]
            x = 0.0
            queensWidth = width * rec.queens / maxCount
            if queensWidth < 1 and rec.queens > 0:
                queensWidth = 1.0
            canvas.create_line(x, day, x+queensWidth, day, fill='red')
            x += queensWidth

            soldiersWidth = width * rec.soldiers / maxCount
            canvas.create_line(x, day, x+soldiersWidth, day, fill='green')
            x += soldiersWidth

            workersWidth = width * rec.workers / maxCount
            canvas.create_line(x, day, x+workersWidth, day, fill='yellow')
            x += workersWidth

            babiesWidth = width * rec.babies / maxCount
            canvas.create_line(x, day, x+babiesWidth, day, fill='gray')
            x += babiesWidth
