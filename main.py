from fastapi import FastAPI
from fastapi.responses import FileResponse
import easyocr
from PIL import ImageFont, ImageDraw, Image, ImageFilter
import re
from fastapi import UploadFile
from datetime import datetime
import hashlib
from matplotlib import pyplot as plt

# async / await 비동기 처리가능
app = FastAPI()

# this needs to run only once to load the model into memory
reader = easyocr.Reader(['ko', 'en'])
def func(filenametemp):
    # 이미지 원본과 결과값의 좌표값 넣으면 블러처리하는 함수

    def rounded_rectangle(draw, xy, fill=255):
        temp_xy = []
        for i in xy:
            temp_tuple = tuple([int(i[0]), int(i[1])])
            temp_xy.append(temp_tuple)
        draw.polygon(temp_xy, fill=fill)

    img = Image.open(filenametemp)
    # 텍스트 찾는 AI
    if (img.size[0]//100)*(img.size[1]//100)>400:
        text_detect_result = reader.detect(filenametemp, min_size=3, text_threshold=0.3, low_text=0.4, link_threshold=0.1,
                               width_ths=0.3 ) #최소사이즈, 텍스트 최소인식률, 작아질수록 인식 업 , ,박스 합쳐지는 범위
    else:
        text_detect_result = reader.detect(filenametemp, min_size=3, text_threshold=0.3, low_text=0.4,
                                           link_threshold=0.1,
                                           width_ths=0.5)  # 최소사이즈, 텍스트 최소인식률, 작아질수록 인식 업 , ,박스 합쳐지는 범위
    # 찾은 텍스트를 txt 포맷으로 변경
    result = reader.recognize(filenametemp, text_detect_result[0][0],text_detect_result[1][0],batch_size=4)

    registNum = '(\d{6}[ ,-]-?[1-4]\d{7})|(\d{6}[ ,-]?[1-4])'
    account = '([0-9,\-]{3,9}\-[0-9,\-]{2,6}\-[0-9,\-])'
    address1 = '(([가-힣]+(시|도)|[서울]|[인천]|[대구]|[광주]|[부산]|[울산])+( |)[가-힣]+(시|군|구))'
    address2 = '(([가-힣]+(d|d(,|.)d|)+(읍|면|동|가|리))(^구|)((d(~|-)d|d)(가|리|)|))([ ](산(d(~|-)d|d))|)|(([가-힣]|(d(~|-)d)|d)+(로|길))'
    address3 = '([가-힣]*\s?[\d]+(동)\s?[\d]+(호)|[\d]+(호)[\s\S]*)'
    phone = '([O\d]{2,3}[ ,-]-?[O|\d]{2,4}[ ,-]-?[O|\d]{4})'
    email = '(([\w!-_\.])*@([\w!-_\.]))'
    carNum1 = '^[가-힣]{2}\d{2}[가-힣]{1}\d{4}$'
    carNum2 = '^\d{2,3}[가-힣]{1}\d{4}$'


    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    temp_draw = ImageDraw.Draw(img)
    for i in result:
        # print(i[0],i[1],i[2])
        # 디텍션 된 텍스트가 전체 크기의 1/256보다 작다면 그냥 블러처리
        if (img.size[0]*img.size[1])/4096 > (i[0][1][0]-i[0][0][0])*(i[0][2][1]-i[0][1][1]):
            rounded_rectangle(draw, i[0], fill=255)
        else:
            if i[2]<0.05:
                rounded_rectangle(draw, i[0], fill=255)
            else:
                if re.match(registNum, str(i[1]).replace(" ",'')) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(account, str(i[1]).replace(" ",'')) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(address1, str(i[1])) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(address2, str(i[1])) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(address3, str(i[1])) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(phone, str(i[1]).replace(" ",'')) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(email, str(i[1])) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(carNum1, str(i[1]).replace(" ",'')) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                elif re.match(carNum2, str(i[1]).replace(" ",'')) != None:
                    rounded_rectangle(draw, i[0], fill=255)
                else:
                    print(i)
                    # print(str(i[1]).replace(" ",''))
                    # temp_xy = []
                    # for i in i[0]:
                    #     temp_tuple = tuple([int(i[0]), int(i[1])])
                    #     temp_xy.append(temp_tuple)
                    # for k in range(4):
                    #     temp_draw.line([temp_xy[k%4], temp_xy[(k+1)%4]], fill="blue", width=1)
                    # draw.text((int((x + x + w) / 2), y - 2), str(i[1]), font=font, fill='red')
    # Blur image
    blurred = img.filter(ImageFilter.GaussianBlur(30))
    # Paste blurred region and save result
    img.paste(blurred, mask=mask)
    img.save(filenametemp,'jpeg')

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    now = datetime.now()
    current_time = now.strftime("%d%H%M%S")
    hashed_name=hashlib.md5(current_time.encode('utf-8')).hexdigest()
    temp_file = open('image/'+str(hashed_name)+'.jpg','wb+')
    temp_file.write(file.file.read())
    func('image/'+str(hashed_name)+'.jpg')

    return {"fileurl": str(hashed_name)+'.jpg'}

@app.get("/downloadfile/{filename}")
async def downloadfile(filename:str):
    return FileResponse(f"image/{filename}")
