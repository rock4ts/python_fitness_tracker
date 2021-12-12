from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float  # duration_h учту, здесь pytest не принимает :(
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    TO_MINUTES: ClassVar[int] = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км для бега и ходьбы."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        results_message = InfoMessage(type(self).__name__,
                                      self.duration,
                                      self.get_distance(),
                                      self.get_mean_speed(),
                                      self.get_spent_calories())
        return results_message


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        COEFF_1: int = 18
        DEDUCTOR_1: int = 20
        spent_calories = (
            (COEFF_1 * self.get_mean_speed() - DEDUCTOR_1)
            * self.weight) / self.M_IN_KM * self.duration * self.TO_MINUTES
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        COEFF_1: float = 0.035
        COEFF_2: float = 0.029
        DEGREE_1: int = 2
        spent_calories = (
            COEFF_1 * self.weight +
            + ((self.get_mean_speed()**DEGREE_1 // self.height) * COEFF_2)
            * self.weight) * self.duration * self.TO_MINUTES
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swim_length = self.length_pool * self.count_pool
        mean_speed = swim_length / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        INCREMENT_1: float = 1.1
        COEFF_1: int = 2
        spent_calories = (
            (self.get_mean_speed() + INCREMENT_1) * COEFF_1) * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout:
        training_class = workout[workout_type]
        training_results = training_class(*data)
        return training_results
    else:
        print("Wrong key.")


# try:
#     training_class = workout[workout_type]
#     training_results = training_class(*data)
#     return training_results
# except KeyError as "Key not in workout dict.":
#     print("Неверная аббревиатура типа тренировки.")
# как правильней, оптимальней будет?


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
