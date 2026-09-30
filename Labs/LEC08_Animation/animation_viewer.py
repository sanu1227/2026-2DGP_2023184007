"""800x600 화면에서 사무라이 애니메이션을 재생한다."""

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
            clear_canvas()
            update_canvas()
            delay(0.02)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
