from typing import Dict, NoReturn, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        msg = (f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.')
        return msg


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_km: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_kmh: float = self.get_distance() / self.duration_h
        return mean_speed_kmh

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Нет реализации метода в классе:'
                                  f'{type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(type(self).__name__,
                                    self.duration_h,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    MEAN_SPEED_MULTIPLIER: float = 18
    MEAN_SPEED_SUBTRAHEND: float = 20

    def get_spent_calories(self) -> float:
        spent_calories_kcal: float = ((self.MEAN_SPEED_MULTIPLIER
                                      * self.get_mean_speed()
                                      - self.MEAN_SPEED_SUBTRAHEND)
                                      * self.weight_kg / self.M_IN_KM
                                      * self.duration_h * self.MIN_IN_H)
        return spent_calories_kcal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_WEIGHT_MULTIPLIER: float = 0.035
    SECOND_WEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm: float = height

    def get_spent_calories(self) -> float:
        spent_calories_kcal: float = ((self.FIRST_WEIGHT_MULTIPLIER
                                      * self.weight_kg
                                      + (self.get_mean_speed()
                                          ** 2 // self.height_cm)
                                      * self.SECOND_WEIGHT_MULTIPLIER
                                      * self.weight_kg)
                                      * self.duration_h * self.MIN_IN_H)
        return spent_calories_kcal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    MEAN_SPEED_SUMMAND: float = 1.1
    MEAN_SPEED_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        mean_speed_kmh: float = (self.length_pool_m * self.count_pool
                                 / self.M_IN_KM / self.duration_h)
        return mean_speed_kmh

    def get_spent_calories(self) -> float:
        spent_calories_kcal: float = ((self.get_mean_speed()
                                      + self.MEAN_SPEED_SUMMAND)
                                      * self.MEAN_SPEED_MULTIPLIER
                                      * self.weight_kg)
        return spent_calories_kcal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    """Добавление GuardBlock"""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if not workout_type:
        message = (f'Нет такой тренировки: {workout_type}'
                   f'Ожидали: {str.join(*workout_type)}')
        raise ValueError(message)
    return training_type[workout_type](*data)


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
