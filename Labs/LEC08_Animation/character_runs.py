from pico2d import *

open_canvas()

grass = load_image('grass.png')
boy = load_image('animation_sheet.png')

# fill here
while (True):
    frame = 0

    for x in range(750, 50, -5):
        clear_canvas()
        grass.draw(400, 30)
        boy.clip_draw(
            100 * frame, 0,
            100, 100,
            x, 90,
            100, 100
        )
        update_canvas()

        frame = (frame + 1) % 8
        delay(0.05)

    frame = 0

    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        boy.clip_draw(
            100 * frame, 100,
            100, 100,
            x, 90,
            100, 100
        )
        update_canvas()

        frame = (frame + 1) % 8
        delay(0.05)

    frame = 0

    for x in range(750, 50, -5):
        clear_canvas()
        grass.draw(400, 30)
        boy.clip_draw(
            100 * frame, 200,
            100, 100,
            x, 90,
            100, 100
        )
        update_canvas()

        frame = (frame + 1) % 8
        delay(0.05)


    frame = 0
    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        boy.clip_draw(
            100 * frame, 300,
            100, 100,
            x, 90,
            100, 100
        )
        update_canvas()

        frame = (frame + 1) % 8
        delay(0.05)


close_canvas()

