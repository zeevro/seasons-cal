import argparse
import sys

from . import write_calendar


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--start-year', type=int, default=1900)
    p.add_argument('-c', '--years', type=int, default=200)
    p.add_argument('-o', '--out-file', default='-')
    p.add_argument('-E', '--no-emoji', action='store_true')
    p.add_argument('-t', '--exact-time', action='store_true')
    args = p.parse_args()

    with open(sys.stdout.fileno() if args.out_file == '-' else args.out_file, 'w', encoding='utf8', newline='\r\n') as f:
        write_calendar(args.start_year, args.years, f, not args.no_emoji, args.exact_time)


if __name__ == '__main__':
    main()
