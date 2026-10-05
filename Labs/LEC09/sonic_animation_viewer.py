from pico2d import *
from pathlib import Path
from sys import argv


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCALE = 3
FRAME_INTERVAL = 0.08
ACTION_PAUSE = 1.0
RENDER_DELAY = 0.005
GROUND_Y = 230
PLAYING = 0
PAUSE_BETWEEN_ACTIONS = 1
IMAGE_PATH = str(Path(__file__).resolve().with_name('sonic-sprite.png'))
IMAGE_WIDTH = 399
IMAGE_HEIGHT = 525

# (source_x, source_y, width, height), source origin is bottom-left.
ACTIONS = [
    [
        (0, 447, 33, 39),
        (33, 447, 33, 39),
        (66, 447, 33, 39),
        (99, 447, 33, 39),
        (132, 447, 33, 39),
        (165, 447, 33, 39),
        (198, 447, 33, 39),
        (231, 447, 33, 39),
        (264, 447, 33, 39),
        (297, 447, 33, 39),
    ],
    [
        (0, 407, 33, 39),
        (33, 407, 33, 39),
        (66, 407, 33, 39),
        (99, 407, 33, 39),
        (132, 407, 33, 39),
        (165, 407, 33, 39),
        (198, 407, 33, 39),
        (231, 407, 33, 39),
        (264, 407, 33, 39),
        (297, 407, 33, 39),
        (330, 407, 33, 39),
        (363, 407, 33, 39),
    ],
    [
        (0, 361, 38, 43),
        (38, 361, 38, 43),
        (88, 361, 38, 43),
        (129, 361, 38, 43),
        (180, 361, 38, 43),
        (227, 361, 38, 43),
    ],
    [
        (0, 325, 32, 33),
        (34, 325, 32, 33),
        (66, 325, 32, 33),
        (97, 325, 32, 33),
        (130, 325, 32, 33),
        (161, 325, 32, 33),
        (192, 325, 32, 33),
        (229, 325, 32, 33),
        (267, 325, 32, 33),
    ],
    [
        (0, 292, 32, 27),
        (35, 292, 32, 27),
        (69, 292, 32, 27),
        (104, 292, 32, 27),
        (138, 292, 32, 27),
        (173, 292, 32, 27),
    ],
    [
        (0, 251, 32, 36),
        (35, 251, 32, 36),
        (73, 251, 32, 36),
        (110, 251, 32, 36),
        (148, 251, 32, 36),
        (185, 251, 32, 36),
    ],
    [
        (0, 207, 40, 35),
        (35, 207, 40, 35),
        (71, 207, 40, 35),
        (122, 207, 40, 35),
        (171, 207, 40, 35),
        (217, 207, 40, 35),
    ],
    [
        (0, 154, 30, 45),
        (30, 154, 30, 45),
        (60, 154, 30, 45),
        (90, 154, 30, 45),
        (120, 154, 30, 45),
        (150, 154, 30, 45),
        (183, 154, 42, 45),
        (225, 154, 45, 45),
    ],
    [
        (0, 108, 30, 40),
        (30, 108, 34, 40),
        (63, 108, 34, 40),
        (98, 108, 34, 40),
        (135, 108, 34, 40),
        (175, 108, 34, 40),
        (216, 108, 34, 40),
        (253, 108, 34, 40),
    ],
    [
        (0, 56, 42, 43),
        (43, 56, 42, 43),
        (92, 56, 30, 43),
        (122, 56, 30, 43),
    ],
    [
        (0, 8, 65, 45),
        (65, 8, 40, 45),
        (105, 8, 20, 45),
        (125, 8, 30, 45),
        (155, 8, 35, 45),
    ],
]


sonic = None
action_index = 0
frame_index = 0
repeat_count = 0
frame_elapsed = 0.0
pause_elapsed = 0.0
state = PLAYING


def validate_actions():
    assert Path(IMAGE_PATH).is_file()
    assert len(ACTIONS) == 11
    assert SCALE == 3
    assert FRAME_INTERVAL == 0.08
    assert ACTION_PAUSE == 1.0
    assert RENDER_DELAY <= 0.005
    for action in ACTIONS:
        assert action
        for frame in action:
            source_x, source_y, width, height = frame
            assert source_x >= 0
            assert source_y >= 0
            assert width > 0 and height > 0
            assert source_x + width <= IMAGE_WIDTH
            assert source_y + height <= IMAGE_HEIGHT


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def draw_current_frame():
    source_x, source_y, source_width, source_height = ACTIONS[action_index][frame_index]
    draw_width = source_width * SCALE
    draw_height = source_height * SCALE
    draw_x = max(draw_width // 2, min(WINDOW_WIDTH - draw_width // 2, WINDOW_WIDTH // 2))
    draw_y = max(draw_height // 2, min(WINDOW_HEIGHT - draw_height // 2, GROUND_Y + draw_height // 2))
    sonic.clip_draw(
        source_x,
        source_y,
        source_width,
        source_height,
        draw_x,
        draw_y,
        draw_width,
        draw_height,
    )


def update_animation(delta_time):
    global action_index, frame_index, frame_elapsed, repeat_count
    global pause_elapsed, state

    if state == PAUSE_BETWEEN_ACTIONS:
        pause_elapsed += delta_time
        if pause_elapsed >= ACTION_PAUSE:
            pause_elapsed = 0.0
            action_index += 1
            if action_index >= len(ACTIONS):
                action_index = 0
            frame_index = 0
            frame_elapsed = 0.0
            state = PLAYING
        return

    frame_elapsed += delta_time
    while state == PLAYING and frame_elapsed >= FRAME_INTERVAL:
        frame_elapsed -= FRAME_INTERVAL
        frame_index += 1
        if frame_index >= len(ACTIONS[action_index]):
            repeat_count += 1
            if repeat_count >= 5:
                repeat_count = 0
                frame_index = len(ACTIONS[action_index]) - 1
                state = PAUSE_BETWEEN_ACTIONS
            else:
                frame_index = 0


def main():
    global sonic

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        try:
            sonic = load_image(IMAGE_PATH)
        except Exception as error:
            print(f'이미지 로드 실패: {error}')
            return

        running = True
        previous_time = get_time()
        while running:
            running = handle_events()
            current_time = get_time()
            update_animation(current_time - previous_time)
            previous_time = current_time

            clear_canvas()
            draw_current_frame()
            update_canvas()
            delay(RENDER_DELAY)
    finally:
        close_canvas()


if __name__ == '__main__':
    if '--self-check' in argv:
        validate_actions()
        print('ACTIONS self-check passed')
    else:
        main()
