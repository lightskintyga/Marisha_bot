from typing import Union
import random

import my_exception as e


class Buddhist:
    def __init__(self, karma: int = 0):
        self.karma = karma

    def get_karma(self) -> int:
        return self.karma

    def set_karma(self, karma: int):
        self.karma += karma


def one_day(number: int) -> (Union[bool, int]):
    if random.randint(1, 10) == 1:
        raise random.choice([e.KillError('Убийство'),
                             e.DrunkError('Напился'),
                             e.CarCrashError('Разбил машину'),
                             e.GluttonyError('Чревоугодие'),
                             e.DepressionError('Депрессия')])
    else:
        return random.randint(1, 7)


buddhist = Buddhist()
day = 0
while buddhist.get_karma() < 500:
    day += 1
    try:
        result = one_day(day)
        if isinstance(result, bool):
            pass
        else:
            buddhist.set_karma(result)
    except (e.KillError, e.DrunkError, e.CarCrashError, e.GluttonyError, e.DepressionError) as err:
        with open('karma.log', 'a', encoding='utf8') as karma_log:
            error_message = f'{err.__class__.__name__} - {err}'
            karma_log.write(f'День {day}: Проступок: {error_message}\n')
