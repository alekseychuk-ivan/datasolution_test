import math
from pathlib import Path
from PIL import Image, ImageDraw
from test2.proccesing import *


path = Path('data/images')
maskpath = Path('data/masks.xml')


def polygon(image, coords, color):
    draw = ImageDraw.Draw(image)
    draw.polygon(coords, fill=color)



def main():
    _, root = read_xml_full(maskpath)
    dctmask = {'Skin': 'purple', 'Ignore': None}
    dctblack = {'Skin': 'purple', 'Ignore': 'black'}
    for image in root.findall('image'):
        file = image.get('name').split('/')[-1]
        width = int(image.get('width'))
        height = int(image.get('height'))
        immask = Image.open(os.path.join(path, file))
        imblack = Image.new('RGB', (width, height), 'black')
        # immask.show('original')
        for subtag in image:
            label = subtag.get('label')
            coords = list()
            for xy in subtag.get('points').split(';'):
                xy = xy.split(',')
                coords.append(tuple(map(int, (map(float, xy)))))
            polygon(immask, coords, dctmask[label])
            # polygon(imblack, coords, dctblack[label])
        immask.show()
        # imblack.show()


if __name__ == '__main__':
    main()
