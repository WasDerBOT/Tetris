import pygame
import random

pygame.init()

# Colors

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
# Pieces colors
cyan = (1, 237, 250)
green = (83, 218, 63)
yellow = (254, 251, 52)
purple = (221, 10, 178)
red = (234, 20, 28)
navy = (46, 46, 132)
orange = (255, 145, 12)

# Constants
FPS = 60
BlockSize = 40
g = 10  # Falling speed
m = 1  # Moving to the side

# Tetrominos

stick = [
    [[0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],
    [[0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0],
     [0, 0, 1, 0]],
    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 1, 1, 1],
     [0, 0, 0, 0]],
    [[0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0],
     [0, 1, 0, 0]]
]

L = [
    [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 1, 0],
     [0, 1, 1]],
    [[0, 0, 0],
     [1, 1, 1],
     [1, 0, 0]],
    [[1, 1, 0],
     [0, 1, 0],
     [0, 1, 0]]
]
Flipped_L = [
    [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 1],
     [0, 1, 0],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 1],
     [0, 0, 1]],
    [[0, 1, 0],
     [0, 1, 0],
     [1, 1, 0]]
]
Z = [
    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]],
    [[0, 0, 1],
     [0, 1, 1],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 0],
     [1, 1, 0],
     [1, 0, 0]]
]
Flipped_Z = [
    [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 1, 1],
     [0, 0, 1]],
    [[0, 0, 0],
     [0, 1, 1],
     [1, 1, 0]],
    [[1, 0, 0],
     [1, 1, 0],
     [0, 1, 0]]
]
Square = [
    [[1, 1, 0],
     [1, 1, 0],
     [0, 0, 0]],
    [[1, 1, 0],
     [1, 1, 0],
     [0, 0, 0]],
    [[1, 1, 0],
     [1, 1, 0],
     [0, 0, 0]],
    [[1, 1, 0],
     [1, 1, 0],
     [0, 0, 0]],
]
T = [
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]],
    [[0, 1, 0],
     [0, 1, 1],
     [0, 1, 0]],
    [[0, 0, 0],
     [1, 1, 1],
     [0, 1, 0]],
    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 0]]
]
Pieces = [stick, L, Flipped_L, Z, Flipped_Z, Square, T]
ColorMathes = dict()
ColorMathes['stick'] = cyan
ColorMathes['L'] = blue
ColorMathes['Flipped_L'] = purple
ColorMathes['Z'] = yellow
ColorMathes['Flipped_Z'] = orange
ColorMathes['Square'] = green
ColorMathes['T'] = red

# Pygame defines

screen = pygame.display.set_mode((15 * BlockSize, 22 * BlockSize))
pygame.display.set_caption("Tetris")


# Classes
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __neg__(self):
        return Vector(-self.x, -self.y)

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def normalized(self):
        length = self.length
        return Vector(self.x / length, self.y / length)


class Block:
    def __init__(self, color, position, velocity):
        self.color = color
        self.position = position
        self.velocity = velocity

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, 40, 40))
        pygame.draw.rect(screen, (0, 0, 0, 50), (self.position.x, self.position.y, 40, 40), 2)


class Frame:
    def __init__(self, color, position, size):
        self.color = color
        self.position = position
        self.size = size
        self.spawnPosition = Vector(self.size.x / 2 - 2 * BlockSize + self.position.x, self.position.y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.size.x, self.size.y), 2)

    def process(self):
        if ActiveBlocks:
            self.spawnPosition += block.velocity / FPS * g

    def refreshSpawn(self):
        self.spawnPosition = Vector(self.size.x / 2 - 2 * BlockSize + self.position.x, self.position.y)

    def CheckBorderCollision(self, block):
        contactSurface = []
        if block.position.y + block.velocity.y / FPS * g + BlockSize > self.position.y + self.size.y:
            contactSurface.append('bottom')
        if block.position.x + BlockSize >= self.position.x + self.size.x:
            contactSurface.append('right')
        if block.position.x <= self.position.x:
            contactSurface.append('left')

        return contactSurface

    def CheckCollision(self, block, StaticBlocks):
        contactSurface = self.CheckBorderCollision(block)
        for static_block in StaticBlocks:
            if (static_block.position.x == block.position.x and
                    BlockSize > static_block.position.y - block.position.y >= -block.velocity.y / FPS * g):
                contactSurface.append('bottom')
            if block.position.x - static_block.position.x == BlockSize and abs(
                    block.position.y - static_block.position.y) <= BlockSize * 0.99:
                contactSurface.append('left')
            if static_block.position.x - block.position.x == BlockSize and abs(
                    block.position.y - static_block.position.y) <= BlockSize * 0.99:
                contactSurface.append('right')
            if block.position.y - static_block.position.y == BlockSize and abs(
                    block.position.x - static_block.position.x) <= BlockSize * 0.99:
                contactSurface.append('top')

        contactSurface = list(set(contactSurface))
        return contactSurface


