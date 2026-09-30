"""CC0 사무라이 원본에서 과제용 스프라이트 시트를 만든다."""

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile
import sys


SOURCE_URL = "https://opengameart.org/sites/default/files/samurai1.zip"
ANIMATIONS = {
    "idle": "Samurai1/01-Idle/__Samurai1_Idle_",
    "run": "Samurai1/02-Run/__Samurai1_Run_",
    "attack": "Samurai1/04-Attack/Attack1/__Samurai1_Attack1_",
    "hurt": "Samurai1/06-Hurt/__Samurai1_Hurt_",
}


def read_source():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_bytes()
    request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request) as response:
        return response.read()


def main():
    with ZipFile(BytesIO(read_source())) as archive:
        for name, prefix in ANIMATIONS.items():
            files = sorted(path for path in archive.namelist()
                           if path.startswith(prefix) and path.endswith(".png"))
            print(f"{name}: {len(files)}프레임")


if __name__ == "__main__":
    main()
