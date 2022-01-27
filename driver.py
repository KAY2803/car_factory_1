from dataclasses import dataclass
from typing import Union
from utils import check_types


@dataclass
class Experience:
    newbie: tuple = None
    middle: tuple = None
    professional: tuple = None
    current_experience: Union[int, float] = 0

    def get_max_speed_driver(self):
        max_speed_driver = 0
        if self.newbie[0] <= self.current_experience < self.newbie[1]:
            max_speed_driver = 90
        if self.middle[0] <= self.current_experience < self.middle[1]:
            max_speed_driver = 120
        if self.professional[0] <= self.current_experience < self.professional[1]:
            max_speed_driver = 150
        return max_speed_driver


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

    print(experience_alex.get_max_speed_driver())
    print(experience_ivan.get_max_speed_driver())

    print(ivan.get_experience().get_max_speed_driver())

    print(ivan)
    print(alex)
