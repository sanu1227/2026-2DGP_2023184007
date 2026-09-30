"""800x600 화면에서 사무라이 애니메이션을 재생한다."""

import json
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
DISPLAY_SCALE = 1.4
FRAME_TIME = 0.1
ANIMATION_ORDER = ("idle", "run")
ASSET_DIR = Path(__file__).resolve().parent


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sheet = load_image(str(ASSET_DIR / "samurai_sheet.png"))
        metadata = json.loads(
            (ASSET_DIR / "samurai_sheet.json").read_text(encoding="utf-8")
        )
        animation_index = 0
        frames = metadata["animations"][ANIMATION_ORDER[animation_index]]
        frame = frames[0]
        sheet_height = metadata["sheet_size"][1]
        anchor_x = frame["source_x"] + frame["w"] / 2
        anchor_y = frame["source_y"] + frame["h"] / 2
        animation_start = get_time()
        running = True
        while running:
            for event in get_events():
                if event.type == SDL_QUIT:
                    running = False
                elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                    running = False
            now = get_time()
            elapsed = now - animation_start
            while elapsed >= len(frames) * FRAME_TIME:
                elapsed -= len(frames) * FRAME_TIME
                animation_index = (animation_index + 1) % len(ANIMATION_ORDER)
                frames = metadata["animations"][ANIMATION_ORDER[animation_index]]
                animation_start = now - elapsed
            frame_index = int(elapsed / FRAME_TIME) % len(frames)
            frame = frames[frame_index]
            clear_canvas()
            draw_x = CANVAS_WIDTH / 2 + (
                frame["source_x"] + frame["w"] / 2 - anchor_x
            ) * DISPLAY_SCALE
            draw_y = CANVAS_HEIGHT / 2 - (
                frame["source_y"] + frame["h"] / 2 - anchor_y
            ) * DISPLAY_SCALE
            sheet.clip_draw(
                frame["x"], sheet_height - frame["y"] - frame["h"],
                frame["w"], frame["h"],
                draw_x, draw_y,
                int(frame["w"] * DISPLAY_SCALE),
                int(frame["h"] * DISPLAY_SCALE),
            )
            update_canvas()
            delay(0.02)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
