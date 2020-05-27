

import json
from PIL import Image, ImageDraw, ImageColor
import requests
import time

def load_api_key(json_file):
    '''
    json file should a json file structured like this {api_key:"<key>", secret_api_key:"<secret>"}
    '''
    api_key = ""
    secret_api_key = ""

    try:
        file = open(json_file, 'r', encoding="utf-8")
        data = json.load(fp=file)
        file.close()
        secret_api_key = data['secret_api_key']
        api_key = data['api_key']
    except Exception as e:
        print('Error {}'.format(e))
        return None

    return (secret_api_key, api_key)


def create_image(data, icon_size, color, icon_name, icon_extension):
    '''
    data is the bat price
    '''
    image = Image.new('RGBA', icon_size, color)
    dc = ImageDraw.Draw(image)
    dc.text((icon_size[0]*0.10, icon_size[1]/2*0.85), data, fill=(0, 0, 0, 0))
    image.save(icon_name, icon_extension)

def get_price_bat(url_api, headers):
    session = requests.Session()
    session.headers.update(headers)

    try:
        response = session.get(url_api)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(e)
        return None

ICON_SIZE = (64, 64)
BACKGROUND_COLOR = (255, 255, 255, 1)
ICON_EXTENSION = "PNG"
ICON_NAME = "bat_ico."+ICON_EXTENSION.lower()

KEY_FILE = "api_key.json"

SECRET_API_KEY, API_KEY = load_api_key(KEY_FILE)
BASE_HOST = "https://api.binance.com"
BAT_API_URL = "/api/v3/avgPrice"
REQUEST_HEADER = {
    "X-MBK-APIKEY": API_KEY
}
REQUEST_PARAMETER = "symbol=USDBAT"

data = get_price_bat(BASE_HOST+BAT_API_URL+"?"+REQUEST_PARAMETER, REQUEST_HEADER)
print(data)