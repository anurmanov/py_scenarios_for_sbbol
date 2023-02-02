from datetime import datetime, timedelta

yargy_date_format = '%Y-%m-%d'
inner_date_format = '%d.%m.%Y'
max_days_in_period = 365


def check_period(d1: datetime, d2: datetime, max_days: int) -> bool:
    """
    Проверка периода на максимальное количество дней в нем,
    на то чтобы не было будущей даты и
    на удаленность периода от текущей даты
    :return: True - если период корректный, False - иначе
    """
    now: datetime = datetime.now()
    delta: timedelta = d2 - d1
    # проверка дней в периоде
    if abs(delta.days) > max_days:
        return False
    # проверка будущих дат
    max_d: datetime = max(d1, d2)
    if max_d > now:
        return False
    # если не период, а просто дата,
    # то проверяем не слишком поздняя ли дата
    if d1 == d2:
        delta: timedelta = now - d1
        if abs(delta.days) > max_days:
            return False

    return True
