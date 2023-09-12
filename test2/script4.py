from pathlib import Path
from proccesing import *

path = Path('data/')
outpath7 = Path('result_7')
outpath8 = Path('result_8')
outpath9 = Path('result_9')


def main():
    step7(inpath=path, outpath=outpath7)
    step8(inpath=path, outpath=outpath8)
    step9(inpath=path, outpath=outpath9)


if __name__ == '__main__':
    main()