ActiveBlocks = []
StaticBlocks = []
CurrentPiece = stick
MovingRight = False
MovingLeft = False
center = False
status = 0


def CheckIntersection(block: Vector, another):
    if another.x < MainFrame.position.x or another.y < MainFrame.position.y:
        return True
    if (another.x + BlockSize > MainFrame.position.x + MainFrame.size.x or
            another.y + BlockSize > MainFrame.position.y + MainFrame.size.y):
        return True
    if block.x < another.x - BlockSize:
        return False
    if block.y < another.y - BlockSize:
        return False
    if block.x > another.x + BlockSize:
        return False
    if block.y > another.y + BlockSize:
        return False
    return True


def CheckSpawnpability(Figure, spawnposition):
    for i in range(len(Figure)):
        for j in range(len(Figure[i])):
            if Figure[i][j] == 1:
                for block in StaticBlocks:
                    if CheckIntersection(block.position, spawnposition + Vector(j * BlockSize, i * BlockSize)):
                        return False

    return True


# Block operations
def SpawnBlocks(Figure, spawnposition):
    color = cyan
    if Figure == stick:
        color = cyan
    elif Figure == L:
        color = orange
    elif Figure == Flipped_L:
        color = blue
    elif Figure == Z:
        color = red
    elif Figure == Flipped_Z:
        color = green
    elif Figure == Square:
        color = yellow
    elif Figure == T:
        color = purple
    Figure = Figure[status]
    for i in range(len(Figure)):
        for j in range(len(Figure[i])):
            if Figure[i][j] == 1:
                ActiveBlocks.append(Block(color, spawnposition + Vector(
                    j * BlockSize,
                    i * BlockSize), Vector(0, BlockSize)))


def MoveLeft():
    for block in ActiveBlocks:
        block.position -= Vector(BlockSize, 0)
    global MovingLeft
    MovingLeft = False
    MainFrame.spawnPosition -= Vector(BlockSize, 0)


def MoveRight():
    for block in ActiveBlocks:
        block.position += Vector(BlockSize, 0)
    global MovingRight
    MovingRight = False
    MainFrame.spawnPosition += Vector(BlockSize, 0)


def RotateRight():
    global status
    if not (CheckSpawnpability(CurrentPiece[(status + 1) % 4], MainFrame.spawnPosition)):
        return
    status += 1
    status = status % 4
    ActiveBlocks.clear()
    SpawnBlocks(CurrentPiece, MainFrame.spawnPosition)


def MoveDown():
    for block in ActiveBlocks:
        block.position += Vector(0, BlockSize)
    global center
    center = False


MainFrame = Frame(black, Vector(BlockSize, BlockSize), Vector(BlockSize * 10, BlockSize * 20))

# Filling screen
screen.fill(white)
pygame.display.flip()
CurrentPiece = random.choice(Pieces)
SpawnBlocks(CurrentPiece, MainFrame.spawnPosition)
MainFrame.draw()
# Main loop
running = True
while running:
    # hotkeys
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and not ActiveBlocks:
                SpawnBlocks(Z, MainFrame.spawnPosition)
            if event.key == pygame.K_w:
                RotateRight()
            if event.key == pygame.K_a:
                MovingLeft = True
            if event.key == pygame.K_d:
                MovingRight = True
            if event.key == pygame.K_r:
                center = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                MovingLeft = False
            if event.key == pygame.K_d:
                MovingRight = False
            if event.key == pygame.K_r:
                center = False
        if event.type == pygame.QUIT:
            running = False

    # Clean screen
    screen.fill((255, 255, 255))

    # Spawn
    if not ActiveBlocks:
        CurrentPiece = random.choice(Pieces)
        if not CheckSpawnpability(CurrentPiece[0], MainFrame.spawnPosition):
            pass
        else:
            SpawnBlocks(CurrentPiece, MainFrame.spawnPosition)
    # Check collision
    for block in ActiveBlocks:
        if 'bottom' in MainFrame.CheckCollision(block,
                                                StaticBlocks):
            for activeblock in ActiveBlocks:
                activeblock.position.y = ((activeblock.position.y + BlockSize / 2) // BlockSize * BlockSize)
                StaticBlocks.append(activeblock)
            status = 0
            ActiveBlocks.clear()
            MainFrame.refreshSpawn()
            break

    # Update
    MainFrame.process()
    for block in ActiveBlocks:
        block.position += block.velocity / FPS * g
    if MovingRight:
        for block in ActiveBlocks:
            if 'right' in MainFrame.CheckCollision(block, StaticBlocks):
                break

        else:
            MoveRight()
    if MovingLeft:
        for block in ActiveBlocks:
            if 'left' in MainFrame.CheckCollision(block, StaticBlocks):
                break
        else:
            MoveLeft()
    # Draw
    for block in ActiveBlocks:
        block.draw()
    for block in StaticBlocks:
        block.draw()

    MainFrame.draw()
    pygame.time.Clock().tick(FPS)
    pygame.display.flip()
pygame.quit()
