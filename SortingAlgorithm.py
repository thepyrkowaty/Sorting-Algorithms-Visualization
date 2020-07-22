import pygame
import os

GAME_WIDTH = 800
GAME_HEIGHT = 800
os.environ['SDL_VIDEO_CENTERED'] = '1'
GAME_WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualisation")


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


def getClickedPosistion(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def bubbleSort(win, count, grid, rows, width):
    win.fill((255, 255, 255))

    n = len(count)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if count[j] > count[j + 1]:
                count[j], count[j + 1] = count[j + 1], count[j]

        for a in range(rows):
            for b in range(rows):
                grid[a][b].colour = (128, 128, 128)

        for row in range(rows):
            for col in range(count[row]):
                grid[row][rows - col - 1].colour = (0, 0, 128)

        draw(win, grid, rows, width)
    return True


def resetGame(grid, rows):
    for i in range(rows):
        for j in range(rows):
            grid[i][j].colour = (128, 128, 128)
            grid[i][j].calculated = False


def main(win, width):
    ROWS = 100
    count = [0 for i in range(ROWS)]
    grid = makeGrid(ROWS, width)
    running = True
    started = False
    ended = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if not started and not ended:
                draw(win, grid, ROWS, width)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started and not ended:
                    started = True
                    ended = bubbleSort(win, count, grid, ROWS, width)

                if event.key == pygame.K_r and started and ended:
                    resetGame(grid, ROWS)
                    started = False
                    ended = False
                    for i in range(ROWS):
                        count[i] = 0

                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main(GAME_WINDOW, GAME_WIDTH)

