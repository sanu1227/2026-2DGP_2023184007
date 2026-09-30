"""시트 배치와 재생 경계를 확인하는 간단한 검사."""

import json
import struct

from animation_viewer import ASSET_DIR, frame_at


def main():
    data = json.loads((ASSET_DIR / "samurai_sheet.json").read_text(encoding="utf-8"))
    animations = data["animations"]
    assert [len(frames) for frames in animations.values()] == [10, 8, 8, 6]

    with (ASSET_DIR / "samurai_sheet.png").open("rb") as image:
        header = image.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    assert list(struct.unpack(">II", header[16:24])) == data["sheet_size"]

    sheet_width, sheet_height = data["sheet_size"]
    rectangles = []
    for frames in animations.values():
        for frame in frames:
            x, y, w, h = (frame[key] for key in ("x", "y", "w", "h"))
            assert w > 0 and h > 0
            assert 0 <= x < x + w <= sheet_width
            assert 0 <= y < y + h <= sheet_height
            rectangles.append((x, y, x + w, y + h))
    assert len({(right - left, bottom - top)
                for left, top, right, bottom in rectangles}) > 1
    for index, first in enumerate(rectangles):
        for second in rectangles[index + 1:]:
            assert first[2] <= second[0] or second[2] <= first[0] or \
                   first[3] <= second[1] or second[3] <= first[1]

    assert frame_at(animations, 0) == ("idle", 0)
    assert frame_at(animations, 1.0) == ("idle", 0)
    assert frame_at(animations, 4.9) == ("idle", 9)
    assert frame_at(animations, 5.0) == ("idle", 9)
    assert frame_at(animations, 5.999) == ("idle", 9)
    assert frame_at(animations, 6.0) == ("run", 0)
    assert frame_at(animations, 11.0) == ("attack", 0)
    assert frame_at(animations, 16.0) == ("hurt", 0)
    assert frame_at(animations, 20.0) == ("idle", 0)
    print("시트 배치와 5회 반복/1초 정지 검사 통과")


if __name__ == "__main__":
    main()
