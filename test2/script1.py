import os
from pathlib import Path
from proccesing import *
from collections import Counter


path = Path('data/')


def main():
    for file in os.listdir(path):
        data, counter = datacollect(os.path.join(path, file))
        print(f'В файле {"*" * 20} "{file}" {"*" * 20} содержится:')
        print(f'1. Общее количество изображений - {data["images"]} шт.')
        print(f'2. Размеченных изображений - {data["immarking"]} шт.')
        print(f'3. Не размеченных изображений - {data["images"] - data["immarking"]} шт.')

        print(f'5. Общее количество фигур {sum(data["fig"].values())}')
        for key, val in data['fig'].items():
            print(f'Фигура "{key}" встречается {val} раз(а).')

        width, height = data['maximage']['width'], data['maximage']['height']
        print(f'Самое большое изображение имеет размер {width}x{height}, '
              f'такое изображение встречается {counter[(width, height)]} раз(а)')
        print(f'Информация о таком изображении:\n'
              f'ширина - {width}, высота - {height}, номер ID - {data["maximage"]["id"]}, '
              f'имя изображения - {data["maximage"]["name"].split("/")[-1]}')
        width, height = data['minimage']['width'], data['minimage']['height']
        print(f'Самое маленькое изображение имеет размер {width}x{height}, '
              f'такое изображение встречается {counter[(width, height)]} раз(а)')
        print(f'Информация о таком изображении:\n'
              f'ширина - {width}, высота - {height}, номер ID - {data["minimage"]["id"]}, '
              f'имя изображения - {data["minimage"]["name"].split("/")[-1]}')
        print()


if __name__ == '__main__':
    main()
