import pygame
from queue import PriorityQueue

WIDTH = 500
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path finding algorithm")

RED = (255, 23, 68)
BLUE = (33, 150, 243)
GREEN = (29, 233, 182)
YELLOW = (238, 255, 65)
WHITE = (238, 238, 238)
BLACK = (33, 33, 33)
START = "#76ff03"
PURPLE = (171, 71, 188)
TERQUOISE = (64, 224, 250)
GREY = (176, 190, 197)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_startnode(self):
        return self.color == START

    def is_endnode(self):
        return self.color == YELLOW

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_obstacle(self):
        self.color = BLACK

    def make_endnode(self):
        self.color = YELLOW

    def make_startnode(self):
        self.color = START

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def clear_path(self):
        if not self.is_obstacle() and not self.is_startnode() and not self.is_endnode():
            self.color = WHITE

    def update_neighbour(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2-x1) + abs(y2-y1)


def reconstruct_path(prev_node, current, draw,):
    while current in prev_node:
        current = prev_node[current]
        current.make_path()
        draw()


def method_bidirectional(draw, grid, start, end):
    for row in grid:
        for node in row:
            node.clear_path()
    count = 0
    count1 = 0
    open_set = PriorityQueue()
    open_set1 = PriorityQueue()
    open_set.put((0, count, start))
    open_set1.put((0, count1, end))
    u = {}
    v = {node: float("inf") for row in grid for node in row}
    v[start] = 0
    u1 = {}
    v1 = {node: float("inf") for row in grid for node in row}
    v1[end] = 0

    open_set_hash = {start}
    open_set_hash1 = {end}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        current1 = open_set1.get()[2]
        open_set_hash.remove(current)

        for neighbour in current.neighbors:
            temp_score_v = v[current] + 1

            if temp_score_v < v[neighbour]:
                u[neighbour] = current
                v[neighbour] = temp_score_v

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((v[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        for i in open_set_hash:
            for j in open_set_hash1:
                if i == j:
                    reconstruct_path(u, i, draw)
                    reconstruct_path(u1, j, draw)
                    start.make_startnode()
                    i.make_path()
                    end.make_endnode()
                    return True
        for neighbour1 in current1.neighbors:
            temp_score_v1 = v1[current1] + 1

            if temp_score_v1 < v1[neighbour1]:
                u1[neighbour1] = current1
                v1[neighbour1] = temp_score_v1

                if neighbour1 not in open_set_hash1:
                    count1 += 1
                    open_set1.put((v1[neighbour1], count1, neighbour1))
                    open_set_hash1.add(neighbour1)
                    neighbour1.make_open()

        if current1 != end:
            current1.make_closed()
        draw()
        if current != start:
            current.make_closed()


def method_dijkstra(draw, grid, start, end):
    for row in grid:
        for node in row:
            node.clear_path()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    u = {}
    v = {node: float("inf") for row in grid for node in row}
    v[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(u, end, draw)
            start.make_startnode()
            end.make_endnode()
            return True

        for neighbour in current.neighbors:
            temp_score_v = v[current] + 1

            if temp_score_v < v[neighbour]:
                u[neighbour] = current
                v[neighbour] = temp_score_v

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((v[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()


def method_astar(draw, grid, start, end):
    for row in grid:
        for node in row:
            node.clear_path()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    prev_node = {}
    score_g = {node: float("inf") for row in grid for node in row}
    score_g[start] = 0
    score_f = {node: float("inf") for row in grid for node in row}
    score_f[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(prev_node, end, draw)
            start.make_startnode()
            end.make_endnode()
            return True

        for neighbour in current.neighbors:
            temp_score_g = score_g[current] + 1

            if temp_score_g < score_g[neighbour]:
                prev_node[neighbour] = current
                score_g[neighbour] = temp_score_g
                score_f[neighbour] = temp_score_g + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((score_f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_boundries(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_boundries(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    ROWS = 25
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True
    while run:

        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_startnode()
                elif not end and node != start:
                    end = node
                    end.make_endnode()
                elif node != start and node != end:
                    node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    method_astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    method_bidirectional(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    method_dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and ROWS > 15:
                    pass
                if event.button == 5 and ROWS < 50:
                    pass

    pygame.quit()


if __name__ == '__main__':
    main(window, WIDTH)
