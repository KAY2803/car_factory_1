from typing import Any


def check_type(value: Any, types: Any):
    if not isinstance(value, types):
        raise TypeError(f"Ожидается {types}, получено {type(value)}")


def check_types(values: Any, types_: tuple):
    # подумать если хотим проверить что прилетел кортеж
    # не элементы внутри кортежа, а сам кортеж

    if not isinstance(values, tuple):
        values = (values,)

    for elem in values:
        check_type(elem, types_)


if __name__ == '__main__':
    a = 10
    b = 10
    tup = (a, b)
    check_types(tup)

