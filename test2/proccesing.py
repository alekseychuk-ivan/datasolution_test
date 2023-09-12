import xml.etree.ElementTree as ET
from collections import Counter
import os


def read_xml(path: str) -> str:
    """The function gets path to xml file."""
    with open(path, 'r', encoding='utf-8') as file:
        xmlr = file.read()
    start = xmlr.find('</meta>') + len('</meta>\n')
    newxml = f'<annotations>\n' + xmlr[start:]
    return ET.fromstring(newxml)


def read_xml_full(path: str) -> tuple:
    """The function gets path to xml file. Return """
    tree = ET.parse(os.path.join(path))
    return tree, tree.getroot()


def datacollect(path: str) -> tuple:
    """The function collects daa from xml file. Return dict with figures, classes from xml, minimal and maximal images,
    number of images and marking images, counter with size of images."""
    root = read_xml(path)
    sizelst = []
    dct_class, dct_fig = dict(), dict()
    im, immarking = 0, 0
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
        for subtag in image:
            dct_fig[subtag.tag] = dct_fig.get(subtag.tag, 0) + 1
            dct_class[subtag.get('label')] = dct_class.get(subtag.get('label'), 0) + 1
            markvar = 1
        immarking += markvar

    return {'fig': dct_fig, 'class': dct_class, 'maximage': bigimagedata, 'minimage': minimagedata, 'images': im,
            'immarking': immarking}, Counter(sizelst)


def step7(inpath: str, outpath: str) -> None:
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    for file in os.listdir(inpath):
        tree, root = read_xml_full(os.path.join(inpath, file))
        for image in root.findall('image'):
            image.set('id', image.get('id')[-1::-1])

        tree.write(os.path.join(outpath, f'{file.split(".")[0]}_7.xml'))
    print(f'Задание "Изменить id-шники изображений - сделать их в обратном порядке" завершено, '
          f'результаты в папке "{outpath}"')


def step8(inpath: str, outpath: str) -> None:
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    for file in os.listdir(inpath):
        tree, root = read_xml_full(os.path.join(inpath, file))
        for image in root.findall('image'):
            image.set('name', str(*image.get('name').split('.')[:-1]) + '.png')

        tree.write(os.path.join(outpath, f'{file.split(".")[0]}_8.xml'))
    print(f'Задание "Изменить name изображений - поменять расширение на "png"" завершено, '
          f'результаты в папке "{outpath}"')


def step9(inpath: str, outpath: str) -> None:
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
    for file in os.listdir(inpath):
        tree, root = read_xml_full(os.path.join(inpath, file))
        for image in root.findall('image'):
            image.set('name', str(image.get('name').split('/')[-1]))

        tree.write(os.path.join(outpath, f'{file.split(".")[0]}_9.xml'))
    print(f'Задание "Изменить name изображений - удалить путь к файлу, оставить только '
          f'название самого файла" завершено, результаты в папке "{outpath}"')
