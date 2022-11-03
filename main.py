import os
from re import template
from urllib import request

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import easyocr
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image, ImageFilter
import re
# async / await 비동기 처리가능
app = FastAPI()

#/ 주소 들어가면 get 메소드로 파일 리턴
@app.get("/")
def run():
    return FileResponse('index.html')



# this needs to run only once to load the model into memory
reader = easyocr.Reader(['ko', 'en'])
def func(filenametemp):
    result = reader.readtext(filenametemp)

    jumin = '(\d{6}[ ,-]-?[1-4]\d{6})|(\d{6}[ ,-]?[1-4])'
    name = '^[가-힣]{2,3}$'
    account = '([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-])'
    address1 = '(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+)'
    address2 = '(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d-]+)|(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d][^시]+)'
    phone = '(\d{2,3}[ ,-]-?\d{2,4}[ ,-]-?\d{4})'
    email = '(([\w!-_\.])*@([\w!-_\.])*\.[\w]{2,3})'


    img = cv2.imread(filenametemp)
    img = Image.fromarray(img)
    font = ImageFont.truetype('malgun.ttf', 50)
    draw = ImageDraw.Draw(img)

    def rounded_rectangle(draw, xy, rad, fill=None):
        x0, y0, x1, y1 = xy
        draw.rectangle([ (x0, y0 + rad), (x1, y1 - rad) ], fill=fill)
        draw.rectangle([ (x0 + rad, y0), (x1 - rad, y1) ], fill=fill)
        draw.pieslice([ (x0, y0), (x0 + rad * 2, y0 + rad * 2) ], 180, 270, fill=fill)
        draw.pieslice([ (x1 - rad * 2, y1 - rad * 2), (x1, y1) ], 0, 90, fill=fill)
        draw.pieslice([ (x0, y1 - rad * 2), (x0 + rad * 2, y1) ], 90, 180, fill=fill)
        draw.pieslice([ (x1 - rad * 2, y0), (x1, y0 + rad * 2) ], 270, 360, fill=fill)

    for i in result:
        print(i[1])
        x = i[0][0][0]
        y = i[0][0][1]
        w = i[0][1][0] - i[0][0][0]
        h = i[0][2][1] - i[0][1][1]

        if re.match(account, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x+w, y+h), rad=40, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(name, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x+w, y+h), rad=40, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)

        else:
            draw.rectangle(((x, y), (x + w, y + h)), outline='red', width=2)
            draw.text((int((x + x + w)/2), y-2), str(i[1]), font=font, fill='red')


    plt.figure(figsize=(20, 20))
    plt.imshow(img)
    plt.show()


from fastapi import UploadFile, File
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    temp_file=open(str(file.filename),'wb+')
    temp_file.write(file.file.read())
    func(file.filename)
    img = cv2.imread(file.filename)
    img = Image.fromarray(img)
    plt.imshow(img)
    plt.show()
    return {"filename": file.filename}