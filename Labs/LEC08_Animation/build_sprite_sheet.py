"""CC0 사무라이 원본에서 과제용 스프라이트 시트를 만든다."""

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile
import json
import sys
from PIL import Image


SOURCE_URL = "https://opengameart.org/sites/default/files/samurai1.zip"
ANIMATIONS = {
    "idle": "Samurai1/01-Idle/__Samurai1_Idle_",
    "run": "Samurai1/02-Run/__Samurai1_Run_",
    "attack": "Samurai1/04-Attack/Attack1/__Samurai1_Attack1_",
    "hurt": "Samurai1/06-Hurt/__Samurai1_Hurt_",
}
SHEET_WIDTH = 2048
PADDING = 8


def read_source():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_bytes()
    request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        return response.read()


def trim_frame(frame):
    bounds = frame.getchannel("A").getbbox()
    if bounds is None:
        raise ValueError("투명한 프레임은 사용할 수 없습니다")
    return frame.crop(bounds), bounds


def place_frames(frames):
    x = y = PADDING
    row_height = 0
    placed = []
    for name, image, bounds in frames:
        if x + image.width + PADDING > SHEET_WIDTH:
            x = PADDING
            y += row_height + PADDING
            row_height = 0
        placed.append((name, image, bounds, x, y))
        x += image.width + PADDING
        row_height = max(row_height, image.height)
    return placed, y + row_height + PADDING


def main():
    selected = []
    with ZipFile(BytesIO(read_source())) as archive:
        for name, prefix in ANIMATIONS.items():
            files = sorted(path for path in archive.namelist()
                           if path.startswith(prefix) and path.endswith(".png"))
            frames = []
            for path in files:
                with Image.open(BytesIO(archive.read(path))) as image:
                    frames.append(image.convert("RGBA"))
            sizes = [trim_frame(frame)[0].size for frame in frames]
            print(f"{name}: {len(frames)}프레임, 원본 크기 {frames[0].size}, "
                  f"잘린 크기 {min(sizes)}~{max(sizes)}")
            for frame in frames:
                image, bounds = trim_frame(frame)
                selected.append((name, image, bounds))
    placed, height = place_frames(selected)
    sheet = Image.new("RGBA", (SHEET_WIDTH, height))
    metadata = {
        "sheet_size": [SHEET_WIDTH, height],
        "source_size": [595, 483],
        "animations": {name: [] for name in ANIMATIONS},
    }
    for name, image, bounds, x, y in placed:
        sheet.paste(image, (x, y))
        metadata["animations"][name].append({
            "x": x, "y": y, "w": image.width, "h": image.height,
            "source_x": bounds[0], "source_y": bounds[1],
        })
    sheet.save(Path(__file__).with_name("samurai_sheet.png"))
    Path(__file__).with_name("samurai_sheet.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"시트 배치: {len(placed)}프레임, {SHEET_WIDTH}x{height}")


if __name__ == "__main__":
    main()
