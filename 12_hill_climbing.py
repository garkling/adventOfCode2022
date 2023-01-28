import math
import sys

START = 'S'
END = 'E'
SPEC_SYM_MAP = {START: 'a', END: 'z'}
MAX_ELEVATION_DIFF = 1
SQUARE_CENTER_OFFSETS = ((-1, 0), (0, -1), (0, 1), (1, 0))


class Vertex:

    def __init__(self, name):
        self.name = name
        self.neighbors = set()
        self.distance = math.inf
        self.visited = False

    def __repr__(self):
        return self.name

    def add_neighbor(self, vertex):
        if vertex not in self.neighbors:
            self.neighbors.add(vertex)

    def get_neighbors(self):
        return self.neighbors

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance

    def set_visited(self):
        self.visited = True

    def is_visited(self):
        return self.visited

    def reset(self):
        self.distance = math.inf
        self.visited = False


class Graph:

    def __init__(self):
        self.start = None
        self.end = None
        self.vertices = dict()

    def add_vertex(self, vertex: Vertex):
        self.vertices[vertex.get_name()] = vertex

    def get_vertex(self, name):
        return self.vertices.get(name)

    def get_vertices(self):
        return self.vertices.values()

    def set_start(self, vertex):
        self.start = vertex
        self.start.set_distance(0)

    def set_end(self, vertex):
        self.end = vertex

    def get_destination_distance(self):
        return self.end.get_distance()

    def reset(self):
        self.start = None
        for vertex in self.get_vertices():
            vertex.reset()

    def find_shortest_paths(self):

        queue = [self.start]
        while len(queue):
            vertex = queue.pop(0)
            vertex.set_visited()

            for neighbor in vertex.get_neighbors():
                if not neighbor.is_visited():
                    new_distance = vertex.get_distance() + 1
                    if new_distance < neighbor.get_distance():
                        neighbor.set_distance(new_distance)
                        queue.append(neighbor)


def build_graph(start_y, start_x):
    __create_vertex(start_y, start_x, heightmap[start_y][start_x])


def __create_vertex(y, x, elevation):
    vertex_name = '{:02}{:02}{}'.format(y, x, elevation)
    existing_vertex = graph.get_vertex(vertex_name)
    if existing_vertex:
        return existing_vertex

    vertex = Vertex(vertex_name)
    graph.add_vertex(vertex)
    for y_offset, x_offset in SQUARE_CENTER_OFFSETS:
        ny, nx = y + y_offset, x + x_offset
        if 0 <= ny < map_h and 0 <= nx < map_w:
            n_elevation = heightmap[ny][nx]
            if __check_elevation_diff(elevation, n_elevation):
                neighbor_vertex = __create_vertex(ny, nx, n_elevation)
                vertex.add_neighbor(neighbor_vertex)

    if elevation == START:
        vertex.set_distance(0)
        graph.set_start(vertex)
    if elevation == END:
        graph.set_end(vertex)

    return vertex


def __check_elevation_diff(source_el, dest_el):
    source_code = ord(SPEC_SYM_MAP.get(source_el, source_el))
    dest_code = ord(SPEC_SYM_MAP.get(dest_el, dest_el))

    return True if source_code > dest_code else dest_code - source_code <= MAX_ELEVATION_DIFF


def __draw_graph():
    draw_map = [['.' for _ in range(map_w)] for _ in range(map_h)]
    for vertex in graph.get_vertices():
        name = vertex.get_name()
        y = int(name[:2])
        x = int(name[2:4])
        char = name[-1]
        draw_map[y][x] = char

    for row in draw_map:
        print(''.join(row))


if __name__ == '__main__':
    graph = Graph()
    heightmap = []
    with open('inputs/12_location_heightmap.txt') as file:
        for line in file:
            row = line.strip()
            heightmap.append(list(row))

    map_h = len(heightmap)
    map_w = len(heightmap[0])
    sys.setrecursionlimit(1000 + map_w * map_h)

    build_graph(0, 0)
    graph.find_shortest_paths()
    shortest_path = graph.get_destination_distance()

    shortest_path_from_elevation_a = math.inf
    lowest_elevation_y = None
    for y, row in enumerate(heightmap):
        elevation = heightmap[y][0]
        vertex_name = '{:02}{:02}{}'.format(y, 0, elevation)
        vertex = graph.get_vertex(vertex_name)

        graph.reset()
        graph.set_start(vertex)
        graph.find_shortest_paths()
        dest_distance = graph.get_destination_distance()
        if dest_distance < shortest_path_from_elevation_a:
            shortest_path_from_elevation_a = dest_distance
            lowest_elevation_y = y

    print(f'The fewest {shortest_path} steps required to get the highest point')
    print(f'The fewest {shortest_path_from_elevation_a} steps required to get the highest point from the lowest elevation at ({lowest_elevation_y}, 0)')


'''
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.
You ask the device for a heightmap of the surrounding area (your puzzle input). 
The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, 
where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). 
Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.
You'd like to reach E, but to save energy, you should do it in as few steps as possible. 
During each step, you can move exactly one square up, down, left, or right. 
To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; 
that is, if your current elevation is m, you could step to elevation n, but not to elevation o. 
(This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. 
You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. 
From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). 
The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
'''
'''
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. 
The beginning isn't very scenic, though; perhaps you can find a better starting point.
To maximize exercise while hiking, the trail should start as low as possible: elevation a. 
The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. 
So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). 
If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^

This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
'''