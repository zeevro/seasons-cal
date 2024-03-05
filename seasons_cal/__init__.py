import datetime
from typing import TextIO

import ephem


EVENTS = [
    ('Spring Equinox', '🌱', ephem.next_vernal_equinox),
    ('Summer Solstice', '☀️', ephem.next_summer_solstice),
    ('Autumn Equinox', '🍂', ephem.next_autumnal_equinox),
    ('Winter Solstice', '❄️', ephem.next_winter_solstice),
]

_SPACE = ' '
_MINUS = '-'


def dt_date(dt: datetime.datetime) -> str:
    return f';VALUE=DATE:{dt:%Y%m%d}'


def dt_datetime(dt: datetime.datetime) -> str:
    return f':{dt:%Y%m%dT%H%M%SZ}'


def write_calendar(first_year: int, years: int, file: TextIO, add_emoji: bool = True, exact_time: bool = False) -> None:
    print('BEGIN:VCALENDAR', file=file)
    print('VERSION:2.0', file=file)
    print('PRODID:Seasons iCal Generator', file=file)

    dt_func = dt_datetime if exact_time else dt_date
    title_func = (lambda title, emoji: f'{emoji} {title}') if add_emoji else (lambda title, _emoji: title)
    dtstamp = dt_datetime(datetime.datetime.now(datetime.timezone.utc))

    for year in map(str, range(first_year, first_year + years)):
        for title, emoji, func in EVENTS:
            print('BEGIN:VEVENT', file=file)
            print(f'UID:{title.lower().replace(_SPACE, _MINUS)}-{year}@seasons-cal', file=file)
            print(f'DTSTAMP{dtstamp}', file=file)
            print(f'DTSTART{dt_func(func(year).datetime())}', file=file)
            print(f'SUMMARY:{title_func(title, emoji)}', file=file)
            print('TRANSP:TRANSPARENT', file=file)
            print('END:VEVENT', file=file)

    print('END:VCALENDAR', file=file)
