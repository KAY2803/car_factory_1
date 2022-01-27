""" Модуль, который описывает класс Driver и класс Experience"""

from dataclasses import dataclass
import datetime

from utils import check_types, check_type


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
    profi: tuple = None
    current_experience: int = 0


class Driver:
    """Класс, который описывает водителя транспортного средства.

    Переменные класс:
    name: имя водителя
    experience: стаж вождения
    Водитель характеризуется опытом вождения, может иметь права.

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

    @staticmethod
    def __check_experience(exp):
        """Метод, который проверяет корректность введеного значения текущего стажа вождения
        (значение не может быть отрицательным числом)

        """
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
    experience = Experience((0, 5), (5, 10), (10, 60), 5)
    #experience = Experience((0, 5), (5, 10), (10, 60), -1)

    ivan = Driver("Иван", experience)
    alex = Driver("Алексей", experience)

    print(ivan)
    print(alex)

