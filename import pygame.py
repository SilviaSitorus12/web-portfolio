import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar dan grid
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid untuk puzzle
TILE_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle dengan 4 Gambar Makanan")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Gambar puzzle (gambar yang akan dipotong menjadi tiles)
image_paths = [
    "strawberry.jpg",  # Gambar strawberry
    "banana.jpg",      # Gambar pisang
    "avocado.jpg",     # Gambar alpukat
    "cherry.jpg"       # Gambar cherry
]

# Memuat gambar dan memotongnya menjadi potongan-potongan kecil (tiles)
def load_images(image_paths):
    images = []
    for image_path in image_paths:
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))  # Resize gambar sesuai dengan ukuran layar
        images.append(img)
    return images

# Fungsi untuk memecah gambar menjadi beberapa bagian (tiles)
def split_images(images, grid_size):
    tiles = []
    for image in images:
        for row in range(grid_size):
            for col in range(grid_size):
                tile = image.subsurface(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tiles.append(tile)
    return tiles

# Memuat dan memotong gambar
images = load_images(image_paths)
tiles = split_images(images, GRID_SIZE)

# Membuat puzzle acak
def create_puzzle():
    puzzle = list(range(len(tiles)))
    random.shuffle(puzzle)
    return [puzzle[i:i + GRID_SIZE] for i in range(0, len(puzzle), GRID_SIZE)]

def draw_puzzle(puzzle):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile_index = puzzle[row][col]
            if tile_index != GRID_SIZE * GRID_SIZE - 1:  # Jangan gambar tile terakhir (kosong)
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                screen.blit(tiles[tile_index], (x, y))

# Fungsi untuk mendapatkan posisi gambar kosong
def get_empty_position(puzzle):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if puzzle[row][col] == GRID_SIZE * GRID_SIZE - 1:
                return (row, col)

# Menukar dua tiles dalam puzzle
def swap_tiles(puzzle, pos1, pos2):
    row1, col1 = pos1
    row2, col2 = pos2
    puzzle[row1][col1], puzzle[row2][col2] = puzzle[row2][col2], puzzle[row1][col1]

# Cek apakah puzzle sudah selesai
def is_solved(puzzle):
    return puzzle == [list(range(i, i + GRID_SIZE)) for i in range(0, GRID_SIZE * GRID_SIZE, GRID_SIZE)]

# Game loop
running = True
puzzle = create_puzzle()
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Dapatkan posisi mouse
            x, y = pygame.mouse.get_pos()
            col = x // TILE_SIZE
            row = y // TILE_SIZE
            empty_row, empty_col = get_empty_position(puzzle)

            # Cek apakah tile bisa digeser (bersebelahan dengan tempat kosong)
            if (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row):
                swap_tiles(puzzle, (row, col), (empty_row, empty_col))

    draw_puzzle(puzzle)

    # Cek apakah puzzle sudah selesai
    if is_solved(puzzle):
        font = pygame.font.SysFont(None, 40)
        solved_text = font.render("Puzzle Selesai!", True, BLACK)
        screen.blit(solved_text, (WIDTH // 3, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
