import os
from glob import glob
#pythonista
import photos

import requests
from InstagramAPI import InstagramAPI


def get_url(media):
    if 'video_versions' in media.keys():
        return media['video_versions'][0]['url']
    else:
        return media['image_versions2']\
            ['candidates'][0]['url']


def download_img():
    secrete_file = './secrete.txt'

    if not os.path.exists(secrete_file):
        with open(secrete_file, 'w') as f:
            pass
    with open(secrete_file) as f:
        username, password = [l.rstrip() for l in f.readlines()]

    complete_file = './complete.txt'
    if not os.path.exists(complete_file):
        with open(complete_file, 'w') as f:
            pass
    with open(complete_file) as f:
        completes = [l.rstrip() for l in f.readlines()]

    out_dir = './downloads'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

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
            out_name = os.path.basename(url)
            out_name = out_name.split('?')[0]
            print(out_name)
            out_file = os.path.join(out_dir, out_name)
            with open(out_file, 'wb') as f:
                f.write(img_bin)

    with open(complete_file, 'a') as f:
        f.write('\n'.join([item['media']['id'] for item in items]))
        f.write('\n')


def save_to_photo_app():
    img_dir = './downloads' 
    img_files = glob(os.path.join(img_dir, '*'))

    for img_file in img_files:
        if img_file.split('.')[-1] == 'jpg':
            photos.create_image_asset(img_file) 
            os.remove(img_file)


def main():
    download_img()
    save_to_photo_app()


if __name__=='__main__':
    main()
