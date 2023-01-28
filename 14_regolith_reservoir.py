from math import inf


AIR = '.'
ROCK = '#'
SAND_UNIT = 'o'


def __build_cavemap(paths):
    for path in paths:
        prev_x = prev_y = None
        for x, y in path:
            rel_x = x - min_x
            if prev_x is not None and prev_y is not None:
                x_distance = abs(rel_x - prev_x)
                y_distance = abs(y - prev_y)
                if x_distance:
                    start, end = (rel_x, prev_x) if prev_x > rel_x else (prev_x, rel_x)
                    cavemap[y][start:end + 1] = [ROCK] * (x_distance + 1)
                elif y_distance:
                    start, end = (y, prev_y) if prev_y > y else (prev_y, y)

                    for rel_y in range(start, end + 1):
                        cavemap[rel_y][rel_x] = ROCK

            prev_x = rel_x
            prev_y = y


def __simulate_pouring_sand(cavemap, start):

    def __pour_sand(coo):
        sand_x, sand_y = coo
        pos = cavemap[sand_y][sand_x]
        while pos == AIR:
            sand_y += 1

            if sand_y + 1 >= cavemap_h:
                return None, None

            pos = cavemap[sand_y + 1][sand_x]

        if (sand_x, sand_y) == (700, 0):
            return None, None

        while True:
            if sand_y + 1 >= cavemap_h or (sand_x + 1 >= cavemap_w or sand_x - 1 < 0):
                return None, None

            if cavemap[sand_y + 1][sand_x] == AIR:
                return __pour_sand((sand_x, sand_y))

            diag_left = cavemap[sand_y + 1][sand_x - 1]
            diag_right = cavemap[sand_y + 1][sand_x + 1]
            if diag_left == AIR:
                sand_x -= 1
                sand_y += 1
            elif diag_right == AIR:
                sand_x += 1
                sand_y += 1
            else:
                return sand_x, sand_y

    sand_in_rest = 0
    while True:
        sand_x, sand_y = __pour_sand(start)
        if sand_y is None or sand_x is None:
            break

        sand_in_rest += 1
        cavemap[sand_y][sand_x] = SAND_UNIT

    return sand_in_rest


with open('inputs/14_cave_scan.txt') as file:
    with_floor = False
    max_y = max_x = 0
    min_x = inf
    paths = []
    for line in file:
        path = []
        string_path = line.strip()
        for str_coo in string_path.split(' -> '):
            x, y = map(int, str_coo.split(','))

            max_y = y if y > max_y else max_y

            max_x = x if x > max_x else max_x
            min_x = x if x < min_x else min_x

            path.append((x, y))

        paths.append(path)

    print(max_y, min_x, max_x)
    sand_start_point = (500 - min_x, 0)
    cavemap_w = max_x - min_x + 1
    cavemap_h = max_y + 1
    cavemap = [[AIR for _ in range(cavemap_w)] for _ in range(cavemap_h)]

    __build_cavemap(paths)
    sand_in_rest = __simulate_pouring_sand(cavemap, sand_start_point)
    print(sand_in_rest)
    for row in cavemap:
        print(''.join(row))


'''
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually, hang on - the signal seems like it's coming from the waterfall itself, 
and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here, and the signal definitely leads further inside.
As you begin to make your way deeper underground, you feel the ground rumble for a moment. Sand begins pouring into the cave! 
If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here. 
You scan a two-dimensional vertical slice of the cave above you (your puzzle input) and discover that it is mostly air with structures made of rock.
Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path, 
where x represents distance to the right and y represents distance down. Each path appears as a single line of text in your scan. 
After the first point of each path, each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. 

For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9

This scan means that there are two paths of rock; the first path consists of two straight lines, and the second path consists of three straight lines. 
(Specifically, the first path consists of a line of rock from 498,4 through 498,6 and another line of rock from 498,6 through 496,6.)
The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time, and the next unit of sand is not produced until the previous unit of sand comes to rest. 

A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible. If the tile immediately below is blocked (by rock or sand), 
the unit of sand attempts to instead move diagonally one step down and to the left. 

If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right. 
Sand keeps moving as long as it is able to do so, at each step trying to move down, then down-left, then down-right. 

If all three possible destinations are blocked, the unit of sand comes to rest and no longer moves, 
at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.

After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.

After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.

Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.

Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom, falling into the endless void. 
Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand. How many units of sand come to rest before sand starts flowing into the abyss below?
'''
'''
--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!
You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. 
(This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) 
With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->

To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, 
blocking the source entirely and stopping the flow of sand into the cave. 

In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################

Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
'''