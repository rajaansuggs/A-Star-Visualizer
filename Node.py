
import pygame
import math
from queue import PriorityQueue
#main arguments take in width and window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
PURPLE = (128, 0 , 128)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
ORANGE = (255, 165, 0)

class Node(object):
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.neighbors = []
        self.color = WHITE
        self.width = width
        self.totalRows = totalRows

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == RED

    def isBarrier(self):
        return self.color == BLACK

    def isOpen(self):
        return self.color == GREEN

    def isStart(self):
        return self.color == ORANGE

    def isEnd(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def startIt(self):
        self.color = ORANGE

    def closeIt(self):
        self.color = RED

    def openIt(self):
        self.color = GREEN

    def endIt(self):
        self.color = TURQUOISE

    def barrierIt(self):
        self.color = BLACK

    def pathIt(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbor(self, grid):
        self.neighbors = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBarrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[0][self.col].isBarrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBarrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False
    '''
    H is the heuristic function that uses the manhattan distance for guessing
    '''
def h(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.pathIt()
		draw()

def algorithm(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))#A priority queue of first the start node w/ f-score of 0
    cameFrom = {}
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[start] = 0
    fScore = {node: float("inf") for row in grid for node in row}
    fScore[start] = h(start.getPos(), end.getPos())

    openSetHash = {start} #allows us to check whether something is in priority queue
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2] #get the start at first
        openSetHash.remove(current)

        if current == end:
            reconstruct_path(cameFrom, end, draw)
            end.endIt()
            return True

        for neighbor in current.neighbors:
            tempGScore = gScore[current] + 1

            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + h(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count+=1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.openIt()
        draw()
        if current != start:
            current.closeIt()
    return False


def createGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def drawGridLines(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    drawGridLines(window, rows, width)
    pygame.display.update()

def getClickedPosition(pos, rows, width):
    gap = width // rows
    y, x = pos
    rows = y // gap
    col = x // gap

    return rows, col

def main(window, width):
    ROWS = 50
    grid = createGrid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:#Left
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.startIt()

                elif not end and node != start:
                    end = node
                    end.endIt()

                elif node != end and node != start:
                    node.barrierIt()

            elif pygame.mouse.get_pressed()[2]: #Right will erase what you place
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosition(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbor(grid)

                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = createGrid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)

