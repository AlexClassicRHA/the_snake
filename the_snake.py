from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов, содержит общие атрибуты и методы"""
    
    def __init__(self, position, color):
        """Инициализация позиции и цвета объекта"""
        self.position = position
        self.body_color = color

    def draw(self):
        """Абстрактный метод для отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс для яблока на игровом поле"""
    
    def __init__(self):
        """Инициализация яблока с рандомной позицией и цветом"""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле"""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка яблока на экране"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки, отвечает за логику её движения, роста и отрисовки"""
    
    def __init__(self):
        """Инициализация змейки с начальной позицией и цветом"""
        super().__init__((100, 100), SNAKE_COLOR)  # Инициализация базового класса
        self.length = 1
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]  # Начальная позиция змейки
        self.direction = RIGHT  # Начальное направление
        self.next_direction = RIGHT  # Устанавливаем начальное следующее направление
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки в зависимости от нажатия клавиш"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None  # Сбрасываем после обновления

    def move(self):
        """Обновляет позицию змейки, добавляет новый сегмент и удаляет хвост, если длина не увеличивается"""
        cur = self.positions[0]  # Текущая позиция головы змейки (кортеж из двух чисел)
        x, y = self.direction  # Направление движения (x, y)

        new_head = ((cur[0] + x * GRID_SIZE) % SCREEN_WIDTH, 
                     (cur[1] + y * GRID_SIZE) % SCREEN_HEIGHT)  # Вычисляем новую позицию головы змейки

        if new_head in self.positions:
            self.reset()  # Если змейка столкнулась сама с собой, сбрасываем игру
        else:
            self.positions = [new_head] + self.positions[:self.length]  # Добавляем кортеж в список
            self.last = self.positions[-1]  # Запоминаем последний сегмент (хвост)

    def reset(self):
        """Сброс состояния змейки после столкновения с самой собой"""
        self.length = 1
        self.positions = [(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2))]  # Установка на центр
        self.direction = RIGHT
        self.next_direction = RIGHT  # Устанавливаем следующее направление на первоначальное

    def grow(self):
        """Увеличивает длину змейки после поедания яблока"""
        self.length += 1

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]
    

    def draw(self):
            """Отрисовка всех сегментов змейки"""
            for position in self.positions[:-1]:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, self.body_color, rect)
                pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

            # Затирание последнего сегмента
            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает действия пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    running = True  # Переменная для управления циклом игры
    while running:
        clock.tick(SPEED)
        handle_keys(snake)

        # Обработка событий, таких как закрытие окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Прерываем цикл при закрытии окна

        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        # Очистка экрана и отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

    pygame.quit()  # Закрываем игру корректно после выхода из цикла


if __name__ == '__main__':
    main()
