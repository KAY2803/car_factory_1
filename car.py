"""Модуль, который описывает класс Car."""
import time
import random
from utils import check_type, check_types
from custom_errors import *
from driver import Driver, Mech, GTA, Experience


class Car:
    """Класс, который описывает транспортное средство (ТС)

    ТС может приводиться в движение и останавливаться при наступлении определенных условий
    Переменные экземпляра класса:
    color: цвет ТС
    body_type: тип кузова ТС
    model_name: модель ТС
    engine_type: тип двигателя ТС
    gear_type: тип трансмиссии ТС
    complectation: комплектация ТС

    Открытые методы класса:
    change_brand - метод, который позволяет изменить атрибут класса brand

    """
    brand = None
    _max_speed = 180
    __created_car = 0
    __gas_tank = 50

    def __init__(self, color, body_type, model_name,
                 engine_type, gear_type, complectation):
        """Инициализируем ТС

        :param color: цвет ТС
        :param body_type: тип кузова ТС
        :param model_name: модель ТС
        :param engine_type: тип двигателя ТС
        :param gear_type: тип трансмиссии ТС
        :param complectation: комплектация ТС
        """

        self.__model_name = model_name
        self.__body_type = body_type
        self._engine_type = engine_type
        self._gear_type = gear_type
        self.complectation = complectation
        self.color = color

        self.__mileage = 0

        self.__driver = None
        self.__driver_license = None
        self.__key_owner = False
        self.__mech = None
        self.__engine_status = False
        self.__count_TO = 0
        self.__status_TO = False
        self.__fuel = 0
        self.__mileage = 0          # одометр
        self.__count_TO = 1         # счетчик ТО
        self.__distance_TO = 30        # пробег требующий ТО
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
        """Метод класса, который позволяет изменить марку ТС.
        Принимает аргумент brand. Возвращает значение brand.

        """
        cls.brand = new_brand

    @classmethod
    def _change_max_speed(cls, max_speed):
        """Метод класса, который позволяет изменить максимальную скорость, если введены значения типа int или float.
        Принимает аргумент max_speed. Возвращает значение _max_speed.

        """
        check_type(max_speed, (int, float))

        cls._max_speed = max_speed

    @classmethod
    def __append_new_car_counter(cls):
        """Метод класса, который хранит данные о количестве созданных экземпляров класса Car.
        Возвращает значение __created_car.

        """
        cls.__created_car += 1

    # ==================
    # Статические методы
    # ==================

    @property
    def driver(self):
        """
        Свойство, которое возвращает значение водителя класса Driver
        :return: self.__driver
        """
        return self.__driver

    @driver.setter
    def driver(self, driver: Driver):
        """Свойство, которое присваивает значение атрибуту __driver.
        Принимает аргумент driver класса Driver.
        Если аргумент прошел проверку типа, также присвивает атрибуту __key_owner (ключи от ТС) значение True"""

        check_type(driver, (Driver, GTA))
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
            raise DriverTypeError(
                f'Used to be {type(Mech)}, instead{type(mech)}')
        self.__key_owner = True
        self.__driver = None

    def check_driver_license(self):
        """Метод, который проверяет наличие действующих водительских прав. Если права есть, возвращает True"""
        if self.__driver.license is not None:
            return True
        return False

    @property
    def start_engine(self):
        """Свойство, которое возвращает значение атрибута __engine_status"""
        return self.__engine_status

    @start_engine.setter
    def start_engine(self, key_owner: bool):
        """Свойство, которое присваивает значение атрибуту __engine_status.
        Принимает в качестве аргумента значение атрибута key_owner.
        Возвращает True, если key_owner = True

        """
        if self.__key_owner is True:
            self.__engine_status = True
        else:
            print('Нет ключей')

    def __check_driver(self):
        """Метод, который проверяет наличие водителя. Возвращает True, если водитель есть"""
        if self.driver is not None:
            return True
        return False

    def alarm_status(self):
        """Метод, который проверяет наличие водителя и ключей от ТС. Возвращает True, если есть и водитель и ключи"""
        if self.driver is not None and self.__key_owner:
            return True
        return False

    def __ready_status(self):
        """Метод, который проверяет готовность ТС к движению.
        ТС готово к движению при соблюдении одновременно следующих условий:
        1. есть водитель с действующими водительскими правами
        2. есть ключи от ТС
        3. своевременно пройдено ТО
        4. топлива > 0.1
        Возвращает True, если все вышеперечисленные условия соблюдены

        """
        if not self.alarm_status():
            raise AlarmOn('Alarm!')
        if not self.__engine_status:
            raise EngineIsNotRunning("двигатель не запущен")
        if not self.__check_driver():
            raise DriverNotFoundError("водитель не найден")
        if not self.__check_technical_inspection():
            raise TechnicInspection(f"без пройденного ТО автомобиль не поедет")

        if self.fuel < 0.1:
            raise GasTankEmpty(f"отсутствует топливо")
        if not self.check_driver_license():
            raise InvalidLicense("водительские права недействительны")
        return True

    def move(self, distance=10):
        """Метод, который приводит ТС в движение.

        В качестве аргумента принимает расстояние, которое нужно проехать ТС.
        ТС приводится в движение, при условии ее готовности (если ready_status = True).
        Метод предусматривает кратковременные остановки с последующим продолжением движения в следующих случаях:
        1. красный сигнал светофора
        2. непрерывное время в пути превышает допустимое значение
        Если топлива < 0.1 ТС не поедет

        """
        try:
            if self.__ready_status():

                if distance > self.__driver.get_max_trip_distance():
                    print(f"Дистанция, которую нужно проехать, слишком большая для водителя с таким стажем вождения.\n"
                          f"Водитель проедет максимум {self.__driver.get_max_trip_distance()} км")
                    time.sleep(3)
                    distance = self.__driver.get_max_trip_distance()

                part_distance = 0

                for i in range(distance):
                    print(f'Машина проехала {i+1} км.')
                    part_distance += 1
                    self.__traffic_lights(2)
                    time.sleep(0.3)
                    self.__mileage += 1
                    # отработка ТО
                    if self.__mileage > self.__distance_TO - 5:
                        print(f" Общий пробег = {self.__mileage}, пройдите ТО {self.__count_TO}")
                        if self.__mileage % self.__distance_TO == 0:
                            self.__status_TO = True
                            self.__distance_TO += self.__mileage
                            raise TechnicInspection(f" ТО {self.__count_TO} НЕ ПРОЙДЕНО!")
                    # конец отработки ТО
                    time_driving = part_distance / 60
                    print(f'Непрерывное время в пути {time_driving}')
                    self.fuel -= 0.1
                    if self.fuel <= 0.1:
                        raise GasTankEmpty(f"отсутствует топливо, необходимо заправиться")

                    try:
                        if time_driving >= 0.1:
                            raise MoveStop
                    except MoveStop:
                        print('Требуется принудительная остановка 5 сек.')
                        time.sleep(5)
                        part_distance = 0
                    print('\n\n')

                print(f'Пройден путь в {distance} км '
                      f'c максимальной скоростью {self.__driver.get_max_speed_driver()} км/ч')
        except (EngineIsNotRunning, DriverNotFoundError, AlarmOn) as e:
            print(f"Машина не может начать движение, т.к. {e}")

    # Блок отработки технического обслуживания авто

    # Блок отработки технического осмотра
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

    @property
    def _distance_tech_inspection(self):
        return self.__distance_TO

    @_distance_tech_inspection.setter
    def _distance_tech_inspection(self, distance_tech_ispection):
        """
        Устанавливаем промежуток между техническим осмотром
        :param distance_tech_ispection: расстояние между техническим осмотром
        """
        if not isinstance(distance_tech_ispection, int):
            raise TypeError(f"Ожидается {int}, получено {type(distance_tech_ispection)}")

        self.__distance_TO = distance_tech_ispection

    # Блок светофора

    @staticmethod
    def __traffic_lights(sleep_time):
        """Метод, который описвает светофор на пути движения ТС.

        В качестве аргумента принимает время, в течение которого ТС не будет двигаться, если горит красный сигнал
        светофора.

        """
        rand_bool = random.choice([True, False])  # случайно выбирается состояние светофора
        if rand_bool:
            print(f"Светофор красный, нужно подождать {sleep_time} сек.")
            time.sleep(sleep_time)  # если светофор True красный, то ждем 1 секунду

    # Блок работы с защищёнными методами.
    @property
    def _mileage(self):
        """Свойство, которое возвращает пробег ТС"""
        return self.__mileage

    @_mileage.setter
    def _mileage(self, mileage):
        """Свойство, которое присвает значение атрибуту mileage (пробег ТС).

        Принимает аргумент mileage (пробег ТС) типа int или float.

        """
        check_types(mileage, (int, float))
        self.__mileage = mileage
    # /Блок работы с защищёнными методами

    @property
    def fuel(self):
        """Свойство, которое возвращает объем топлива ТС"""
        return self.__fuel

    @fuel.setter
    def fuel(self, fuel: (int, float)):
        """Свойство, которое присваивает значение атрибуту fuel (объем топлива ТС).

        Принимает аргумент fuel (объем топлива ТС) типа int или float. Значение не может быть отрицательным, а также
        превышать объем топливного бака (атрибут класса gas_tank).

        """
        check_types(fuel, (int, float))
        if 0 > fuel or fuel > self.__gas_tank:
            raise ValueError
        self.__fuel = fuel


if __name__ == '__main__':

    car = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')
    car_2 = Car('черный', 'седан', 'модель', 'бензин', 'автомат', 'люкс')

    experience_ivan = Experience((0, 5), (5, 15), (15, 100), 4)
    car.driver = Driver("Иван", experience_ivan)
    car.driver = GTA("Иван", Experience((0, 5), (5, 10), (10, 60), 5))
    car.start_engine = "Заведись"
    car.fuel = 49
    car.driver.license = 1234567890, 2020, 11, 12
    car.move()

    # Блок проверки отработки ТО
    car.move()
    car.move()
    car.move()
    car._make_technical_inspection()
    car.move()
    car.move()
    car.move()