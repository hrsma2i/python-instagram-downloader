import os
from glob import glob
#pythonista
import photos

import requests
from InstagramAPI import InstagramAPI


def get_url(media):
    return media['image_versions2']\
        ['candidates'][0]['url']
        

def download_img():
    secrete_file = './secrete.txt'

    with open(secrete_file) as f:
        username, password = [l.rstrip() for l in f.readlines()]

    with open('./complete') as f:
        completes = [l.rstrip() for l in f.readlines()]

    api = InstagramAPI(username, password)
    api.login()

    api.getSelfSavedMedia()
    result = api.LastJson
    items = result['items']
    print(len(items))
    items = [item for item in items
             if item['media']['id'] not in completes]
    print(len(items))

    for item in items:
        media = item['media']
        img_urls = []

        if 'carousel_media' in media.keys():
            for m in media['carousel_media']:
                img_urls.append(get_url(m))
        elif 'image_versions2' in media.keys():
            img_urls.append(get_url(media))
                
        for url in img_urls:
            res = requests.get(url)
            img_bin = res.content
            out_dir = './downloads'
            out_name = os.path.basename(url)
            out_name = out_name.split('jpg')[0] + 'jpg'
            print(out_name)
            out_file = os.path.join(out_dir, out_name)
            with open(out_file, 'wb') as f:
                f.write(img_bin)

    with open('./complete', 'a') as f:
        f.write('\n'.join([item['media']['id'] for item in items]))
        f.write('\n')


def save_to_photo_app():
   img_dir = './downloads' 
   img_files = glob(os.path.join(img_dir, '*'))

   for img_file in img_files:
        photos.create_image_asset(img_file) 


def main():
    download_img()
    save_to_photo_app()


if __name__=='__main__':
    main()
