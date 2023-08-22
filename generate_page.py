import shutil
import json
import sys
import os
import re
import htmlmin
from PIL import Image
from bs4 import BeautifulSoup as bs
from colorama import Fore, Style

TEMPLATE_PATH = 'template_source/template.html'
CONTENT_PATH = 'content'
OUT_PATH = 'out'
COL_RED = Fore.RED
COL_GREEN = Fore.GREEN
COL_NONE = Style.RESET_ALL

def convert_images(name, mod_info):
    print('Converting images to JPEG...', end='\0')
    # Banner
    banner = mod_info['banner']
    old_banner = Image.open(f'{CONTENT_PATH}/{name}/{banner}')
    old_banner = old_banner.convert('RGB')
    new_banner = old_banner.resize((852, 426))
    new_banner.save(f'{OUT_PATH}/{name}/banner.jpg', quality=75)

    # Screenshots
    i = 0
    for j in mod_info['screenshots']:
        shot = Image.open(f'{CONTENT_PATH}/{name}/{j}')
        shot = shot.convert('RGB')
        new_shot = shot.resize((852, 480))
        new_shot.save(f'{OUT_PATH}/{name}/shot_{i}.jpg', quality=50)
        i += 1
    print('OK')

def modify_html(name, mod_info):
    print('Inserting attributes into HTML...', end='\0')
    with open(f'{OUT_PATH}/{name}/index.html', 'r') as document:
        soup = bs(document, 'html.parser')

    mod_name = mod_info['mod_info']['title']
    mod_subtitle = mod_info['mod_info']['subtitle']
    mod_desc = mod_info['mod_info']['description']
    mod_game = mod_info['mod_info']['game']
    download = mod_info['download_name']

    # Page Title : PAGE_TITLE
    html_title = soup.find('title')
    html_title.find(string=re.compile('PAGE_TITLE')).replace_with(f'{mod_name} - CoD Map Pool')
    # Game Name : GAME_CONTENT_NAME
    html_name = soup.find('div', {'class':'banner_txt'})
    html_name.find(string=re.compile('GAME_CONTENT_NAME')).replace_with(f'{mod_name}')
    # Game Subtitle : GAME_CONTENT_SUBTITLE
    html_subtitle = soup.find('p', {'class':'content_subtitle'})
    html_subtitle.find(string=re.compile('GAME_CONTENT_SUBTITLE')).replace_with(f'{mod_subtitle}')  
    # Game Description : GAME_CONTENT_DESCRIPTION
    html_desc = soup.find('p', {'class':'content_description'})
    html_desc.find(string=re.compile('GAME_CONTENT_DESCRIPTION')).replace_with(f'{mod_desc}')
    # Download Link : GAME_DOWNLOAD
    html_download = soup.find('a', {'class':'content_download'})
    html_download['href'] = f'https://archive.org/download/{download}'
    # Mod for Game : GAME_NAME
    html_game = soup.find('p', {'class':'content_game'})
    html_game.find(string=re.compile('GAME_NAME')).replace_with(f'{mod_game}')

    # Insert screenshots
    html_screens = soup.find('div', {'class':'content_gallery'})
    i = len(mod_info['screenshots']) - 1
    for j in mod_info['screenshots']:
        html_screens.insert(1, f'<div class="content_screenshot"><img src="shot_{i}.jpg"/></div>')
        i -= 1

    with open(f'{OUT_PATH}/{name}/index.html', 'w') as document:
        mini = htmlmin.minify(soup.prettify(formatter=None), remove_empty_space=True)
        document.write(mini)
    print('OK')

def setup_directory(name):
    try:
        os.mkdir(f'{OUT_PATH}')
    except FileExistsError:
        pass

    try:
        os.mkdir(f'{OUT_PATH}/{name}')
    except FileExistsError:
        shutil.rmtree(f'{OUT_PATH}/{name}/')
        os.mkdir(f'{OUT_PATH}/{name}')
    shutil.copyfile(f'{TEMPLATE_PATH}', f'{OUT_PATH}/{name}/index.html')

def write_out(mod_info):
    with open('out.txt', 'w') as out_file:
        title = mod_info['mod_info']['title']
        subtitle = mod_info['mod_info']['subtitle']
        out_file.write(f'{title}+{subtitle}')

def main():
    cont_name = sys.argv[1]
    try:
        json_file = f'{CONTENT_PATH}/{cont_name}/{cont_name}.json'
    except IndexError:
        print(f'{COL_RED}Error{COL_NONE}: No content specified. Aborting.')
        sys.exit()

    with open(json_file, 'r') as json_data:
        mod_info = json.load(json_data)

    setup_directory(cont_name)
    convert_images(cont_name, mod_info)
    modify_html(cont_name, mod_info)
    write_out(mod_info)
    print(f'{COL_GREEN}Done!{COL_NONE} Wrote out info to out.txt for building the index 😃')
    sys.exit()

if __name__ == '__main__':
    main()