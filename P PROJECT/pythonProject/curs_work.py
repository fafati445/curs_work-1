from time import sleep
from tqdm import tqdm
import requests
import json
import configparser

class VKapi:

    config = configparser.ConfigParser()
    config.read('settings.ini')
    VK_TOKEN = config['Tokens']['VK_TOKEN']
    YA_TOKEN = config['Tokens']['YA_TOKEN']

    base_url = 'https://api.vk.com/method/'

    def __init__(self,id,count,yandex_token = YA_TOKEN):
        self.id = id
        self.count = count
        self.yandex_token = yandex_token
        self.z = {}
        self.info = []

    def getphoto_vk(self,count = 6):
        params = {'access_token':self.VK_TOKEN,'v':'5.199','owner_id':self.id,'album_id':'profile','extended':1,'count':self.count}
        resp = requests.get(url=self.base_url+'photos.get',params = params).json()
        count_ = 1
        for itm in tqdm(resp['response']['items']):
            sleep(5)
            print(f'полуаем фото {count_}')
            count_ += 1

            if itm['likes']['user_likes'] not in self.z:
                self.z[itm['likes']['user_likes']] = itm['sizes'][-1]['url']
                self.info.append({'file_name':str(itm['likes']['user_likes'])+'.jpg','size':itm['sizes'][-1]['type']})
            else:
                self.z[f'{str(itm['likes']['user_likes'])},{str(itm['date'])}'] = itm['sizes'][-1]['url']
                self.info.append({'file_name':f'{str(itm['likes']['user_likes'])},{str(itm['date'])}.jpg','size':itm['sizes'][-1]['type']})

    def put_papka_yandex_disc(self):
        headers = {'Authorization':self.yandex_token}
        params = {'path':'image_vk_profile'}
        put_papka = requests.put(url='https://cloud-api.yandex.net/v1/disk/resources',params=params,headers=headers)

    def upload_yandex_disk(self):
        self.getphoto_vk()
        self.put_papka_yandex_disc()
        headers = {'Authorization': self.yandex_token}
        count_ = 1
        for x,y in tqdm(self.z.items()):
            sleep(5)
            print(f'загружаем фото {count_}')
            count_ += 1

            image_url = requests.get(y).content
            image_name = x
            params = {'path': f'image_vk_profile/{str(image_name)}.jpg','overwrite':'true'}
            resp = requests.get(url='https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,params=params).json()['href']
            upload_image = requests.put(url=resp, files={'file': image_url})

    def json_write_reed(self):
        self.upload_yandex_disk()
        with open('text.json','w') as f:
            f.write(json.dumps(self.info))
        with open('text.json') as f2:
            return json.loads(f2.read())

x = input('введите свой вк айди: ')
x2 = input('введите количество фоток: ')
vk_man = VKapi(x,x2)
print(vk_man.json_write_reed())