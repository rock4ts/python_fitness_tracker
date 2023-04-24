from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO_MESSAGE = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.INFO_MESSAGE.format(**asdict(self))


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
        """Получить дистанцию в км."""
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
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        spent_calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             - self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
            ) / self.M_IN_KM * self.duration * self.TO_MINUTES
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WEIGHT_MULTIPLIER: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029
    MEAN_SPEED_POWER: int = 2

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""

        spent_calories = (
            self.weight * self.WEIGHT_MULTIPLIER +
            + (self.get_mean_speed()**self.MEAN_SPEED_POWER // self.height)
            * self.weight * self.WEIGHT_MULTIPLIER_2
            ) * self.duration * self.TO_MINUTES
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: int
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        swim_length = self.length_pool * self.count_pool / self.M_IN_KM
        mean_speed = swim_length / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        spent_calories = (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER) * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout_dict:
        training_class = workout_dict[workout_type]
        training_results = training_class(*data)
        return training_results
    else:
        print("Wrong key.")


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
