from pico2d import get_canvas_height, get_canvas_width, load_image

import game_framework


FLOCK_Y_RATIOS = (0.12, 0.22, 0.31, 0.40, 0.49,
                  0.58, 0.67, 0.76, 0.84, 0.92)
FLOCK_COUNT = 10
FLOCK_POSITIONS = (
    (120, 185), (520, 225), (940, 275), (1380, 325), (300, 375),
    (760, 420), (1180, 470), (1450, 515), (180, 555), (860, 590),
)
FRAME_WIDTH = 183
FRAME_HEIGHT = 168


class Bird:
    """bird_animation.png의 14개 프레임을 사용해 좌우로 비행하는 새."""

    IMAGE_PATH = 'bird_animation.png'
    FRAME_LAYOUT = (5, 5, 4)
    FRAME_WIDTH = FRAME_WIDTH
    FRAME_HEIGHT = FRAME_HEIGHT
    DRAW_WIDTH = 120
    DRAW_HEIGHT = 110
    FRAME_RATE = 12.0
    HALF_DRAW_WIDTH = DRAW_WIDTH // 2
    TOP_MARGIN = 70
    BOTTOM_MARGIN = 90
    FRAME_RECTS = [
        (column * FRAME_WIDTH, row * FRAME_HEIGHT)
        for row, columns in enumerate(FRAME_LAYOUT)
        for column in range(columns)
    ]
    FRAME_COUNT = len(FRAME_RECTS)
    image = None

    def __init__(self, x, y, speed, frame_offset=0):
        if Bird.image is None:
            Bird.image = load_image(self.IMAGE_PATH)

        self.x = float(x)
        self.y = float(y)
        self.speed = abs(float(speed))
        self.direction = 1 if speed >= 0 else -1
        self.frame = float(frame_offset % self.FRAME_COUNT)

    def update(self):
        dt = game_framework.frame_time
        self.x += self.direction * self.speed * dt
        self._bounce_at_walls()
        self.frame = (self.frame + self.FRAME_RATE * dt) % self.FRAME_COUNT

    def _bounce_at_walls(self):
        """스프라이트 절반 너비를 고려해 벽 통과를 막고 방향을 바꾼다."""
        left = self.HALF_DRAW_WIDTH
        right = get_canvas_width() - self.HALF_DRAW_WIDTH

        if self.x < left:
            self.x = left
            self.direction = 1
        elif self.x > right:
            self.x = right
            self.direction = -1

    def is_facing_right(self):
        return self.direction == 1

    def draw(self):
        frame_x, frame_y = self.FRAME_RECTS[int(self.frame)]
        flip = '' if self.is_facing_right() else 'h'
        Bird.image.clip_composite_draw(
            frame_x,
            frame_y,
            self.FRAME_WIDTH,
            self.FRAME_HEIGHT,
            0,
            flip,
            self.x,
            self.y,
            self.DRAW_WIDTH,
            self.DRAW_HEIGHT,
        )


def create_flock():
    """화면 높이에 맞춰 서로 다른 궤도로 움직이는 10마리를 만든다."""
    if len(FLOCK_POSITIONS) != FLOCK_COUNT or len(FLOCK_Y_RATIOS) != FLOCK_COUNT:
        raise ValueError('새 떼의 위치와 높이 데이터 개수가 다릅니다.')

    canvas_height = get_canvas_height()
    usable_height = max(1, canvas_height - Bird.TOP_MARGIN - Bird.BOTTOM_MARGIN)
    birds = []
    for index, (x, speed) in enumerate(FLOCK_POSITIONS):
        y = Bird.TOP_MARGIN + usable_height * FLOCK_Y_RATIOS[index]
        direction_speed = speed if index % 2 == 0 else -speed
        birds.append(Bird(x, y, direction_speed, index))
    return birds
