import pygame
import sys
import random

# Inicializar o Pygame
pygame.init()

# Configurações da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

# Configurações de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock para controlar o FPS
clock = pygame.time.Clock()

# Classe da cobra
class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]  # Segmentos da cobra
        self.direction = "RIGHT"

    def move(self):
        head = self.body[0]
        if self.direction == "RIGHT":
            new_head = [head[0] + 10, head[1]]
        elif self.direction == "LEFT":
            new_head = [head[0] - 10, head[1]]
        elif self.direction == "UP":
            new_head = [head[0], head[1] - 10]
        elif self.direction == "DOWN":
            new_head = [head[0], head[1] + 10]
        
        self.body.insert(0, new_head)
        self.body.pop()  # Remove o último segmento

    def grow(self):
        # Adiciona um novo segmento ao final da cobra
        self.body.append(self.body[-1])

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], 10, 10))

# Classe da comida
class Food:
    def __init__(self):
        self.position = [random.randrange(1, SCREEN_WIDTH//10) * 10,
                         random.randrange(1, SCREEN_HEIGHT//10) * 10]
        self.color = RED

    def spawn(self):
        self.position = [random.randrange(1, SCREEN_WIDTH//10) * 10,
                         random.randrange(1, SCREEN_HEIGHT//10) * 10]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position[0], self.position[1], 10, 10))

# Função para mostrar a tela inicial
def show_start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render("Snake Game", True, GREEN)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    sub_text = pygame.font.Font(None, 36).render("Pressione qualquer tecla para começar", True, BLACK)
    screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Função para mostrar a tela de Game Over
def show_game_over_screen(score):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over!", True, RED)
    score_text = pygame.font.Font(None, 36).render(f"Pontuação: {score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)

# Função para pausar o jogo
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

# Função principal do jogo
def main():
    # Inicializar objetos
    snake = Snake()
    food = Food()
    obstacles = [[random.randrange(1, SCREEN_WIDTH//10) * 10, random.randrange(1, SCREEN_HEIGHT//10) * 10] for _ in range(5)]
    score = 0

    running = True
    while running:
        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                elif event.key == pygame.K_p:
                    pause_game()

        # Mover a cobra
        snake.move()

        # Verificar colisão com comida
        if snake.body[0] == food.position:
            food.spawn()
            snake.grow()
            score += 1

        # Verificar colisões
        if (snake.body[0][0] < 0 or snake.body[0][0] >= SCREEN_WIDTH or
            snake.body[0][1] < 0 or snake.body[0][1] >= SCREEN_HEIGHT):
            running = False

        if snake.body[0] in snake.body[1:]:
            running = False

        for obstacle in obstacles:
            if snake.body[0] == obstacle:
                running = False

        # Atualizar tela
        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)

        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, pygame.Rect(obstacle[0], obstacle[1], 10, 10))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Pontos: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(15)

    show_game_over_screen(score)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    show_start_screen()
    main()
