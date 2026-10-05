from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
IMAGE_PATH = 'sonic-sprite.png'


sonic = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def main():
    global sonic

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sonic = load_image(IMAGE_PATH)

    running = handle_events()
    if running:
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
