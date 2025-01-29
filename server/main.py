#!/usr/bin/env python3

import requests
import json
from fastapi import FastAPI

app = FastAPI()
url = 'https://api.imeicheck.net/v1/checks'


# API
# Проверка работоспособности
@app.get('/api/')
def check_api():
    return {'status': 'OK'}

# Получить IMEI
@app.get('/api/check-imei/')
def check_imei(imei_id: str, token: str):

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    body = json.dumps({
        "deviceId": imei_id,
        "serviceId": 12,
    })
    
    try:
        response = requests.post(url, headers=headers, data=body).json()
    except Exception as e:
        response = json.dumps({'errors': e})

    return response