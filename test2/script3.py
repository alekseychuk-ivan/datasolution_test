from pathlib import Path
from proccesing import *

path = Path('data/')


def main():
    for file in os.listdir(path):
        data, counter = datacollect(os.path.join(path, file))
        print(f'В файле {"*" * 20} "{file}" {"*" * 20} содержится:')
        print(f'4. Статистика по классам:')
        for key, val in data['fig'].items():
            print(f'Фигура "{key}" встречается {val} раз',)
        print()


if __name__ == '__main__':
    main()
