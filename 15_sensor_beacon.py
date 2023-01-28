from __future__ import annotations

import re


class Sensor:
    SENSORS = dict()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coverage = dict()
        self.closest_beacon = None
        self.distance_to_beacon = 0

    def set_beacon(self, beacon: Beacon):
        self.closest_beacon = beacon
        self.distance_to_beacon = self.calc_manhattan_distance(self.x, self.closest_beacon.x, self.y,
                                                               self.closest_beacon.y)

    def get_coo(self):
        return self.x, self.y

    def get_coverage(self):
        return self.coverage

    def get_coverage_by_y(self, given_y):
        distance = abs(self.y - given_y)
        coverage = (self.distance_to_beacon * 2 + 1) - (2 * distance)
        if coverage > 0:
            half = (coverage - 1) // 2
            range_ = (self.x - half, self.x + half)
            return range_

        return None

    def __generate_full_coverage(self):
        d = self.distance_to_beacon
        max_x = self.x + d
        min_x = d - self.x if d < self.x else self.x - d

        x = min_x
        while x <= max_x:
            y_start = self.y - (d - abs(self.x - x))
            y_end = self.y + (d - abs(self.x - x))
            for y in range(y_start, y_end + 1):
                if self.calc_manhattan_distance(self.x, x, self.y, y) <= d:
                    self.coverage[y] = (x, y)

            x += 1

    def __generate_zone_coverage(self):
        d = self.distance_to_beacon

        for idx, y in enumerate(range(self.y - d, self.y + 1)):
            odd = (idx + 1) * 2 - 1
            half = (odd - 1) // 2
            self.coverage[y] = (self.x - half, self.x + half)

        for idx, y in enumerate(range(self.y + d, self.y, -1)):
            odd = (idx + 1) * 2 - 1
            half = (odd - 1) // 2
            self.coverage[y] = (self.x - half, self.x + half)

    @staticmethod
    def calc_manhattan_distance(x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @classmethod
    def get_all_coverage_by_y(cls, given_y):
        ranges = set()
        for sensor in cls.get_sensors():
            sensor_row_range = sensor.get_coverage_by_y(given_y)
            if sensor_row_range:
                start, end = sensor_row_range
                ranges.add((start, end + 1))

        return ranges

    @classmethod
    def find_sensors_at_y(cls, given_y):
        for sensor in cls.get_sensors():
            if sensor.y == given_y:
                yield sensor

    @classmethod
    def create(cls, coo):
        instance = cls(*coo)
        cls.SENSORS[coo] = instance
        return instance

    @classmethod
    def get_sensor(cls, coo):
        return cls.SENSORS.get(coo)

    @classmethod
    def get_sensors(cls):
        return cls.SENSORS.values()


class Beacon:
    BEACONS = dict()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.detected_by = set()

    def set_detected(self, by_: Sensor):
        if by_ not in self.detected_by:
            self.detected_by.add(by_)

    def get_coo(self):
        return self.x, self.y

    @classmethod
    def find_beacons_at_y(cls, given_y):
        for beacon in cls.get_beacons():
            if beacon.y == given_y:
                yield beacon

    @classmethod
    def create_or_get(cls, coo):
        if coo not in cls.BEACONS:
            instance = cls(*coo)
            cls.BEACONS[coo] = instance
        else:
            instance = cls.BEACONS[coo]

        return instance

    @classmethod
    def get_beacons(cls):
        return cls.BEACONS.values()


COO_BOUND = (0, 4_000_000)
COO_PATT = re.compile(r'at x=(-?\d+), y=(-?\d+)')


def order_ranges(ranges):
    changed = False
    exclude = set()
    ren = len(ranges)
    for i in range(ren):
        if i in exclude: continue
        start, end = ranges[i]
        for j in range(ren):
            if j != i and j not in exclude:
                next_start, next_end = ranges[j]
                if start <= next_start and end >= next_end:
                    exclude.add(j)
                    changed = True
                elif end >= next_start > start:
                    end = next_end
                    ranges[i] = (start, end)
                    exclude.add(j)
                    changed = True

    for idx in sorted(exclude, reverse=True):
        ranges.pop(idx)

    if changed:
        ranges = order_ranges(ranges)

    return ranges


def search_distress_beacon():
    lower, upper = COO_BOUND
    for idx, y in enumerate(range(lower, upper)):
        coverage = Sensor.get_all_coverage_by_y(y)
        ordered = order_ranges(list(coverage))
        print('\r{:.2f}%'.format(idx / upper * 100), end='')

        if len(ordered) > 1:
            x = ordered[0][1]
            if lower <= x <= upper:
                return x, y


if __name__ == '__main__':
    given_y = 2_000_000
    with open('inputs/15_sensor_beacons.txt') as file:
        for line in file:
            sensor_info, beacon_info = line.strip().split(':')
            sensor_coo = tuple(map(int, COO_PATT.search(sensor_info).groups()))
            beacon_coo = tuple(map(int, COO_PATT.search(beacon_info).groups()))

            beacon = Beacon.create_or_get(beacon_coo)
            sensor = Sensor.create(sensor_coo)

            sensor.set_beacon(beacon)
            beacon.set_detected(sensor)

    row_coverage = Sensor.get_all_coverage_by_y(given_y)
    sensors_at_given_y = len(tuple(Sensor.find_sensors_at_y(given_y)))
    beacons_at_given_y = len(tuple(Beacon.find_beacons_at_y(given_y)))

    ordered_ranges = order_ranges(list(row_coverage))

    pos_without_beacon_at_given_y = \
        sum(len(range(start, end)) for start, end in ordered_ranges) \
        - sensors_at_given_y \
        - beacons_at_given_y

    beacon_x, beacon_y = search_distress_beacon()
    tuning_frequency = beacon_x * 4_000_000 + beacon_y

    print(f"\nThe {pos_without_beacon_at_given_y} positions that cannot contain a beacon found.")
    print(f"Tuning frequency for the beacon at ({beacon_x}, {beacon_y}) is {tuning_frequency}")


'''
--- Day 15: Beacon Exclusion Zone ---
You feel the ground rumble again as the distress signal leads you to a large network of subterranean tunnels. 
You don't have time to search them all, but you don't need to: your pack contains a set of deployable sensors that you imagine were originally built to locate lost Elves.
The sensors aren't very powerful, but that's okay; your handheld device indicates that you're close enough to the source of the distress signal to use them. 
You pull the emergency sensor system out of your pack, hit the big button on top, and the sensors zoom off down the tunnels.

Once a sensor finds a spot it thinks will give it a good reading, it attaches itself to a hard surface and begins monitoring for the nearest signal source beacon. 
Sensors and beacons always exist at integer coordinates. Each sensor knows its own position and can determine the position of a beacon precisely; 
however, sensors can only lock on to the one beacon closest to the sensor as measured by the Manhattan distance. 
(There is never a tie where two beacons are the same distance to a sensor.)

It doesn't take long for the sensors to report back their positions and closest beacons (your puzzle input). For example:

Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3

So, consider the sensor at 2,18; the closest beacon to it is at -2,15. For the sensor at 9,16, the closest beacon to it is at 10,16.

Drawing sensors as S and beacons as B, the above arrangement of sensors and beacons looks like this:

               1    1    2    2
     0    5    0    5    0    5
 0 ....S.......................
 1 ......................S.....
 2 ...............S............
 3 ................SB..........
 4 ............................
 5 ............................
 6 ............................
 7 ..........S.......S.........
 8 ............................
 9 ............................
10 ....B.......................
11 ..S.........................
12 ............................
13 ............................
14 ..............S.......S.....
15 B...........................
16 ...........SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This isn't necessarily a comprehensive map of all beacons in the area, though. 
Because each sensor only identifies its closest beacon, if a sensor detects a beacon, you know there are no other beacons that close or closer to that sensor. 
There could still be beacons that just happen to not be the closest beacon to any sensor. Consider the sensor at 8,7:

               1    1    2    2
     0    5    0    5    0    5
-2 ..........#.................
-1 .........###................
 0 ....S...#####...............
 1 .......#######........S.....
 2 ......#########S............
 3 .....###########SB..........
 4 ....#############...........
 5 ...###############..........
 6 ..#################.........
 7 .#########S#######S#........
 8 ..#################.........
 9 ...###############..........
10 ....B############...........
11 ..S..###########............
12 ......#########.............
13 .......#######..............
14 ........#####.S.......S.....
15 B........###................
16 ..........#SB...............
17 ................S..........B
18 ....S.......................
19 ............................
20 ............S......S........
21 ............................
22 .......................B....

This sensor's closest beacon is at 2,10, and so you know there are no beacons that close or closer (in any positions marked #).
None of the detected beacons seem to be producing the distress signal, so you'll need to work out where the distress beacon is 
by working out where it isn't. For now, keep things simple by counting the positions where a beacon cannot possibly be along just a single row.

So, suppose you have an arrangement of beacons and sensors like in the example above and, just in the row where y=10, 
you'd like to count the number of positions a beacon cannot possibly exist. The coverage from all sensors near that row looks like this:

                 1    1    2    2
       0    5    0    5    0    5
 9 ...#########################...
10 ..####B######################..
11 .###S#############.###########.
In this example, in the row where y=10, there are 26 positions where a beacon cannot be present.

Consult the report from the sensors you just deployed. In the row where y=2000000, how many positions cannot contain a beacon?
'''
'''
--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, 
but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, 
which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. 
With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. 
The tuning frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning frequency?
'''