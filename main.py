

import json
from PIL import Image, ImageDraw, ImageFont
import requests
import pystray

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


def create_image(data, icon_size, color, font, font_size, icon_name, icon_extension):
    '''
    data is the bat price
    '''
    image = Image.new('RGBA', icon_size, color)
    dc = ImageDraw.Draw(image)
    center_y = icon_size[1]/2-font_size/2
    dc.text((1, center_y), data, fill="white", font=font, align='right')
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
FONT_SIZE = 35
FONT = ImageFont.truetype("Roboto-Bold.ttf", FONT_SIZE)

KEY_FILE = "api_key.json"

SECRET_API_KEY, API_KEY = load_api_key(KEY_FILE)
BASE_HOST = "https://api.binance.com"
BAT_API_URL = "/api/v3/avgPrice"
REQUEST_HEADER = {
    "X-MBK-APIKEY": API_KEY
}
REQUEST_PARAMETER = "symbol=BATUSDT"

#Get BAT price
data = get_price_bat(BASE_HOST+BAT_API_URL+"?"+REQUEST_PARAMETER, REQUEST_HEADER)
print(data)

#Reduce the number of digit
data = data['price'][2:5]
print(data)

#Make an image with the price
create_image(data, ICON_SIZE, BACKGROUND_COLOR, FONT, FONT_SIZE, ICON_NAME, ICON_EXTENSION)

#Create a window tray
print("Tray icon run")
img = Image.open('bat_ico.png', 'r')
tray_icon = pystray.Icon('Test name')
tray_icon.icon = img

def setup(icon):
    icon.visible = True

tray_icon.run(setup)
