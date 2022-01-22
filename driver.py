from dataclasses import dataclass


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


if __name__ == '__main__':
    experience = Experience((0, 5), (5, 10), (10, 60), 5)
    experience = Experience((0, 5), (5, 10), (10, 60), -1)

    ivan = Driver("Иван", experience)
    alex = Driver("Алексей", experience)

    print(ivan)
    print(alex)

