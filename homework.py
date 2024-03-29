"""Модуль фитнес-трекера, который обрабатывает данные
для трех видов тренировок: для бега,
спортивной ходьбы и плавания."""
from dataclasses import dataclass, asdict
from typing import Type, List


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Метод для создания сообщения с информацией о тренировке."""
        return self.message.format(**asdict(self))


class Training:
    """Родительский класс(тренировки)."""

    M_IN_KM: int = 1000  # константа для перевода метров в километры
    LEN_STEP: float = 0.65  # длина шага(предварительная)
    H_IN_M: int = 60  # константа для перевода часов в минуты

    def __init__(self, action: int, duration: float, weight: float) -> None:
        """Конструктор класса (принимает данные о тренировке)."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Метод для расчёта дистанции."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Метод для расчёта средней скорости."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Метод для расчёта затраченных каллорий."""
        raise NotImplementedError(
            'Переопределите get_spent_calories в {}'
            .format(self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Метод, возвращающий сообщение о тренировке."""
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Дочерний класс(бег)."""

    LEN_STEP: float = 0.65  # константа длина шага
    coeff_run_1: int = 18  # константа(коэфицент №1 для подсчёта каллорий)
    coeff_run_2: int = 20  # константа(коэфицент №2 для подсчёта каллорий)

    def get_spent_calories(self) -> float:
        """Метод для расчёта затраченных каллорий."""
        time = self.duration * self.H_IN_M
        spent_calories = ((self.coeff_run_1
                          * self.get_mean_speed()
                          - self.coeff_run_2)
                          * self.weight / self.M_IN_KM * time)
        return spent_calories


class SportsWalking(Training):
    """Дочерний класс(спортивная ходьба)."""

    LEN_STEP: float = 0.65  # const длина шага
    coeff_weight_1: float = 0.035  # const(коэфицент №1 для подсчёта каллорий)
    coeff_weight_2: float = 0.029  # const(коэфицент №2 для подсчёта каллорий)

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        """Конструктор класса (принимает данные о тренировке)."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Метод для расчёта затраченных каллорий."""
        time = self.duration * self.H_IN_M
        spent_calories = ((self.coeff_weight_1 * self.weight
                          + (self.get_mean_speed()**2 // self.height)
                          * self.coeff_weight_2 * self.weight) * time)
        return spent_calories


class Swimming(Training):
    """Дочерний класс(плавание)."""

    LEN_STEP: float = 1.38  # константа (расстояние, за один гребок)
    coeff_swim_1: float = 1.1  # константа(коэфицент №1 для подсчёта каллорий)
    coeff_swim_2: int = 2  # константа(коэфицент №2 для подсчёта каллорий)

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        """Конструктор класса (принимает данные о тренировке)."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Метод для расчёта средней скорости."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Метод для расчёта затраченных каллорий."""
        spent_calories = ((self.get_mean_speed() + self.coeff_swim_1)
                          * self.coeff_swim_2 * self.weight)
        return spent_calories


def read_package(work_type: str, workout_data: List[int]) -> Training:
    """Функция чтения принятых пакетов."""
    try:
        workout_table: dict[str, Type[Training]] = {'SWM': Swimming,
                                                    'RUN': Running,
                                                    'WLK': SportsWalking}
        train_type = workout_table[work_type]
    except KeyError:
        print('Данный тип тренировки не поддерживается.')
    train_type = train_type(*workout_data)
    return train_type


def main(workout: Training) -> None:
    """Функция для вывода информации о тренировке."""
    info: InfoMessage = workout.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Блок кода с пакетом данных, для автономного тестирования трекера."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
