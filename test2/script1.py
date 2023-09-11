from pathlib import Path
import xml.etree.ElementTree as ET
from collections import Counter


path = Path('data/annotations.xml')


def main():
    with open(path, 'r', encoding='utf-8') as file:
        xmlr = file.read()
    start = xmlr.find('</meta>') + len('</meta>\n')
    newxml = f'<annotations>\n' + xmlr[start:]
    root = ET.fromstring(newxml)
    im, immarking = 0, 0
    sizelst = []
    dct_class, dct_fig = dict(), dict()
    dct_data = dict()
    bigarea, minarea = 0, 60000 * 60000

    for image in root:
        im += 1
        markvar = 0
        width = int(image.get('width'))
        height = int(image.get('height'))
        sizelst.append((width, height))
        if height * width > bigarea:
            bigimagedata = {"width": width, "height": height, 'id': image.get('id'), 'name': image.get('name')}
            bigarea = height * width
        if height * width < minarea:
            minimagedata = {"width": width, "height": height, 'id': image.get('id'), 'name': image.get('name')}
            minarea = height * width
        if (width, height) not in dct_data:
            dct_data[(width, height)] = image.attrib
        for subtag in image:
            dct_fig[subtag.tag] = dct_fig.get(subtag.tag, 0) + 1
            dct_class[subtag.get('label')] = dct_class.get(subtag.get('label'), 0) + 1
            markvar = 1
        immarking += markvar

    print(f'1. Общее количество изображений {im}')
    print(f'2. Размеченных изображений {immarking}')
    print(f'3. Не размеченных изображений {im - immarking}')
    print(f'4. Статистика по классам:')
    for key, val in dct_class.items():
        print(f'Класс "{key}" встречается {val} раз(а)')

    print(f'5. Общее количество фигур {sum(dct_fig.values())}')
    for key, val in dct_fig.items():
        print(f'Фигура "{key}" встречается {val} раз(а).')

    counter = Counter(sizelst)
    width, height = bigimagedata['width'], bigimagedata['height']
    print(f'Самое большое изображение имеет размер {width}x{height}, '
          f'такое изображение встречается {counter[(width, height)]} раз(а)')
    print(f'Информация о любом таком изображении:\n'
          f'ширина - {width}, высота - {height}, номер ID - {bigimagedata["id"]}, '
          f'имя изображения - {bigimagedata["name"].split("/")[-1]}')
    width, height = minimagedata['width'], minimagedata['height']
    print(f'Самое маленькое изображение имеет размер {width}x{height}, '
          f'такое изображение встречается {counter[(width, height)]} раз(а)')
    print(f'Информация о любом таком изображении:\n'
          f'ширина - {width}, высота - {height}, номер ID - {minimagedata["id"]}, '
          f'имя изображения - {minimagedata["name"].split("/")[-1]}')


if __name__ == '__main__':
    main()
