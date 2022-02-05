from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

import os
import requests
from fastapi.middleware.cors import CORSMiddleware

import webbrowser as web

from PIL import Image

from fastapi.responses import PlainTextResponse

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import csv

from search import search_and_block

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None): # чтение получиной информации, запись
    return {"item_id": item_id, "q": q}

@app.post('/links')
def lists(url: List[str]): # проверка наличия ссылки в списках
    url = str(url)[2:-2]
    if url == 'file:///E:/server/html_parents/HomePageForParents.html':
        return 1
    with open('data/whiteList.csv', newline='') as f:
        reader = csv.reader(f)
        whitelist = list(reader)[0]
    with open('data/blackList.csv', newline='') as f:
        reader = csv.reader(f)
        blacklist = list(reader)[0]
    whitelist = str(whitelist)
    blacklist = str(blacklist)
    if whitelist.find(url) != -1:
        res = 1
    elif blacklist.find(url) != -1:
        res = 2
    else:
        res = -1
    return res

@app.post('/test')
async def list_of_images(images: List[str]): # перебор полученных изображения и дальнейшее загрузка и проверка
    print('test method called')
    if not images:
        return {'message': 'No images sent in request'}
    for image in images:
        try:
            download(image, dest_folder="download")
        except:
            print('something went wrong')
    result = chek()
    return result

def download(url: str, dest_folder: str): # загрузка изображений
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # создать папку, если она не существует

    filename = url.split('/')[-1].replace(" ", "_")  # будьте осторожны с именами файлов
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

def chek(): # проверка изображений
    path = 'download\\'
    images = os.listdir(path)
    for i in range(len(images)):
        try:
            if ("download\\" + str(images[i]))[-4::] == 'webp':
                img = Image.open("download\\" + str(images[i])).convert("RGB")
                img.save(("download\\" + str(images[i]))[-4::] + 'jpg', "jpeg")
                os.remove("download\\" + str(images[i+1]))
            if ("download\\" + str(images[i]))[-3::] == 'svg':
                drawing = svg2rlg("download\\" + str(images[i]))
                renderPM.drawToFile(drawing, "download\\" + str(images[i])[0:(len(images[i]) - 3)] + "png", fmt="PNG")
                os.remove("download\\" + str(images[i]))
                detect = search_and_block("download\\" + str(images[i])[0:(len(images[i]) - 3)] + 'png')
            elif ("download\\" + str(images[i])).find('.') == -1:
                os.rename("download\\" + str(images[i]), "download\\" + str(images[i]) + '.jpg')
                detect = search_and_block("download\\" + str(images[i]) + '.jpg')
            else:
                detect = search_and_block("download\\" + str(images[i]))
            if detect == 2: # если 1(0) - не найден нежелательный контент, клиенту ответ 2(1) - переход на яндекс страницу
                i = len(images) + 1
                break
        except ValueError:
            detect = 1
    delete_img()
    return detect

def delete_img(): # удаление содержания папки download
    path = 'download\\'
    images = os.listdir(path)
    for i in range(len(images)):
        os.remove("download\\" + str(images[i]))

@app.get("/geturl/{url}") # добавление запрещенной ссылки
async def addlink(addlink: str):
    print(addlink)
    with open('data/blackList.csv', 'a') as f:
        f.write(',' + addlink)
    url = 'file:///E:/server/HomePageForParents.html'
    web.open(url)

@app.get("/word/{wrd}") # добавление запрещенных слов
async def addwrd(addwrd: str):
    print(addwrd)
    with open('data/bad_words.csv', 'a') as f:
        f.write(',' + addwrd)
    url = 'file:///E:/server/HomePageForParents.html'
    web.open(url)

@app.get("/{passLog}")
async def verify(log: str, psw: str): # проверка логина и пароля
    with open('data/passLog.csv', newline='') as f:
        reader = csv.reader(f)
        passLog = list(reader)
        passLog.pop(0)
    passLog = str(passLog)
    if passLog.find(log + "', '" + psw) >= 0:
        print("Yes")
        url = 'file:///E:/server/HomePageForParents.html'
        web.open(url, new=2)
    else:
        print("Try again")
    print(log, psw)


delete_img()
#uvicorn main:app --reload - запуск