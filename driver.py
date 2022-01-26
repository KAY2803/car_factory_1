from dataclasses import dataclass
from utils import check_types, check_type
import datetime

@dataclass
class Experience:
    newbie: tuple = None
    middle: tuple = None
    profi: tuple = None
    current_experience: int = 0


class Driver:
    def __init__(self, name: str, experience: Experience):
        self.__name = name
        self.__experience = experience

        self.__check_experience(experience.current_experience)
        self.__license = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__name})"

    def __str__(self):
        return f"Водитель {self.__name}"

    def get_experience(self):
        return self.__experience

    @staticmethod
    def __check_experience(exp):
        if exp < 0:
            raise ValueError("Стаж введен не корректно")

    @property
    def license(self):
        return self.__license

    @license.setter
    def license(self, value: tuple[int, int, int, int]):
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

