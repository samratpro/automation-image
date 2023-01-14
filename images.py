"""
!pip install pillow
!pip install pytest-shutil
!pip install pyunsplash
!pip install pexels_api
!pip install bing_image_downloader
"""

import shutil
from PIL import Image
from pyunsplash import PyUnsplash
from bing_image_downloader import downloader
from pexels_api import API
import requests
import json
import base64
import os

website_name = ""
Username = ""
App_pass = ""
status = "" 

# Unsplash
unsplash_api = ''  # https://unsplash.com/developers
def unsplash_image_operation_un(command):
  if not os.path.exists('img'):
    os.makedirs('img')
  try:
    pu = PyUnsplash(api_key=unsplash_api)
    photos = pu.photos(type_='random', count=1, featured=True, query=command)
    [photo] = photos.entries
    headers_fox = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    response = requests.get(photo.link_download, stream=True, headers=headers_fox)
    local_file = open('img/' + command + '.jpg', 'wb')
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, local_file)
    im = Image.open('img/' + command + '.jpg')
    resized_im = im.resize((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    resized_im.save('img/' + command + '.jpg')
  except:
    pass

# Pixabay
pixabay_api = "" # https://pixabay.com/api/docs/
def pixabay_image_operation(command):
  if not os.path.exists('img'):
    os.makedirs('img')
  try:
    image_list = requests.get(f'https://pixabay.com/api/?key={pixabay_api}&q={command.replace(" ","+")}&image_type=photo&pretty=true')
    img_soup = image_list.json()['hits']
    img_list = []
    for x in img_soup:
      img_list.append(x['webformatURL'])
    if len(img_list) > 5:
      img_choice = choice([0,1,2,3,4,5])
    else:
      img_choice = 0
    headers_fox = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    response = requests.get(img_list[img_choice], stream=True, headers=headers_fox)
    local_file = open('img/' + command + '.jpg', 'wb')
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, local_file)
    im = Image.open('img/' + command + '.jpg')
    resized_im = im.resize((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    resized_im.save('img/' + command + '.jpg')
  except:
    pass
  
# Bing
def bing_image_operation(command):
  try:
    os.mkdir('img')
  except FileExistsError:
    pass
  try:
    downloader.download(command, limit=1, output_dir='img', filter='.jpg' )
    try:
      im = Image.open('img/'+command+'/Image_1.jpg')
    except:
      try:
        im = Image.open('img/'+command+'/Image_1.png')
      except:
        im = Image.open('img/'+command+'/Image_1.JPEG')

    resized_im = im.resize((round(im.size[0] * 0.8), round(im.size[1] * 0.8)))
    resized_im.save('img/'+command+'.jpg')
  except:
    pass
  

# pexels
pexels_api = ""  # https://www.pexels.com/api/
def pexels_image_operation(command):
  if not os.path.exists('img'):
    os.makedirs('img')
  try:  
    api = API(pexels_api)
    api.search(command, page=1, results_per_page=1)
    photos = api.get_entries()
    photo_list = list()
    for photo in photos:
        photo = photo.original
        photo_list.append(photo)
    if len(photo_list) > 0:
      headers_fox = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
      response = requests.get(photo_list[0], stream=True, headers=headers_fox)
      local_file = open('img/' + command + '.jpg', 'wb')
      response.raw.decode_content = True
      shutil.copyfileobj(response.raw, local_file)
      im = Image.open('img/' + command + '.jpg')
      resized_im = im.resize((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
      resized_im.save('img/' + command + '.jpg')
  except:
    pass
  
  
# Body Image 
def body_img(command):
  pexels_image_operation(command) # Change here, which option you want
  try:
    media = {'file': open('img/' + command + '.jpg', 'rb')}
    image = requests.post(json_url + '/media', headers=headers, files=media)
    image_title = command.replace('-', ' ').split('.')[0]
    post_id = str(json.loads(image.content.decode('utf-8'))['id'])
    source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
    image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
    image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
    image3 = '<!-- /wp:image -->'
    image_wp = image1 + image2 + image3
    return image_wp
  except:
    image_wp = ''
    return image_wp

  
# Feature image
def feature_image(command):
  image_operation(command)
  try:
      media = {'file': open('img/' + command + '.jpg', 'rb')}
      image = requests.post(json_url + '/media', headers=headers, files=media)
      image_wp = str(json.loads(image.content.decode('utf-8'))['id'])
      return image_wp
  except:
    image_wp = 0
    return image_wp
