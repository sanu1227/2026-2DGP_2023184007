from pico2d import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
IMAGE_PATH = 'sonic-sprite.png'


sonic = None


def main():
    global sonic

    open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    sonic = load_image(IMAGE_PATH)
    close_canvas()


if __name__ == '__main__':
    main()
