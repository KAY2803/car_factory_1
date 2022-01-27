from dataclasses import dataclass
from typing import Union
from utils import check_types


@dataclass
class Experience:
    newbie: tuple = None
    middle: tuple = None
    professional: tuple = None
    current_experience: Union[int, float] = 0


class Driver:
    """
    Класс Driver используется для создания водителя с определенным стажем.

    Применение - используется в классе Car как обязательное условие движения автомобиля.

    Attributes
    ----------
    __name : Any
        Имя водителя
    __experience: Experience
        Стаж вождения

    Methods
    -------
    get_experience()
        Позволяет получить доступ к стажу вождения
    get_max_speed_driver()
        Позволяет получить доступ к максимальной скорости вождения в зависимости от стажа водителя
    get_max_trip_distance
        Позволяет получить доступ к максимальному расстоянию, которое может проехать водитель, в зависимости от стажа
    __check_experience()
        Проверяет корректно введен стаж вождения
    """

    def __init__(self, name: str, experience: Experience):
        self.__name = name
        self.__experience = experience

        self.__check_experience(experience.current_experience)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__name})"

    def __str__(self):
        return f"Водитель {self.__name}"

    def get_experience(self):
        return self.__experience

    def get_max_speed_driver(self):
        max_speed_driver = None
        if self.__experience.newbie[0] <= self.__experience.current_experience < self.__experience.newbie[1]:
            max_speed_driver = 90
        if self.__experience.middle[0] <= self.__experience.current_experience < self.__experience.middle[1]:
            max_speed_driver = 120
        if self.__experience.professional[0] <= self.__experience.current_experience:
            max_speed_driver = 150
        return max_speed_driver

    def get_max_trip_distance(self):
        max_trip_distance = None
        if self.__experience.newbie[0] <= self.__experience.current_experience < self.__experience.newbie[1]:
            max_trip_distance = 20
        if self.__experience.middle[0] <= self.__experience.current_experience < self.__experience.middle[1]:
            max_trip_distance = 50
        if self.__experience.professional[0] <= self.__experience.current_experience:
            max_trip_distance = 100
        return max_trip_distance

    @staticmethod
    def __check_experience(exp):
        check_types(exp, (int, float))

        if exp < 0:
            raise ValueError("Стаж введен не корректно")


if __name__ == '__main__':

    experience_ivan = Experience((0, 5), (5, 15), (15, 60), 12)
    experience_alex = Experience((0, 5), (5, 15), (15, 60), 16)

    ivan = Driver("Иван", experience_ivan)
    alex = Driver("Алексей", experience_alex)

    print(ivan.get_max_speed_driver())

    print(ivan)
    print(alex)
