from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCALE = 3
FRAME_INTERVAL = 0.1
ACTION_PAUSE = 1.0
IMAGE_PATH = 'sonic-sprite.png'
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


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def draw_current_frame():
    source_x, source_y, source_width, source_height = ACTIONS[action_index][frame_index]
    sonic.clip_draw(
        source_x,
        source_y,
        source_width,
        source_height,
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        source_width * SCALE,
        source_height * SCALE,
    )


def update_animation(delta_time):
    global frame_index, frame_elapsed

    frame_elapsed += delta_time
    if frame_elapsed >= FRAME_INTERVAL:
        frame_elapsed -= FRAME_INTERVAL
        frame_index += 1
        if frame_index >= len(ACTIONS[action_index]):
            frame_index = 0


def main():
    global sonic

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sonic = load_image(IMAGE_PATH)

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
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
