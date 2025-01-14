from time import sleep
from tqdm import tqdm
import requests
import json
import configparser

class BASE:
    config = configparser.ConfigParser()
    config.read('settings.ini')
    base_url = 'https://api.vk.com/method/'
    ya_token = config['Tokens']['YA_TOKEN']
    vk_token = config['Tokens']['VK_TOKEN']

class VKapi(BASE):
    def __init__(self, id, count):
        self.id = id
        self.count = count
        self.z = {}
        self.info = []

    def getphoto_vk(self):
        params = {'access_token': BASE.vk_token, 'v': '5.199', 'owner_id': self.id, 'album_id': 'profile',
                  'extended': 1, 'count': self.count}
        resp = requests.get(url=self.base_url + 'photos.get', params=params).json()
        for itm in resp['response']['items']:

            if itm['likes']['user_likes'] not in self.z:
                self.z[itm['likes']['user_likes']] = itm['sizes'][-1]['url']
                self.info.append(
                    {'file_name': str(itm['likes']['user_likes']) + '.jpg', 'size': itm['sizes'][-1]['type']})
            else:
                self.z[f'{str(itm['likes']['user_likes'])},{str(itm['date'])}'] = itm['sizes'][-1]['url']
                self.info.append({'file_name': f'{str(itm['likes']['user_likes'])},{str(itm['date'])}.jpg',
                                  'size': itm['sizes'][-1]['type']})
        return self.z, self.info


class YA_disc(BASE):

    def __init__(self):
        vk_man.getphoto_vk()
        self.dict = vk_man.z
        self.info = vk_man.info

    def put_papka_yandex_disc(self):
        headers = {'Authorization': BASE.ya_token}
        params = {'path': 'image_vk_profile'}
        put_papka = requests.put(url='https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)

    def upload_yandex_disk(self):
        self.put_papka_yandex_disc()
        headers = {'Authorization': self.ya_token}
        count_ = 1
        for x, y in tqdm(self.dict.items()):
            print(f'загружаем фото {count_}')
            sleep(2)
            count_ += 1
            image_url = requests.get(y).content
            image_name = x
            params = {'path': f'image_vk_profile/{str(image_name)}.jpg', 'overwrite': 'true'}
            resp = requests.get(url='https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,
                                params=params).json()['href']
            upload_image = requests.put(url=resp, files={'file': image_url})

    def json_write_reed(self):
        self.upload_yandex_disk()
        with open('text.json', 'w') as f:
            f.write(json.dumps(self.info))
        with open('text.json') as f2:
            return json.loads(f2.read())

if __name__ == '__main__':
    vk_man = VKapi(input('введите свой вк айди: '), input('введите количество фоток: '))
    ya_man = YA_disc()
    print(ya_man.json_write_reed())
