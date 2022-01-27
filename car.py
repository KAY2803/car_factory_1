import time
import random
from utils import check_type, check_types
from custom_errors import *
from driver import Driver, Experience


class Car:
    """
    Класс описывающий автомобиль
    """
    brand = None
    _max_speed = 180
    __created_car = 0

    def __init__(self, color, body_type, model_name,
                 engine_type, gear_type, complectation):
        """
        Создаем автомобиль.
        :param color:           цвет автомобиля
        :param body_type:       тип кузова
        :param model_name:      модель
        :param engine_type:     тип двигателя
        :param gear_type:       тип коробки передач
        :param complectation:   комплектация
        """
        self.__model_name = model_name
        self.__body_type = body_type
        self._engine_type = engine_type
        self._gear_type = gear_type
        self.complectation = complectation
        self.color = color

        self.__mileage = 0          # одометр
        self.__count_TO = 1         # счетчик ТО
        self.__const_TO = 25        # пробега с которого начинается предупреждение о необходимости пройти ТО
        self.__status_TO = False    # статус ТО

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
        return self.__driver

    @driver.setter
    def driver(self, driver: Driver):

        if not isinstance(driver, Driver):
            raise DriverTypeError(f"Ожидается {Driver}, получено {type(driver)}")
        self.__driver = driver
        self.__key_owner = True

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
    def start_engine(self):
        return self.__engine_status

    @start_engine.setter
    def start_engine(self, key_owner: bool):
        if self.__key_owner is True:
            self.__engine_status = True
        else:
            print('Нет ключей')

    def __check_driver(self):
        if self.driver is not None:
            return True
        return False

    def alarm_status(self):
        if self.driver is not None and self.__key_owner:
            return True
        return False

    def __ready_status(self):
        if not self.alarm_status():
            raise AlarmOn('Alarm!')
        if not self.__engine_status:
            raise EngineIsNotRunning("двигатель не запущен")
        if not self.__check_driver():
            raise DriverNotFoundError("водитель не найден")
        if not self.__check_technical_inspection():
            raise TechnicInspection(f"без пройденного ТО автомобиль не поедет")

        return True

    def move(self, distance=10):
        try:
            if self.__ready_status():
                part_distance = 0
                for i in range(distance):
                    print(f'Машина проехала {i+1} км.')
                    part_distance += 1
                    self.__traffic_lights(2)
                    time.sleep(0.3)
                    self.__mileage += 1
                    # отработка ТО
                    if self.__mileage > self.__const_TO:
                        print(f" Общий пробег = {self.__mileage}, пройдите ТО {self.__count_TO}")
                        if self.__mileage % 30 == 0:
                            self.__status_TO = True
                            self.__const_TO += self.__mileage
                            raise TechnicInspection(f" ТО {self.__count_TO} НЕ ПРОЙДЕНО!")
                    # конец отработки ТО
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
        except (EngineIsNotRunning, DriverNotFoundError, TechnicInspection, AlarmOn) as e:
            print(f"Машина не может начать движение, т.к. {e}")
    # /Блок отработки технического осмотра

    def __check_technical_inspection(self):
        """
        Проверка статуса технического осмотра
        """
        if self.__status_TO is False:
            return True
        return False

    def _make_technical_inspection(self):
        """
        Проведение технического осмотра
        """
        print(f"TO {self.__count_TO} пройдено")
        self.__count_TO += 1
        self.__status_TO = False

    # Блок светофора
    @staticmethod
    def __traffic_lights(sleep_time):
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
    def _mileage(self):
        return self.__mileage

    @_mileage.setter
    def _mileage(self, mileage):
        if not isinstance(mileage, (int, float)):
            raise TypeError(f"Ожидается {int} или {float}, получено {type(mileage)}")

        self.__mileage = mileage
    # /Блок работы с защищёнными методами


if __name__ == '__main__':

    car = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')
    car_2 = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')

    car.driver = Driver("Иван", Experience((0, 5), (5, 10), (10, 60), 5))
    car.start_engine = "Заведись"
    # car.move()

    # print(car.brand)
    # print(car_2.brand)
    # Car.change_brand("Nissan")
    # print(car.brand)
    # print(car_2.brand)
    #
    # print(car._max_speed)
    # print(car_2._max_speed)
    # Car._change_max_speed(190)
    # print(car._max_speed)
    # print(car_2._max_speed)




    # Блок работы с защищёнными методами
    # print(car._mileage)
    # car._mileage = '10'
    # print(car._mileage)
    # /Блок работы с защищёнными методами

    # Блок отработки движения машины
    # car.start_engine()
    # car.driver = Driver("Иван")

    # car.move()
    # car.move()
    # /Блок отработки движения машины

    # Блок отработки свойств
    # car.driver = Driver('Андрей')
    # print(car.driver)
    # Эквивалент свойствам (property)
    # car.set_driver(Driver('Андрей'))
    # car.get_driver()
    # /Блок отработки свойств


    # Блок проверки отработки ТО
    car.move()
    car.move()
    car.move()
    #car._make_technical_inspection()
    car.move()