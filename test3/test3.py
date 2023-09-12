import os.path
from pathlib import Path
from PIL import Image, ImageDraw
from test2.proccesing import *


path = Path('data/images')
maskpath = Path('data/masks.xml')
pathtosave = Path('result')


def polygon(image: Image.Image, coords: list, color: str) -> None:
    """Add polysin to image. Input image, coordinates and color polygon"""
    draw = ImageDraw.Draw(image)
    draw.polygon(coords, fill=color)


def paste_and_save(image1: Image.Image, image2: Image.Image, mask: Image.Image, pathsave: Path) -> None:
    """The function paste image2 to image1 with mask and save to pah"""
    image1.paste(image2, mask)
    image1.save(pathsave)


def main():
    if not os.path.isdir(pathtosave):
        os.mkdir(pathtosave)
    _, root = read_xml_full(maskpath)
    dctmask = {'Skin': 'purple', 'Ignore': 'black'}
    for image in root.findall('image'):
        file = image.get('name').split('/')[-1]
        # open original image and copy
        original = Image.open(os.path.join(path, file))
        immask = original.copy()
        # create start mask image
        mask = Image.new('L', original.size, 'white')
        oblack = Image.new('RGB', original.size, 'black')
        imblack = oblack.copy()
        for subtag in image:
            label = subtag.get('label')
            coords = list()
            for xy in subtag.get('points').split(';'):
                xy = xy.split(',')
                coords.append(tuple(map(int, (map(float, xy)))))
            if label == 'Ignore':
                polygon(mask, coords, dctmask[label])
            else:
                polygon(immask, coords, dctmask[label])
                polygon(imblack, coords, dctmask[label])

        paste_and_save(original, immask, mask, Path(f'{pathtosave}/{file}'))
        paste_and_save(oblack, imblack, mask, Path(f'{pathtosave}/black_{file}'))


if __name__ == '__main__':
    main()
