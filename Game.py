
#Muhammad Naufal Ghulam F
#NIM 20230140073
# TAMBAHAN
# 1.Menampilkan Top score dari setiap pemain, jika kalah/menang ( ditunggu sebentar baru muncul)
# 2.Jika Bola Memantul 2 Kali, mengeluarkan tambahan 1 bola di bola yang terpantul
# 3.Membuat Papan Pantulan
# 4.Membuat 10 Balok secara acak, jika pecah  mengeluarkan 5 bola (balok yang memiliki angka 5)



import pygame
import random

# Start the game
pygame.init()

size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brick Breaker Game")

GREEN = (28, 252, 106)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (252, 3, 152)
ORANGE = (252, 170, 28)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Ball class to store position and movement for each ball
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed_x = random.choice([1, -1]) * random.randint(2, 4)  # Random speed between 2 and 4
        self.speed_y = random.choice([1, -1]) * random.randint(2, 4)  # Random speed between 2 and 4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Brick class to add attributes to each brick (such as special and value)
class Brick:
    def __init__(self, x, y, special=False, value=1):
        self.rect = pygame.Rect(x, y, 18, 18)  # The actual rectangle for the brick
        self.special = special  # Whether this brick is special
        self.value = value  # The value or number to display (e.g., 5 for special bricks)

