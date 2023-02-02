import sys
import math
import hmac
import json
import hashlib
import requests
import xml.etree.ElementTree as ET
from os import makedirs, path
from clint.textui import progress
requests.packages.urllib3.disable_warnings() 

def graceful_exit():
    confirm = input('\nWould you like to search for more updates? Y/N: ').upper()
    if confirm == 'N':
        sys.exit()
    elif confirm == 'Y':
        print('')
        return main()
    else:
        print ('\nInvalid input')
        return graceful_exit()

def request_ps3_update(title_id):
    xml_url = 'https://a0.ww.np.dl.playstation.net/tpl/np/' + title_id + '/' + title_id + '-ver.xml'
    var_url = requests.get(xml_url, stream = True, verify=False)
    if var_url.status_code == 200 and var_url.text != '':
        root = ET.fromstring(var_url.content)
        name = (root.find('./tag/package/paramsfo/TITLE').text).replace('\n', ' ')
        for item in root.iter('titlepatch'):
            titleid = item.get('titleid')  
        print('\nFound update(s) for: ' + titleid + ' ' + name +'\n')
    elif var_url.status_code == 200 and var_url.text == '':
        print ('\nNo updates available for this game')
        return graceful_exit()
    else:
        print ('\nInvalid ID')
        return graceful_exit()
    return root, name

def request_ps4_update(title_id):
    id = bytes('np_' + title_id, 'UTF-8')
    key = bytearray.fromhex('AD62E37F905E06BC19593142281C112CEC0E7EC3E97EFDCAEFCDBAAFA6378D84')
    hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
    xml_url = ('https://gs-sec.ww.np.dl.playstation.net/plo/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
    var_url = requests.get(xml_url, stream = True, verify=False)
    if var_url.status_code == 200 and var_url.text != '':
        root = ET.fromstring(var_url.content)
        name = (root.find('./tag/package/paramsfo/title').text).replace('\n', ' ')
        for item in root.iter('titlepatch'):
            titleid = item.get('titleid')  
        print('\nFound update(s) for: ' + titleid + ' ' + name + '\n')
    elif var_url.status_code == 200 and var_url.text == '':
        print ('\nNo updates available for this game')
        return graceful_exit()
    else:
        print ('\nInvalid ID')
        return graceful_exit()
    return root, name

def request_vita_update(title_id):
    id = bytes('np_' + title_id, 'UTF-8')
    key = bytearray.fromhex('E5E278AA1EE34082A088279C83F9BBC806821C52F2AB5D2B4ABD995450355114')
    hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
    xml_url = ('https://gs-sec.ww.np.dl.playstation.net/pl/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
    var_url = requests.get(xml_url, stream = True, verify=False)
    if var_url.status_code == 200 and var_url.text != '':
        root = ET.fromstring(var_url.content)
        name = (root.find('./tag/package/paramsfo/title').text).replace('\n', ' ')
        for item in root.iter('titlepatch'):
            titleid = item.get('titleid')  
        print('\nFound update(s) for: ' + titleid + ' ' + name + '\n')
    elif var_url.status_code == 200 and var_url.text == '':
        print ('\nNo updates available for this game')
        return graceful_exit()
    else:
        print ('\nInvalid ID')
        return graceful_exit()
    return root, name

def list_vita_ps3_updates(root):
    for item in root.iter('package'):
        url = (item.get('url'))
        update_file = path.basename(url)
        update_size =int((requests.get(url, stream=True)).headers['Content-Length'])
        print(update_file)
        print('Size: ' + str(math.ceil(update_size/1024)) + 'KB')

def list_ps4_updates(root):
    for item in root.iter('package'):
        man_url = (item.get('manifest_url'))
        json_url = requests.get(man_url, stream = True)
        json_cont = json.loads(json_url.content)
        for item in (json_cont['pieces']):
            url = (item['url'])
            update_size = int((requests.get(url, stream=True)).headers['Content-Length'])
            update_file = path.basename(url)
            print(update_file)
            print('Size: ' + str(math.ceil(update_size/1024)) + 'KB')

def create_ps3_directories(game_id, game_name):
    name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '')
    confirm = input('\nDownload all update files? Y/N: ').upper()
    if confirm == 'Y':
        print('')
        download_path = 'Updates/PlayStation 3/' + game_id + ' ' + name
    else:
        return graceful_exit()
    if not path.exists(download_path):
        makedirs(download_path)
    return download_path

def create_ps4_directories(game_id, game_name):
    name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '')
    confirm = input('\nDownload all update files? Y/N: ').upper()
    if confirm == 'Y':
        print('')
        download_path = 'Updates/PlayStation 4/' + game_id + ' ' + name
    else:
        return graceful_exit()
    if not path.exists(download_path):
        makedirs(download_path)
    return download_path

def create_vita_directories(game_id, game_name):
    name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '')
    confirm = input('\nDownload all update files? Y/N: ').upper()
    if confirm == 'Y':
        print('')
        download_path = 'Updates/PlayStation Vita/' + game_id + ' ' + name
    else:
        return graceful_exit()
    if not path.exists(download_path):
        makedirs(download_path)
    return download_path

def download_vita_ps3_updates(root, download_path):
    for item in root.iter('package'):
        url = (item.get('url'))
        r = requests.get(url, stream = True)
        update_file = path.basename(url)
        print('Downloading ' + update_file)
        with open(download_path + '/' + update_file,'wb') as f:
            update_size =int(r.headers['Content-Length'])
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(update_size/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    print('\nDownload(s) complete!')
    return graceful_exit()

def download_ps4_updates(root, download_path):
    for item in root.iter('package'):
        man_url = (item.get('manifest_url'))
        json_url = requests.get(man_url, stream = True)
        json_cont = json.loads(json_url.content)
        for item in (json_cont['pieces']):
            url = (item['url'])
            r = requests.get(url, stream = True)
            update_file = path.basename(url)
            print('Downloading ' + update_file)
            with open(download_path + '/' + update_file,'wb') as f:
                update_size =int(r.headers['Content-Length'])
                for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(update_size/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
    print('\nDownload(s) complete!')
    return graceful_exit()

def main():
    title_id = input('Enter Title ID: ').upper()
    if title_id.startswith(('NP', 'BC', 'BL')):
        root, game_name = request_ps3_update(title_id)
        list_vita_ps3_updates(root)
        download_path = create_ps3_directories(title_id, game_name)
        download_vita_ps3_updates(root, download_path)
    elif title_id.startswith('CUSA'):
        root, game_name = request_ps4_update(title_id)
        list_ps4_updates(root)
        download_path = create_ps4_directories(title_id, game_name)
        download_ps4_updates(root, download_path)
    elif title_id.startswith('PC'):
        root, game_name = request_vita_update(title_id)
        list_vita_ps3_updates(root)
        download_path = create_vita_directories(title_id, game_name)
        download_vita_ps3_updates(root, download_path)
    else:
        print ('\nInvalid ID')
        return graceful_exit() 
    
main()
