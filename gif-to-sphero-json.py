#!python

import sys
import os
from PIL import Image, UnidentifiedImageError
import time
import json


debug = False


def get_avg_fps(PIL_Image_object):
    """
    Returns the average framerate of a PIL Image object
    from: https://stackoverflow.com/questions/53364769/get-frames-per-second-of-a-gif-in-python
    """
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info["duration"]
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames / duration * 1000
    return None


def main():
    print("GIF to Sphero JSON v1.0.1 by Reboot-Codes")

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.isfile(filepath):
            print(f'Attempting to import "{filepath}"...')

            try:
                im = Image.open(filepath)

                if im.format == "GIF":
                    if im.n_frames > 600:
                        print(
                            "Warning: Animation is greater than 600 frames, we will export multiple JSON files."
                        )
                    if im.n_frames > 992:
                        print(
                            "Warning: Sphero BOLT (Polaris) only supports a max of 992 frames per program, regardless of the number of animations within the program. We will still export the full GIF; however you will not be able to use the whole animation."
                        )

                    fps = int(float(get_avg_fps(im)).__floor__())
                    segments = []
                    colorMap = {}
                    colors = []
                    warnedAboutExcessColors = False

                    remainder = im.n_frames % 600
                    totalSegs = int((im.n_frames - remainder) / 600)
                    totalSegs += 1 if remainder else 0

                    for currentSeg in range(0, totalSegs, 1):
                        currentSegArr = []
                        # This works because ranges are zero-indexed
                        startingOffset = currentSeg * 600

                        endingOffset = startingOffset + (
                            remainder
                            if ((remainder != 0) and (currentSeg == (totalSegs - 1)))
                            else 600
                        )

                        for currentFrame in range(startingOffset, endingOffset, 1):
                            im.seek(currentFrame)

                            currentFrameArr = []

                            for y in range(0, 8, 1):
                                currentLineArr = []

                                for x in range(0, 8, 1):
                                    rgb_im = im.convert("RGB")
                                    r, g, b = rgb_im.getpixel((x, y))

                                    colorID = f"{r}, {g}, {b}"
                                    colorNum = 0
                                    if not colorMap.get(colorID):
                                        if (
                                            len(colorMap) == 16
                                            and not warnedAboutExcessColors
                                        ):
                                            print(
                                                "Warn: Number of colors has exceeded 16, new colors will be the first color in the pallet!"
                                            )
                                        else:
                                            nextColorNum = len(colorMap)
                                            colorMap[colorID] = nextColorNum
                                            colors.append({"r": r, "g": g, "b": b})

                                            if debug:
                                                print(
                                                    f"Added new color: `{r}, {g}, {b}` as {nextColorNum}."
                                                )

                                            colorNum = nextColorNum
                                    else:
                                        colorNum = colorMap[colorID]

                                    currentLineArr.append(colorNum)

                                    if debug:
                                        print(
                                            f"{currentSeg}: {currentFrame}: {x}, {y}: {r}, {g}, {b}"
                                        )

                                currentFrameArr.append(currentLineArr)

                            currentSegArr.append(currentFrameArr)

                        segments.append(currentSegArr)

                    unixTimeStamp = time.time()

                    for currentSeg in range(0, totalSegs, 1):
                        with open(
                            f"sphero-animation-{unixTimeStamp}-{currentSeg}.json", "w"
                        ) as f:
                            json.dump(
                                {
                                    "frames": segments[currentSeg],
                                    "palette": colors,
                                    "fps": fps,
                                },
                                f,
                                indent=4,
                            )
                else:
                    print(f'Error: "{format}" is not supported. Please use GIF.')
                    exit(1)

            except UnidentifiedImageError:
                print(f'Error: "{filepath}" is not a valid image!')
                exit(1)
        else:
            print(f'Error: "{filepath}" is not a file!')
            exit(1)
    else:
        print("Error: Please provide a valid filepath as the first argument.")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
