import pygame
import os

GAME_WIDTH = 800
GAME_HEIGHT = 800
os.environ['SDL_VIDEO_CENTERED'] = '1'
GAME_WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualisation")
pygame.init()


class Tile:

    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.width = width
        self.totalRows = totalRows
        self.x = row * width
        self.y = col * width
        self.colour = (128, 128, 128)
        self.calculated = False

    def getPos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))


def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i, j, gap, width)
            grid[i].append(tile)
    return grid


def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (0, 0, 0), (0, i * gap), (width, i * gap))
        pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill((255, 255, 255))

    for row in grid:
        for tile in row:
            tile.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()


def prepareToDraw(listToSort, grid, rows):
    for a in range(rows):
        for b in range(rows):
            grid[a][b].colour = (128, 128, 128)

    for row in range(rows):
        for col in range(listToSort[row]):
            grid[row][rows - col - 1].colour = (0, 0, 128)


def getClickedPosistion(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def resetGame(grid, rows):
    for i in range(rows):
        for j in range(rows):
            grid[i][j].colour = (128, 128, 128)
            grid[i][j].calculated = False


def bubbleSort(listToSort, win, grid, rows, width):
    n = len(listToSort)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if listToSort[j] > listToSort[j + 1]:
                listToSort[j], listToSort[j + 1] = listToSort[j + 1], listToSort[j]

        prepareToDraw(listToSort, grid, rows)
        draw(win, grid, rows, width)
    return True


def insertionSort(listToSort, win, grid, rows, width):
    for i in range(1, len(listToSort)):
        j = i - 1
        nextElement = listToSort[i]
        while (listToSort[j] > nextElement) and (j >= 0):
            listToSort[j + 1] = listToSort[j]
            j = j - 1
        listToSort[j + 1] = nextElement

        prepareToDraw(listToSort, grid, rows)
        draw(win, grid, rows, width)
    return True


def partitionForQuickSort(listToSort, first, last, win, grid, rows, width):
    i = first - 1
    pivot = listToSort[last]

    for j in range(first, last):
        if listToSort[j] < pivot:
            i = i + 1
            listToSort[i], listToSort[j] = listToSort[j], listToSort[i]

    listToSort[i + 1], listToSort[last] = listToSort[last], listToSort[i + 1]
    prepareToDraw(listToSort, grid, rows)
    draw(win, grid, rows, width)

    return i + 1


def quickSort(listToSort, first, last, win, grid, rows, width):
    if first < last:
        pi = partitionForQuickSort(listToSort, first, last, win, grid, rows, width)
        quickSort(listToSort, first, pi - 1, win, grid, rows, width)
        quickSort(listToSort, pi + 1, last, win, grid, rows, width)

    return True


def cocktailSort(listToSort, win, grid, rows, width):
    n = len(listToSort)
    swapped = True
    start = 0
    end = n - 1
    while swapped:
        swapped = False

        for i in range(start, end):
            if listToSort[i] > listToSort[i + 1]:
                listToSort[i], listToSort[i + 1] = listToSort[i + 1], listToSort[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end -= 1

        for i in range(end - 1, start - 1, -1):
            if listToSort[i] > listToSort[i + 1]:
                listToSort[i], listToSort[i + 1] = listToSort[i + 1], listToSort[i]
                swapped = True
        start += 1

        prepareToDraw(listToSort, grid, rows)
        draw(win, grid, rows, width)

    return True


def countingSort(listToSort, expo, win, grid, rows, width):
    n = len(listToSort)
    output = [0] * n
    count = [0] * 10

    for i in range(0, n):
        index = (listToSort[i] // expo)
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (listToSort[i] // expo)
        output[count[index % 10] - 1] = listToSort[i]
        count[index % 10] -= 1
        i -= 1

    i = 0
    for i in range(0, len(listToSort)):
        listToSort[i] = output[i]

        prepareToDraw(listToSort, grid, rows)
        draw(win, grid, rows, width)


def radixSort(listToSort, win, grid, rows, width):
    max1 = max(listToSort)

    expo = 1
    while max1 // expo > 0:

        countingSort(listToSort, expo, win, grid, rows, width)
        expo *= 10

    return True


def main(win, width):
    ROWS = 100
    count = [0 for i in range(ROWS)]
    grid = makeGrid(ROWS, width)
    running = True
    started = False
    ended = False
    draw(win, grid, ROWS, width)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if pygame.mouse.get_pressed()[0] and not started:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosistion(pos, ROWS, width)
                (grid[row][col]).colour = (0, 0, 0)

                for i in range(col, ROWS, 1):
                    (grid[row][i]).colour = (0, 0, 0)

                for i in range(ROWS):
                    for j in range(ROWS):
                        if grid[j][i].colour == (0, 0, 0) and grid[i][j].calculated is False:
                            grid[i][j].calculated = True
                            count[j] += 1
                draw(win, grid, ROWS, width)

            elif pygame.mouse.get_pressed()[2] and not started:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = getClickedPosistion(pos, ROWS, width)
                (grid[row][col]).colour = (128, 128, 128)

                for i in range(0, ROWS, 1):
                    (grid[row][i]).colour = (128, 128, 128)

                for i in range(ROWS):
                    for j in range(ROWS):
                        if grid[j][i].colour == (128, 128, 128) and grid[i][j].calculated is True:
                            grid[i][j].calculated = False
                            count[j] -= 1
                draw(win, grid, ROWS, width)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and not started and not ended:
                    started = True
                    ended = bubbleSort(count, win, grid, ROWS, width)

                elif event.key == pygame.K_2 and not started and not ended:
                    started = True
                    ended = insertionSort(count, win, grid, ROWS, width)

                elif event.key == pygame.K_3 and not started and not ended:
                    started = True
                    ended = quickSort(count, 0, len(count) - 1, win, grid, ROWS, width)

                elif event.key == pygame.K_4 and not started and not ended:
                    started = True
                    ended = cocktailSort(count, win, grid, ROWS, width)

                elif event.key == pygame.K_5 and not started and not ended:
                    started = True
                    ended = radixSort(count, win, grid, ROWS, width)

                if event.key == pygame.K_r:
                    resetGame(grid, ROWS)
                    started = False
                    ended = False
                    for i in range(ROWS):
                        count[i] = 0
                    draw(win, grid, ROWS, width)

                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main(GAME_WINDOW, GAME_WIDTH)