# Function to create a new game state
def create_game():
    floor = pygame.Rect(250, 550, 100, 10)  # Papan pemantul lebih kecil
    ball = Ball(floor.x + floor.width // 2 - 5, floor.y - 10)  # Bola mulai di atas papan
    score = 0
    # Membuat 600 balok kecil
    bricks = [Brick(x * 20, y * 20) for y in range(20) for x in range(30)]
    
    # Menambahkan 10 balok abu-abu sebagai "besi pemantul"
    bumpers = []
    for i in range(10):
        bumper_width = 50
        bumper_height = 10
        x = random.randint(0, 550)
        y = random.randint(100, 390)
        bumpers.append(pygame.Rect(x, y, bumper_width, bumper_height))
    
    balls = [ball]  # Daftar bola
    
    # Menambahkan 6 balok oranye spesial
    special_bricks = random.sample(bricks, 10)  # Pilih 6 balok acak
    for brick in special_bricks:
        brick.special = True  # Tandai balok ini sebagai spesial
        brick.value = 5  # Set nilai untuk balok spesial

    return floor, balls, score, bricks, bumpers, special_bricks

# Function to draw bricks
def draw_brick(bricks):
    for brick in bricks:
        if brick.special:
            pygame.draw.rect(screen, ORANGE, brick.rect)  # Draw orange for special bricks
            font = pygame.font.Font(None, 36)
            text = font.render(str(brick.value), True, WHITE)
            screen.blit(text, (brick.rect.x + 5, brick.rect.y + 2))  # Menambahkan angka "5" pada balok
        else:
            pygame.draw.rect(screen, ORANGE, brick.rect)  # Draw normal orange bricks

# Function to draw bumpers
def draw_bumpers(bumpers):
    for bumper in bumpers:
        pygame.draw.rect(screen, GRAY, bumper)

# Function to display the leaderboard in the bottom-right corner
def display_leaderboard(leaderboard):
    font_title = pygame.font.Font(None, 24)
    font_entry = pygame.font.Font(None, 20)
    max_width = 150
    total_height = len(leaderboard) * 30 + 30
    x_offset = 600 - max_width - 10
    y_offset = 450

    pygame.draw.rect(screen, BLACK, pygame.Rect(x_offset, y_offset - total_height, max_width, total_height))
    title_text = font_title.render("TOP SCORE", 1, WHITE)
    screen.blit(title_text, (x_offset + 5, y_offset - total_height + 5))

    y_offset += 20
    for name, score in leaderboard:
        text = font_entry.render(f"{name}: {score}", 1, WHITE)
        screen.blit(text, (x_offset + 5, y_offset))
        y_offset += 25

    pygame.display.flip()

# Function to load leaderboard from a file
def load_leaderboard():
    leaderboard = []
    try:
        with open("leaderboard.txt", "r") as file:
            for line in file:
                name, score = line.strip().split(":")
                leaderboard.append((name, int(score)))
    except FileNotFoundError:
        pass
    return leaderboard

# Function to save leaderboard to a file
def save_leaderboard(leaderboard):
    with open("leaderboard.txt", "w") as file:
        for name, score in leaderboard:
            file.write(f"{name}:{score}\n")

# Function to handle the game start screen
def ask_for_name():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(200, 250, 200, 40)
    color_inactive = pygame.Color('BLACK')
    color_active = pygame.Color('WHITE')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    # Timer untuk mengatur kedipan garis
    blink = True
    blink_timer = 0
    blink_interval = 500  # Interval dalam milidetik

    while True:
        screen.fill((0, 0, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Atur kedipan garis berdasarkan timer
        blink_timer += clock.get_time()
        if blink_timer >= blink_interval:
            blink = not blink
            blink_timer = 0

        # Gambar teks yang sedang diketik
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        # Gambar kotak input
        pygame.draw.rect(screen, color, input_box, 2)

        # Gambar garis berkedip (cursor)
        if active and blink:
            cursor_x = input_box.x + txt_surface.get_width() + 10
            cursor_y = input_box.y + 5
            pygame.draw.line(screen, color, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Tambahkan teks "Enter your name:"
        font_title = pygame.font.Font(None, 48)
        title_text = font_title.render("Enter your name:", 1, WHITE)
        screen.blit(title_text, (150, 150))

        # Tambahkan teks "Arahkan kursor ke kotak dan klik untuk mengetik"
        font_hint = pygame.font.Font(None, 24)
        hint_text = font_hint.render("Arahkan kursor ke kotak untuk mengetik.", 1, WHITE)
        screen.blit(hint_text, (150, 300))  # Posisi teks di bawah kotak input

        pygame.display.flip()
        clock.tick(30)

# Main game function
def run_game():
    floor, balls, score, bricks, bumpers, special_bricks = create_game()
    bricks_broken = 0
    leaderboard = load_leaderboard()
    player_name = ask_for_name()

    while True:
        continueGame = True
        while continueGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(BLACK)
            pygame.draw.rect(screen, PINK, floor)

            font = pygame.font.Font(None, 24)
            text = font.render("CURRENT SCORE: " + str(score), 1, WHITE)
            screen.blit(text, (10, 570))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and floor.x < 500:
                floor.x += 6
            if keys[pygame.K_LEFT] and floor.x > 0:
                floor.x -= 6

            draw_brick(bricks)  # Draw normal and special bricks
            draw_bumpers(bumpers)

            for ball in balls:
                ball.move()

                if ball.rect.x > 590 or ball.rect.x < 0:
                    ball.speed_x = -ball.speed_x
                if ball.rect.y <= 3:
                    ball.speed_y = -ball.speed_y
                if floor.collidepoint(ball.rect.x, ball.rect.y):
                    ball.speed_y = -ball.speed_y

                for bumper in bumpers:
                    if bumper.collidepoint(ball.rect.x, ball.rect.y):
                        ball.speed_y = -ball.speed_y

                ball.draw()

                hit_bricks = []
                for brick in bricks:
                    if brick.rect.collidepoint(ball.rect.x, ball.rect.y):
                        hit_bricks.append(brick)
                        ball.speed_x = -ball.speed_x
                        ball.speed_y = -ball.speed_y
                        score += brick.value  # Add the value of the brick to the score
                        bricks_broken += 1

                        if brick.special:
                            for _ in range(5):  # Add 5 new balls for special bricks
                                new_ball = Ball(ball.rect.x, ball.rect.y)
                                balls.append(new_ball)

                for brick in hit_bricks:
                    bricks.remove(brick)

            if bricks_broken >= 2:
                new_ball = Ball(balls[0].rect.x, balls[0].rect.y)
                balls.append(new_ball)
                bricks_broken = 0

            balls = [ball for ball in balls if ball.rect.y < 600]

            if not balls:
                font = pygame.font.Font(None, 74)
                text = font.render("YOU LOST!", 1, RED)
                screen.blit(text, (150, 300))
                pygame.display.flip()
                pygame.time.delay(3000)

                leaderboard.append((player_name, score))
                leaderboard.sort(key=lambda x: x[1], reverse=True)
                leaderboard = leaderboard[:5]
                save_leaderboard(leaderboard)

                display_leaderboard(leaderboard)

                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                run_game()
                                waiting_for_restart = False
                break

            # Check if all bricks are destroyed (game won)
            if not bricks:
                font = pygame.font.Font(None, 48)
                text = font.render("YOU WON THE GAME", 1, GREEN)
                text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2))  # Posisikan di tengah layar
                screen.blit(text, text_rect)
                pygame.time.delay(1000)

                # Update leaderboard
                leaderboard.append((player_name, score))
                leaderboard.sort(key=lambda x: x[1], reverse=True)
                leaderboard = leaderboard[:5]
                save_leaderboard(leaderboard)

                # Display leaderboard after winning
                display_leaderboard(leaderboard)

                waiting_for_restart = True
                while waiting_for_restart:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                run_game()
                                waiting_for_restart = False
                break

            pygame.display.flip()
            pygame.time.Clock().tick(60)


run_game()
