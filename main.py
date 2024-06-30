import pygame

pygame.init()




# Colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Constants
FPS = 60
BlockSize = 40
g = 10  # Falling speed

# Tetrominos

stick = [
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

L = [
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
Flipped_L = [
    [1, 0, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
Z = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
Flipped_Z = [
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
Square = [
    [1, 1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
T = [
    [0, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Pygame defines

screen = pygame.display.set_mode((12 * BlockSize, 22 * BlockSize))
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
        pygame.draw.rect(screen, black, (self.position.x, self.position.y, 40, 40), 4)


class Frame:
    def __init__(self, color, position, size):
        self.color = color
        self.position = position
        self.size = size

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position.x, self.position.y, self.size.x, self.size.y), 2)

    def CheckBorderCollision(self, block):
        if block.position.y + block.velocity.y / FPS * g + BlockSize > self.position.y + self.size.y:
            return True
        return False

    def CheckBlockCollision(self, block, StaticBlocks):
        for static_block in StaticBlocks:
            if static_block.position.x == block.position.x and static_block.position.y - block.position.y <= BlockSize:
                return True
        return False


ActiveBlocks = []
StaticBlocks = []


def SpawnBlocks(Figure, MainFrame=Frame(black, Vector(BlockSize, BlockSize), Vector(BlockSize * 10, BlockSize * 20))):
    for i in range(len(Figure)):
        for j in range(len(Figure[i])):
            if Figure[i][j] == 1:
                ActiveBlocks.append(Block(blue, Vector(
                    MainFrame.size.x / 2 - 2 * BlockSize + MainFrame.position.x + j * BlockSize,
                    MainFrame.position.y + i * BlockSize), Vector(0, BlockSize)))


MainFrame = Frame(black, Vector(BlockSize, BlockSize), Vector(BlockSize * 10, BlockSize * 20))

# Filling screen
screen.fill((255, 255, 255))
pygame.display.flip()
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                SpawnBlocks(Flipped_L)
        if event.type == pygame.QUIT:
            running = False

    # Clean screen
    screen.fill((255, 255, 255))

    # Update
    for block in ActiveBlocks:
        block.position += block.velocity / FPS * g
    # Check collision
    for block in ActiveBlocks:
        if MainFrame.CheckBorderCollision(block) or MainFrame.CheckBlockCollision(block,
                                                                                  StaticBlocks):
            for activeblock in ActiveBlocks:
                StaticBlocks.append(activeblock)
            ActiveBlocks.clear()
            break
    # Draw
    for block in ActiveBlocks:
        block.draw()
    for block in StaticBlocks:
        block.draw()

    # Draw
    MainFrame.draw()
    pygame.time.Clock().tick(FPS)
    pygame.display.flip()
pygame.quit()
