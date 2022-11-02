from re import template
from urllib import request
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
# async / await 비동기 처리가능
app = FastAPI()
