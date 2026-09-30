"""800x600 화면에서 사무라이 애니메이션을 재생한다."""

import json
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
DISPLAY_SCALE = 1.4
ASSET_DIR = Path(__file__).resolve().parent


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sheet = load_image(str(ASSET_DIR / "samurai_sheet.png"))
        metadata = json.loads(
            (ASSET_DIR / "samurai_sheet.json").read_text(encoding="utf-8")
        )
        frame = metadata["animations"]["idle"][0]
        sheet_height = metadata["sheet_size"][1]
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
            clear_canvas()
            sheet.clip_draw(
                frame["x"], sheet_height - frame["y"] - frame["h"],
                frame["w"], frame["h"],
                CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
                int(frame["w"] * DISPLAY_SCALE),
                int(frame["h"] * DISPLAY_SCALE),
            )
            update_canvas()
            delay(0.02)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
