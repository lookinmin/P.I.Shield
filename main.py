import cv2
import numpy as np
from fastapi import FastAPI
from fastapi.responses import FileResponse
import easyocr
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image, ImageFilter
import re
from fastapi import UploadFile
from datetime import datetime
# async / await 비동기 처리가능
app = FastAPI()

#/ 주소 들어가면 get 메소드로 파일 리턴
@app.get("/")
def run():
    return FileResponse('index.html')
# this needs to run only once to load the model into memory
reader = easyocr.Reader(['ko', 'en'])

def func(filenametemp):
    # 텍스트 찾는 AI
    text_detect_result = reader.detect(filenametemp, min_size=3, text_threshold=0.1, low_text=0.4, link_threshold=0.2,
                               width_ths=0.5) #최소사이즈, 텍스트 최소인식률, 작아질수록 인식 업 , ,박스 합쳐지는 범위

    # tempImg = cv2.imread(filenametemp)
    # tempImg = cv2.dilate(tempImg, np.ones((1,1),np.uint8), iterations=1)
    # tempImg = cv2.morphologyEx(tempImg, cv2.MORPH_OPEN, np.ones((2,2),np.uint8))
    # tempImg = cv2.cvtColor(tempImg, cv2.COLOR_BGR2RGB)
    # plt.imshow(tempImg)
    # plt.show()

    # 찾은 텍스트를 txt 포맷으로 변경
    result = reader.recognize(filenametemp, text_detect_result[0][0],text_detect_result[1][0])

    registNum = '(\d{6}[ ,-]-?[1-4]\d{6})|(\d{6}[ ,-]?[1-4])'
    name = '^[가-힣]{2,3}$'
    account = '([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-])'
    address1 = '(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+)'
    address2 = '(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d-]+)|(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d][^시]+)'
    phone = '(\d{2,3}[ ,-]-?\d{2,4}[ ,-]-?\d{4})'
    email = '(([\w!-_\.])*@([\w!-_\.]))'

    img = Image.open(filenametemp)
    font = ImageFont.truetype('malgun.ttf', 50) #폰트 지정
    draw = ImageDraw.Draw(img)

    #이미지의 크기와 같은 복사본 안에 블러처리할 부분을 지정
    def rounded_rectangle(draw, xy, rad, fill=None):
        x0, y0, x1, y1 = xy
        draw.rectangle([ (x0, y0 + rad), (x1, y1 - rad) ], fill=fill)
        draw.rectangle([ (x0 + rad, y0), (x1 - rad, y1) ], fill=fill)
        draw.pieslice([ (x0, y0), (x0 + rad * 2, y0 + rad * 2) ], 180, 270, fill=fill)
        draw.pieslice([ (x1 - rad * 2, y1 - rad * 2), (x1, y1) ], 0, 90, fill=fill)
        draw.pieslice([ (x0, y1 - rad * 2), (x0 + rad * 2, y1) ], 90, 180, fill=fill)
        draw.pieslice([ (x1 - rad * 2, y0), (x1, y0 + rad * 2) ], 270, 360, fill=fill)

    for i in result:
        print(i[1],i[2])
        x = i[0][0][0]
        y = i[0][0][1]
        w = i[0][1][0] - i[0][0][0]
        h = i[0][2][1] - i[0][1][1]

        if re.match(registNum, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
            # elif re.match(name, str(i[1])) != None:
            #     mask = Image.new('L', img.size, 0)
            #     draw = ImageDraw.Draw(mask)
            #     rounded_rectangle(draw, (x, y, x+w, y+h), rad=40, fill=255)
            #     # Blur image
            #     blurred = img.filter(ImageFilter.GaussianBlur(20))
            #     # Paste blurred region and save result
            #     img.paste(blurred, mask=mask)
        elif re.match(account, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(address1, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(address2, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(phone, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(email, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, (x, y, x + w, y + h), rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)

        else:
            draw.rectangle(((x, y), (x + w, y + h)), outline='red', width=2)
            draw.text((int((x + x + w) / 2), y - 2), str(i[1]), font=font, fill='red')

    plt.figure(figsize=(20, 20))
    img.save('modify'+filenametemp,'jpeg')

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    now = datetime.now()
    current_time = now.strftime("%d%H%M%S")
    print(current_time)
    temp_file = open(current_time+'.jpg','wb+')
    temp_file.write(file.file.read())
    func(current_time+'.jpg')

    return {"filename": file.filename+current_time+'.jpg'}