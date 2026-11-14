import pygame
import sys
import random

# ---------- 初始化 ----------
pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打砖块")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)


# ---------- 挡板 ----------
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = (WIDTH - self.width) // 2
        self.y = HEIGHT - 50
        self.speed = 8

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width


# ---------- 球 ----------
class Ball:
    def __init__(self, paddle):
        self.radius = 8
        self.x = paddle.x + paddle.width // 2
        self.y = paddle.y - 10
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

    def update(self, paddle, bricks):
        self.x += self.speed_x
        self.y += self.speed_y

        # 左右墙
        if self.x - self.radius < 0:
            self.x = self.radius
            self.speed_x = abs(self.speed_x)
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.speed_x = -abs(self.speed_x)

        # 上墙
        if self.y - self.radius < 0:
            self.y = self.radius
            self.speed_y = abs(self.speed_y)

        # 挡板碰撞：球在下落、且从上方接触时才反弹
        if (self.speed_y > 0
                and self.y + self.radius >= paddle.y
                and self.y - self.radius <= paddle.y + paddle.height
                and self.x >= paddle.x - self.radius
                and self.x <= paddle.x + paddle.width + self.radius):
            self.y = paddle.y - self.radius
            self.speed_y = -abs(self.speed_y)

        # 砖块碰撞
        for brick in bricks[:]:
            if (self.x + self.radius > brick.x
                    and self.x - self.radius < brick.x + brick.width
                    and self.y + self.radius > brick.y
                    and self.y - self.radius < brick.y + brick.height):
                bricks.remove(brick)
                # 按穿透深度较小的方向判定撞击面，决定反弹轴
                overlap_x = min(self.x + self.radius - brick.x,
                                brick.x + brick.width - (self.x - self.radius))
                overlap_y = min(self.y + self.radius - brick.y,
                                brick.y + brick.height - (self.y - self.radius))
                if overlap_x < overlap_y:
                    self.speed_x = -self.speed_x
                else:
                    self.speed_y = -self.speed_y
                return 10

        return 0


# ---------- 砖块 ----------
class Brick:
    def __init__(self, x, y, width, height, color=GREEN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 1)


def create_bricks(rows=5, cols=8):
    bricks = []
    brick_width = (WIDTH - 40) // cols
    brick_height = 20
    x_offset = 20
    y_offset = 40

    for row in range(rows):
        for col in range(cols):
            x = x_offset + col * brick_width
            y = y_offset + row * brick_height
            color = random.choice([GREEN, YELLOW, GRAY, BLUE])
            bricks.append(Brick(x, y, brick_width, brick_height, color))

    return bricks


# ---------- 游戏结束界面 ----------
def game_over(score):
    screen.fill(GRAY)
    msg = f"Game Over! Your Score: {score}"
    label = font.render(msg, True, BLACK)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(label, rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


# ---------- 主循环 ----------
def main():
    paddle = Paddle()
    ball = Ball(paddle)
    bricks = create_bricks(rows=5, cols=8)
    score = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left()
        if keys[pygame.K_RIGHT]:
            paddle.move_right()

        score += ball.update(paddle, bricks)

        if ball.y - ball.radius > HEIGHT:
            running = False
        if len(bricks) == 0:
            running = False

        screen.fill(BLACK)
        for brick in bricks:
            brick.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)

        text_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text_surface, (10, 10))
        pygame.display.flip()

    game_over(score)


if __name__ == "__main__":
    main()
