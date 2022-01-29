from dataclasses import dataclass


@dataclass
class Experience:
    newbie: tuple = None
    middle: tuple = None
    profi: tuple = None
    current_experience: int = 0


class Driver:
    """
    Водитель. Может ехать, может открыть машину.
    """
    def __init__(self, name: str, experience: Experience):
        self._name = name
        self.__experience = experience

        self.__check_experience(experience.current_experience)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._name})"

    def __str__(self):
        return f"Driver {self._name}"

    def get_experience(self):
        return self.__experience

    @staticmethod
    def __check_experience(exp):
        if exp < 0:
            raise ValueError("Стаж введен не корректно.")


class Mech(Driver):
    '''
    Механик, может открыть машину, не может ехать.
    '''
    def __init__(self, mech_name):
        self._name = mech_name
        # super().__init__(name=mech_name, experience=experience)

    def __str__(self):
        return f'Mech {self._name}'


class GTA(Driver):
    '''
    Угонщик, может открыть машину, может ехать.
    Полностью подменяет водителя.
    '''
    def __init__(self, gta_name, experience):
        super().__init__(name=gta_name, experience=experience)
        self.experience = 15


if __name__ == '__main__':
    experience = Experience((0, 5), (5, 10), (10, 60), 5)

    ivan = Driver('Ivan', experience)
    alex = Driver('Alex', experience)
    uter = Mech('WAAAAAAGH!!!')
    vercetti = GTA('Tommy Vercetti', experience)

    print(ivan)
    print(alex)
    print(uter)
    print(vercetti)
