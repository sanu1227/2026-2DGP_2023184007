"""800x600 화면에서 사무라이 애니메이션을 재생한다."""

import json
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
DISPLAY_SCALE = 1.4
FRAME_TIME = 0.1
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0
ANIMATION_ORDER = ("idle", "run", "attack", "hurt")
ASSET_DIR = Path(__file__).resolve().parent


def frame_at(animations, elapsed):
    total = sum(len(animations[name]) * FRAME_TIME * REPEAT_COUNT + PAUSE_SECONDS
                for name in ANIMATION_ORDER)
    elapsed %= total
    for name in ANIMATION_ORDER:
        frames = animations[name]
        play_time = len(frames) * FRAME_TIME * REPEAT_COUNT
        if elapsed < play_time + PAUSE_SECONDS:
            if elapsed >= play_time:
                return name, len(frames) - 1
            return name, int((elapsed + 1e-9) / FRAME_TIME) % len(frames)
        elapsed -= play_time + PAUSE_SECONDS


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sheet = load_image(str(ASSET_DIR / "samurai_sheet.png"))
        metadata = json.loads(
            (ASSET_DIR / "samurai_sheet.json").read_text(encoding="utf-8")
        )
        frame = metadata["animations"][ANIMATION_ORDER[0]][0]
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
            animation_name, frame_index = frame_at(
                metadata["animations"], get_time() - animation_start
            )
            frame = metadata["animations"][animation_name][frame_index]
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
