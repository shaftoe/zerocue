from datetime import timedelta
from sys import stdout, stderr
from typing import Union, BinaryIO
import argparse
import re

DEBUG = False


def print_debug(message):
    if DEBUG:
        print(message, file=stderr, end="")


class CueError(Exception):
    pass


class CueTime:
    # https://en.wikipedia.org/wiki/Cue_sheet_(computing)
    # There are 75 frames per second of audio
    FRAMES_PER_SECOND = 75

    __slots__ = "minute", "second", "frame", "delta"

    def __init__(self, minute: Union[str, int], second: Union[str, int], frame: Union[str, int]):
        try:
            self.minute = int(minute)
            self.second = int(second)
            self.frame = int(frame)
            self.delta = timedelta(minutes=self.minute, seconds=self.second)

            assert self.minute >= 0
            assert 0 <= self.second < 60
            assert 0 <= self.frame < self.FRAMES_PER_SECOND

        except (AssertionError, TypeError, ValueError):
            print(f"\nFATAL: '{minute}:{second}:{frame}' is not a valid CUE TIMESTAMP, aborting",
                  file=stderr)
            raise CueError

        print_debug(" => %s\n" % self)

    def __str__(self) -> str:
        return "{:02}:{:02}:{:02}".format(self.minute, self.second, self.frame)

    def __sub__(self, other):
        result_frame = self.frame - other.frame

        if result_frame >= 0:
            result_delta = self.delta - other.delta
        else:
            result_delta = self.delta - other.delta - timedelta(seconds=1)

        minutes, seconds = divmod(result_delta.seconds, 60)

        return CueTime(minute=minutes,
                       second=seconds,
                       frame=result_frame % self.FRAMES_PER_SECOND)

    def __eq__(self, other):
        return self.delta == other.delta and self.frame == other.frame


def create_new_cue(cue_file: BinaryIO, outfile: BinaryIO) -> None:
    """Parse CUE sheet file line by line and produce new CUE sheet output."""
    delay = None

    for num, line in enumerate(cue_file.readlines()):
        try:
            decoded_line = str(line, encoding="utf-8")

        except Exception as CueError:  # pylint: disable=broad-except
            print_debug("CueError decoding line #%d: %s\n" % (num, CueError))
            outfile.write(line)
            continue

        match = re.search(r"INDEX \d+ (.*)", decoded_line)
        if match:
            print_debug("Parsing line #{:03}: '{}'".format(num, decoded_line.rstrip().lstrip(" ")))
            time_str = match.groups(1)[0]
            index = decoded_line.index(match.groups(1)[0])

            cue = CueTime(*time_str.split(":"))

            if delay is None:
                # First track, we store the time delta
                delay = cue
                print_debug(f"Setting timedelta delay: {delay}\n")

            print_debug("New cue time")
            line = bytes(f"{decoded_line[0:index]}{cue - delay}\n", encoding="utf-8")

        outfile.write(line)
        outfile.flush()


def main():
    parser = argparse.ArgumentParser(
        description="remove first INDEX track time from every "
                    "following INDEXes in a CUE sheet file")
    parser.add_argument("cuefile", help="source CUE file (e.g playlist.cue)")
    parser.add_argument("-v", "--verbose", help="send informative logs to STDERR",
                        action="store_true")
    parser.add_argument("-o", "--output", help="write to OUTPUT file instead of STDOUT")
    args = parser.parse_args()

    global DEBUG
    DEBUG = args.verbose

    if args.output:
        output = open(args.output, "wb")
        print_debug(f"Writing new CUE file to {args.output}\n")
    else:
        output = stdout.buffer
        print_debug("Printing new CUE file content to STDOUT\n")

    try:
        with open(args.cuefile, "rb") as cuefile:
            create_new_cue(cuefile, output)
    except CueError:
        if args.output:
            output.close()
        raise SystemExit(1)

    if args.output:
        print_debug(f"New CUE file {args.output} ready\n")
        output.close()


if __name__ == "__main__":
    main()
