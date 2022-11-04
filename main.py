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
        temp_xy = []
        for i in xy:
            temp_tuple = tuple([int(i[0]), int(i[1])])
            temp_xy.append(temp_tuple)
        draw.polygon(temp_xy, fill=fill)

    for i in result:
        print(i[0],i[1],i[2])

        if re.match(registNum, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, i[0], rad=5, fill=255)
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
            rounded_rectangle(draw, i[0], rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(address1, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, i[0], rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(address2, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, i[0], rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(phone, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, i[0], rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)
        elif re.match(email, str(i[1])) != None:
            mask = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(mask)
            rounded_rectangle(draw, i[0], rad=5, fill=255)
            # Blur image
            blurred = img.filter(ImageFilter.GaussianBlur(20))
            # Paste blurred region and save result
            img.paste(blurred, mask=mask)

        else:
            draw = ImageDraw.Draw(img)
            temp_xy = []
            for i in i[0]:
                temp_tuple = tuple([int(i[0]), int(i[1])])
                temp_xy.append(temp_tuple)
            for k in range(4):
                draw.line([temp_xy[k%4],
                          temp_xy[(k+1)%4]], fill="blue", width=1)
            # draw.text((int((x + x + w) / 2), y - 2), str(i[1]), font=font, fill='red')
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