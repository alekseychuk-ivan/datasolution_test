import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import requests
from fake_useragent import UserAgent


link = 'https://auto.ru/'
fullpath = os.path.join(os.getcwd(), )

ua = UserAgent(browsers='chrome')


def getpage(url: str, name: str = 'index.html') -> None:
    """The function gets URLs and page loads.
      A web driver for chrome is being created, random generation of a user agent is used to reduce the appearance
      captcha. Also, to reduce the likelihood of a captcha appearing, an imitation of pressing the esc and
      end keys is used. Timeout 20"""

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f'-user-agent={ua.random}')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url=url)
        page = driver.find_element(By.TAG_NAME, 'html')
        page.send_keys(Keys.ESCAPE)
        page.send_keys(Keys.END)
        # driver.implicitly_wait(20)
        time.sleep(20)
        while True:
            with open(os.path.join(fullpath, name), 'w', encoding='utf-8') as file:
                file.write(driver.page_source)
            if os.path.isfile(os.path.join(fullpath, name)):
                break
            print(f'I cant create file')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def getbrandsurl(filepath: str, num: int = 10) -> dict:
    """The function gets path to start page and number of cars. Return dict(brand: url_to_brand)"""
    with open(filepath, 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    carurls = soup.find_all('a', class_='IndexMarks__item')
    brandcar = dict()
    for carurl in carurls[:num]:
        name = carurl.find(class_="IndexMarks__item-name").get_text('\n', strip=True)
        href = carurl.get('href')
        brandcar[name] = href
    return brandcar


def getdata(name: str, href: str, dir: str, numphoto: int = 5) -> None:
    """The function gets name car, url to car, path to dir for save images and number of images."""
    getpage(url=href, name=f'{name}.html')
    with open(os.path.join(fullpath, f'{name}.html'), 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    images = soup.find_all(attrs={"class": 'ImageGalleryDesktop__itemContainer'})  # ImageGalleryDesktop__image-container 'ImageGalleryDesktop__image'
    for i, image in enumerate(images):
        if i == numphoto:
            break
        imgurl = 'https:' + image.find(class_='ImageGalleryDesktop__image').get('src')
        Image.open(BytesIO(requests.get(imgurl).content)).convert("RGB").save(os.path.join(f'{dir}', f'{name}_{i}.jpg'))
    os.remove(os.path.join(fullpath, f'{name}.html'))


def getcar(branddct: dict, num: int = 10, numphoto: int = 5) -> None:
    """Get dict(brand: url_to_brand), number of announcements"""
    for key, link in branddct.items():
        number = num
        print(f'Start download {key}')
        dir = os.path.join(fullpath, key)
        if not os.path.isdir(dir):
            os.mkdir(dir)

        getpage(url=link, name=f"{key}.html")
        with open(os.path.join(fullpath, f'{key}.html'), 'r', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')

        startpagen = 1
        while number:
            allcars = soup.find_all('div', class_='ListingItem__main')
            for car in allcars:
                name = car.find(class_='Link ListingItemTitle__link').get_text('\n', strip=True)
                name = name.replace('/', '_')
                href = car.find(class_='Link ListingItemTitle__link').get('href')
                getdata(name, href, numphoto=numphoto, dir=dir)
                number -= 1
                if number == 0:
                    break
            if number:
                startpagen += 1
                getpage(url=link + f'?page={startpagen}', name=f"{key}.html")
                with open(os.path.join(fullpath, f'{key}.html'), 'r', encoding='utf-8') as file:
                    src = file.read()
                soup = BeautifulSoup(src, 'lxml')

        print(f'Download {key} complete')
        os.remove(os.path.join(fullpath, f'{key}.html'))


if __name__ == '__main__':
    getpage(url=link)
    getcar(branddct=getbrandsurl(filepath=os.path.join(fullpath, 'index.html')))
    os.remove(os.path.join(fullpath, 'index.html'))
