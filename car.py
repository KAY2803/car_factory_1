import time
import random
from utils import check_type, check_types
from custom_errors import *
from driver import Driver, Mech, GTA, Experience


class Car:
    brand = None
    _max_speed = 180
    __created_car = 0

    def __init__(self, color, body_type, model_name,
                 engine_type, gear_type, complectation):

        self.__model_name = model_name
        self.__body_type = body_type
        self._engine_type = engine_type
        self._gear_type = gear_type
        self.complectation = complectation
        self.color = color

        self.__mileage = 0
        self.__driver = None
        self.__mech = None
        self.__engine_status = False
        self.__count_to = 0
        self.__status_to = False

        self.__key_owner = False

    def __new__(cls, *args, **kwargs):
        cls.__append_new_car_counter()
        print(f"Выпущено {cls.__created_car} автомобилей, класса {cls.__name__}")
        return super().__new__(cls)

    # =============
    # Методы класса
    # =============

    @classmethod
    def change_brand(cls, new_brand: str):
        cls.brand = new_brand

    @classmethod
    def _change_max_speed(cls, max_speed):
        check_type(max_speed, (int, float))

        cls._max_speed = max_speed

    @classmethod
    def __append_new_car_counter(cls):
        cls.__created_car += 1

    # ==================
    # Статические методы
    # ==================

    @property
    def driver(self):
        """
        Возвращает имя водителя.
        :return: self.__driver
        """
        return self.__driver

    @driver.setter
    def driver(self, driver: (Driver, GTA)):
        """
        Разрешает водителю запустить двигатель и катиться из гаража.
        :param driver: Driver, GTA
        :return: __driver = driver, __key_owner = True
        """
        if not isinstance(driver, (Driver, GTA)):
            raise DriverTypeError(f"Ожидается {Driver}, получено {type(driver)}")
        if isinstance(driver, Mech):
            raise DriverTypeError(f'Ожидается {Driver}, получено{type(driver)}')
        self.__driver = driver
        self.__key_owner = True

    @property
    def mech(self):
        """
        Возвращает имя мекбоя.
        :return: self.__mech
        """
        return self.__mech

    @mech.setter
    def mech(self, mech: Mech) -> None:
        """
        Разрешает мекбою запустить двигатель.
        :param mech: Mech.
        :return: param __key_owner: True, __driver = None
        """
        if not isinstance(mech, Mech):
            raise DriverTypeError(f'Used to be {type(Mech)}, instead{type(mech)}')
        self.__key_owner = True
        self.__driver = None

    # Эквивалент свойствам (property)
    # def set_driver(self, driver: Driver):
    #     if not isinstance(driver, Driver):
    #         raise DriverTypeError(f"Ожидается {Driver}, получено {type(driver)}")
    #     self.__driver = driver
    #
    # def get_driver(self):
    #     return self.__driver

    # Блок отработки движения машины
    # def start_engine(self):
    #     self.__engine_status = True

    @property
    def start_engine(self) -> bool:
        """
        Статус двигателя.
        :return: __engine_status
        """
        return self.__engine_status

    @start_engine.setter
    def start_engine(self, key_owner: bool) -> None:
        """
        Запуск двигателя если __key_owner is True.
        :param key_owner: True/False
        :return: __engine_status
        """
        if self.__key_owner is True:
            self.__engine_status = True
        else:
            print('Нет ключей.')

    def __check_driver(self) -> bool:
        """
        Проверка наличия водителя, если self.driver is not None.
        :return: True/False
        """
        if self.driver is not None:
            return True
        return False

    def alarm_status(self) -> bool:
        """
        Установка статуса сигнализации в зависимости от self.driver и self.__key_owner.
        :return: True/False
        """
        if self.driver is not None and self.__key_owner:
            return True
        return False

    def __ready_status(self) -> bool:
        """
        Проверка статуса готовности к поездке:
        - alarm_status
        - __engine_status
        - __check_driver
        - check_to
        :return: Exception/True
        """
        if not self.alarm_status():
            raise AlarmOn('Alarm!')
        if not self.__engine_status:
            raise EngineIsNotRunning("Двигатель не запущен.")
        if not self.__check_driver():
            raise DriverNotFound("Водитель не найден.")
        if not self.check_to():
            raise TechnicInspection(f"ТО не пройдено. Автомобиль не поедет.")

        return True

    def move(self, distance=10) -> None:
        """
        Модуль движения.
        :param distance: Расстояние.
        :return: None/Exception
        """
        try:
            if self.__ready_status():
                part_distance = 0
                for i in range(distance):
                    print(f'Машина проехала {i+1} км.')
                    part_distance += 1
                    self.__traffic_lights(2)
                    time.sleep(0.3)
                    self.__mileage += 1
                    time_driving = part_distance / 60
                    print(f'Непрерывное время в пути {time_driving}')

                    try:
                        if time_driving >= 0.1:
                            raise MoveStop
                    except MoveStop:
                        print('Требуется принудительная остановка 5 сек.')
                        time.sleep(5)
                        part_distance = 0

                    print('\n\n')

                print('Путь пройден')
        except (EngineIsNotRunning, DriverNotFound, AlarmOn) as e:
            print(f"Машина не может начать движение, т.к. {e}")
    # /Блок отработки движения машины

    def make_to(self) -> None:
        """
        Счётчик времени до ТО.
        :return: None
        """
        self.__count_to += 1
        self.__status_to = False

    def check_to(self) -> bool:
        """
        Выставляет статус ТО в зависимости от пробега.
        :return: True/False
        """
        if self.__mileage % 30 > 0 and self.__status_to:
            print(f"{self.__driver}, Вы не можете ехать без пройденного ТО")
            return False
        if self.__mileage >= 20:
            self.__status_to = True
            print(f"Необходимо пройти ТО, можно проехать еще 10 км, после автомобиль не поедет")
        return True

    # Блок светофора
    @staticmethod
    def __traffic_lights(sleep_time) -> None:
        """
        Светофор
        """
        rand_bool = random.choice([True, False])  # случайно выбирается состояние светофора
        if rand_bool:
            print(f"Светофор красный, нужно подождать {sleep_time} сек.")
            time.sleep(sleep_time)  # если светофор True красный, то ждем 1 секунду
    # /Блок светофора
# /Блок отработки движения.

# Блок работы с защищёнными методами.
    @property
    def _mileage(self) -> int:
        """
        Пробег ТС.
        :return: int
        """
        return self.__mileage

    @_mileage.setter
    def _mileage(self, mileage) -> None:
        """
        Установка пробега ТС.
        :param mileage: int
        :return: None
        """
        if not isinstance(mileage, (int, float)):
            raise TypeError(f"Ожидается {int} или {float}, получено {type(mileage)}")

        self.__mileage = mileage
    # /Блок работы с защищёнными методами


if __name__ == '__main__':

    car = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')
    car_2 = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')

    # car.driver = Driver("Иван", Experience((0, 5), (5, 10), (10, 60), 5))
    car.driver = GTA("Иван", Experience((0, 5), (5, 10), (10, 60), 5))
    # car.driver = Mech("Иван")
    car.start_engine = "Заведись"
    car.move()

