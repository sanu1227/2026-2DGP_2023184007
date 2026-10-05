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
    source_x, source_y, source_width, source_height = ACTIONS[0][0]
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


def main():
    global sonic

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sonic = load_image(IMAGE_PATH)

    clear_canvas()
    draw_current_frame()
    update_canvas()
    handle_events()
    delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
