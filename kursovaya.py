import requests
import time
import json
from tqdm import tqdm
from datetime import datetime


class VK:
   def __init__(self, access_token, my_id, version='5.199'):
       self.token = access_token
       self.id = my_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()

with open('token.txt') as f:
    access_token = f.read()


def vk_download(offset=0, count=5):
    response = requests.get('https://api.vk.com/method/photos.get', params={
        'owner_id': my_id,
        'access_token': access_token,
        'offset': offset,
        'count': count,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'v': '5.199'
    })
    return response.json()


my_id = input('Введите ID пользователя ВКонтакте: ')
vk = VK(access_token, my_id)
if my_id.isdigit() == False:
    print('Неверный ID, попробуйте снова')
else:
    print('Фото будут загружены из профиля пользователя с именем: ')
    print(vk.users_info()['response'][0]['first_name'])
    token_ya = input('Введите токен с Полигона Яндекс.Диска: ')



    likes = 0
    dict_j = {}
    dict_j['file_name'] = ''
    dict_j['size'] = ''
    data = vk_download()
    for photos in data['response']['items']:
        for i in tqdm(range(data['response']['count'])):
            time.sleep(0.5)
        photo_url = photos['sizes'][-1]['url']
        name_photo = photos['likes']['count']
        date_photo = datetime.fromtimestamp(photos['date'])
        date_photo = str(date_photo)
        date_photo = date_photo.split(' ')[0]
        size_photo = photos['sizes'][-1]['type']
        if name_photo == likes:
            name_photo = str(name_photo) + str(date_photo)
        elif name_photo != likes:
            likes = name_photo
        file_name = photo_url.split('?')[0]
        file_name1 = file_name.split('/')[-1]
        file_name2 = str(name_photo) + file_name1[11:15]
        dict_j['file_name'] = file_name2
        dict_j['size'] = size_photo
        with open('save_file.json', 'a') as f:
            json.dump(dict_j, f)




        response = requests.get(photo_url)
        with open(file_name2, 'wb') as f:
            f.write(response.content)


        # создать папку на Яндекс диске
        params = {'path': 'Kursovaya_rabota'}
        headers = {'Authorization': 'OAuth ' + token_ya}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                params=params,
                                headers=headers)

        # загрузить файл на Яндекс диск
        params = {'path': f'Kursovaya_rabota/{file_name2}'}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                params=params,
                                headers=headers)

        url_for_upload = response.json()['href']

        with open(file_name2, 'rb') as f:
            requests.put(url_for_upload,
                    files={'file': f})



    with open('save_file.json') as f:
        result = f.read()
    print(result)
