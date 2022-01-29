""" Модуль, который описывает класс Driver и класс Experience"""

from dataclasses import dataclass
import datetime

from utils import check_types, check_type
from typing import Union
from utils import check_types


@dataclass
class Experience:
    """Класс, который описывает водительский стаж

    newbie: диапазон лет, который представляет собой небольшой стаж вождения
    middle: диапазон лет, который представляет собой средний стаж вождения
    profi: диапазон лет, который представляет собой большой стаж вождения
    current_experience: текущий стаж вождения

    """

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
        """Инициализируем водителя

        :param name: имя водителя
        :param experience: стаж вождения

        """
        self.__name = name
        self.__experience = experience

        self.__check_experience(experience.current_experience)
        self.__license = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__name})"

    def __str__(self):
        return f"Водитель {self.__name}"

    def get_experience(self):
        """Метод, который возвращает стаж вождения"""
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
        """Метод, который проверяет корректность введеного значения текущего стажа вождения
        (значение не может быть отрицательным числом)

        """
        check_types(exp, (int, float))

        if exp < 0:
            raise ValueError("Стаж введен не корректно")

    @property
    def license(self):
        """Свойство, которое возвращает данные водительских прав"""
        return self.__license

    @license.setter
    def license(self, value: tuple[int, int, int, int]):
        """Свойство, которое присваивает значение водительским правам, предварительно проведя проверку введенных данных

        :param value: значение из 4 целых чисел, первое из которых - номер прав из 10 цифр; второе - год выдачи прав;
        третье - месяц выдачи прав; четвертое - дата выдачи прав. Данные даты выдачи прав должны вводиться в формате,
        подходящем для модуля datetime. Период действия прав не может превышать 10 лет с даты выдачи.
        :return: возвращает строковое значение в виде номера и даты выдачи прав

        """
        check_types(value, int)
        if len(str(value[0])) != 10:
            raise ValueError(f'Права не существуют')
        year = value[1]
        month = value[2]
        day = value[3]
        license_date = datetime.date(year, month, day)
        valid_period = datetime.date.today() - license_date
        if valid_period.days > 3652:
            raise ValueError("Права просрочены")
        self.__license = f'права № {value[0]} от {license_date.strftime("%d.%m.%Y")}'


if __name__ == '__main__':

    experience_ivan = Experience((0, 5), (5, 15), (15, 100), 13)
    experience_alex = Experience((0, 5), (5, 15), (15, 100), 16)
    experience = Experience((0, 5), (5, 10), (10, 60), 5)
    #experience = Experience((0, 5), (5, 10), (10, 60), -1)

    ivan = Driver("Иван", experience_ivan)
    alex = Driver("Алексей", experience_alex)

    print(ivan.get_max_speed_driver())
    print(ivan.get_max_trip_distance())

    print("-------------")

    print(ivan)
    print(alex)

