#!/usr/bin/env python3

import re
from os.path import basename, splitext
from sys import argv

TIMING_RE = re.compile("(?P<minutes>\d+)(:|\.)(?P<seconds>[0-5]\d)")

class TimingFormatError(Exception):
    pass
    

class Timing():

    def __init__(self, minutes: int=0, seconds: int=0):
        self._minutes = minutes + seconds // 60
        self._seconds = seconds % 60

    @property
    def minutes(self):
        return self._minutes
    
    @property
    def seconds(self):
        return self._seconds

    def __str__(self):
        return f"{self._minutes}:{self._seconds:02}"

    def __repr__(self):
        return f"Timing(minutes={self._minutes}, seconds={self._seconds})"

    def __radd__(self, other):
        """
        >>> Timing(4, 33) + Timing(6, 28)
        Timing(minutes=11, seconds=1)
        """
        if not isinstance(other, Timing):
            raise TypeError(f"{other} is not an instance of Timing")
        return Timing(self.minutes + other.minutes, 
                      self.seconds + other.seconds)
        
    def __add__(self, other):
        return self.__radd__(other)

def parse_timing(timing_string):
    m = TIMING_RE.search(timing_string)
    if m:
        return Timing(minutes=int(m["minutes"]), 
                      seconds=int(m["seconds"]))
    else:
        return None

def parse_timings_string(timings_string):
    timing_strings = timings_string.split()
    for timing_string in timing_strings:
        timing = parse_timing(timing_string)
        if not timing:
            raise TimingFormatError(f"Invalid timing string: {timing_string}")
            break
        else:
            yield timing

def add_timings(timings_string):
    timings = [timing for timing in parse_timings_string(timings_string)]
    return {"timings": timings, "total": sum(timings, start=Timing())}

def main():
    current_file = basename(__file__)
    if len(argv) < 2:
        print(f"Usage: python[3] {current_file} timings")
        return
    timings_string = argv[1]
    result = add_timings(timings_string)

    print()
    for timing in result["timings"]:
        print(f"{str(timing):>7}")
    print("", "=" * 6)
    print(f"{str(result['total']):>7}")

if __name__ == "__main__":
    main()
