from datetime import datetime, timezone
from difflib import unified_diff
from io import StringIO
from textwrap import dedent

from seasons_cal import dt_datetime, write_calendar


def _t(s: str) -> str:
    return dedent(s).lstrip().replace('\r\n', '\n').replace('\n', '\r\n')


EXPECTED_RESULTS = {
    (False, False): _t(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:Seasons iCal Generator
        BEGIN:VEVENT
        UID:spring-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240320
        SUMMARY:Spring Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:summer-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240620
        SUMMARY:Summer Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:autumn-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240922
        SUMMARY:Autumn Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:winter-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20241221
        SUMMARY:Winter Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        END:VCALENDAR
    """
    ),
    (False, True): _t(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:Seasons iCal Generator
        BEGIN:VEVENT
        UID:spring-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240320T030622Z
        SUMMARY:Spring Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:summer-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240620T205103Z
        SUMMARY:Summer Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:autumn-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240922T124332Z
        SUMMARY:Autumn Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:winter-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20241221T092020Z
        SUMMARY:Winter Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        END:VCALENDAR
    """
    ),
    (True, False): _t(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:Seasons iCal Generator
        BEGIN:VEVENT
        UID:spring-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240320
        SUMMARY:🌱 Spring Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:summer-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240620
        SUMMARY:☀️ Summer Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:autumn-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20240922
        SUMMARY:🍂 Autumn Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:winter-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART;VALUE=DATE:20241221
        SUMMARY:❄️ Winter Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        END:VCALENDAR
    """
    ),
    (True, True): _t(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:Seasons iCal Generator
        BEGIN:VEVENT
        UID:spring-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240320T030622Z
        SUMMARY:🌱 Spring Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:summer-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240620T205103Z
        SUMMARY:☀️ Summer Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:autumn-equinox-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20240922T124332Z
        SUMMARY:🍂 Autumn Equinox
        TRANSP:TRANSPARENT
        END:VEVENT
        BEGIN:VEVENT
        UID:winter-solstice-2024@seasons-cal
        DTSTAMP:%DTSTAMP%
        DTSTART:20241221T092020Z
        SUMMARY:❄️ Winter Solstice
        TRANSP:TRANSPARENT
        END:VEVENT
        END:VCALENDAR
    """
    ),
}


def main() -> None:
    failed = 0
    for (add_emoji, exact_time), expected_raw in EXPECTED_RESULTS.items():
        print(f'Test for {add_emoji=} & {exact_time=} ', end='')

        f = StringIO(newline='\r\n')
        write_calendar(2024, 1, f, add_emoji, exact_time)

        expected = expected_raw.replace(':%DTSTAMP%', dt_datetime(datetime.now(timezone.utc)))
        actual = f.getvalue()

        if expected != actual:
            print('failed!')
            print(''.join(unified_diff(expected.splitlines(keepends=True), actual.splitlines(keepends=True), 'expected', 'actual')))
            failed += 1
        else:
            print('passed.')

    if failed:
        raise SystemExit(f'{failed} test(s) failed!')

    print('All tests passed OK.')


if __name__ == '__main__':
    main()
