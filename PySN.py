import math
import hmac
import json
import hashlib
import requests
from clint.textui import progress
import xml.etree.ElementTree as ET
from os import makedirs, path
#This is always a good sign:
requests.packages.urllib3.disable_warnings() 

loop = 'Y'

while(loop=='Y'):
    title_id = input('Enter Title ID: ').upper()
    key = bytearray.fromhex('E5E278AA1EE34082A088279C83F9BBC806821C52F2AB5D2B4ABD995450355114')
    id = bytes('np_' + title_id,'UTF-8')
    hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
    xml_url = ('https://gs-sec.ww.np.dl.playstation.net/pl/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
    var_url = requests.get(xml_url, stream = True, verify=False)
    #I'm sure there's a better way to handle Sony's weird certs.

    if var_url.status_code == 200:
        if var_url.text != '':
            root = ET.fromstring(var_url.content)
            name = (root.find('./tag/package/paramsfo/title').text).replace('\n',' ')
            for item in root.iter('titlepatch'):
                titleid = item.get('titleid')
           
            print('Found update(s) for: ' + titleid + ' ' + name)

            name = name.replace(':',' -').replace('/',' ').replace('?','')
            download_path = 'Updates/PlayStation Vita/' + titleid + ' ' + name

            for item in root.iter('package'):
                url = (item.get('url'))
                update_file = path.basename(url)
                update_size =int((requests.get(url, stream=True)).headers['Content-Length'])
                print(update_file)
                print('Size: ' + str(math.ceil(update_size/1024)) + 'KB')

            confirm = input('Would you like to download these updates? Y/N:').upper()
            if confirm == 'Y':
                if not path.exists(download_path):
                    makedirs(download_path)
                for item in root.iter('package'):
                    url = (item.get('url'))
                    r = requests.get(url, stream = True)
                    update_file = path.basename(url)
                    print('downloading ' + update_file)

                    with open(download_path + '/' + update_file,'wb') as f:
                        update_size =int(r.headers['Content-Length'])
                        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(update_size/1024) + 1): 
                            if chunk:
                                f.write(chunk)
                                f.flush()
                print('Finished.')                
        else: print('No updates available for this game.')

    else:
        xml_url = 'https://a0.ww.np.dl.playstation.net/tpl/np/' + title_id + '/' + title_id + '-ver.xml'
        var_url = requests.get(xml_url, stream = True, verify=False)

        if var_url.status_code == 200:
            if var_url.text != '':
                root = ET.fromstring(var_url.content)
                name = (root.find('./tag/package/paramsfo/TITLE').text).replace('\n',' ')
                for item in root.iter('titlepatch'):
                    titleid = item.get('titleid')
           
                print('Found update(s) for: ' + titleid + ' ' + name)

                name = name.replace(':',' -').replace('/',' ').replace('?','')
                download_path = ('Updates/PlayStation 3/' + titleid + ' ' + name)

                for item in root.iter('package'):
                    url = (item.get('url'))
                    update_file = path.basename(url)
                    update_size =int((requests.get(url, stream=True)).headers['Content-Length'])
                    print(update_file)
                    print('Size: ' + str(math.ceil(update_size/1024)) + 'KB')

                confirm = input('Would you like to download these updates? Y/N:').upper()
                if confirm == 'Y':
                    if not path.exists(download_path):
                        makedirs(download_path)
                    for item in root.iter('package'):
                        url = (item.get('url'))
                        r = requests.get(url, stream = True)
                        update_file = path.basename(url)
                        print('downloading ' + update_file)

                        with open(download_path + '/' + update_file,'wb') as f:
                            update_size =int(r.headers['Content-Length'])
                            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(update_size/1024) + 1): 
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                    print('Finished.')  
            else: print('No updates available for this game.')

        else:
            key = bytearray.fromhex('AD62E37F905E06BC19593142281C112CEC0E7EC3E97EFDCAEFCDBAAFA6378D84')
            hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
            xml_url = ('https://gs-sec.ww.np.dl.playstation.net/plo/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
            var_url = requests.get(xml_url, stream = True, verify=False)

            if var_url.status_code == 200:
                if var_url.text != '':
                    root = ET.fromstring(var_url.content)
                    name = (root.find('./tag/package/paramsfo/title').text).replace('\n',' ')
                    for item in root.iter('titlepatch'):
                        titleid = item.get('titleid')
           
                    print('Found update(s) for: ' + titleid + ' ' + name)

                    name = name.replace(':',' -').replace('/',' ').replace('?','')
                    download_path = ('Updates/PlayStation 4/' + titleid + ' ' + name)

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

                    confirm = input('Would you like to download these updates? Y/N:').upper()
                    if confirm == 'Y':
                        if not path.exists(download_path):
                            makedirs(download_path)
                        for item in root.iter('package'):
                            man_url = (item.get('manifest_url'))
                            json_url = requests.get(man_url, stream = True)
                            json_cont = json.loads(json_url.content)

                            for item in (json_cont['pieces']):
                                url = (item['url'])
                                r = requests.get(url, stream = True)
                                update_file = path.basename(url)
                                print('downloading ' + update_file)

                                with open(download_path + '/' + update_file,'wb') as f:
                                    update_size =int(r.headers['Content-Length'])
                                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(update_size/1024) + 1): 
                                        if chunk:
                                            f.write(chunk)
                                            f.flush()
                        print('Finished.')       
                else: print('No updates available for this game.')
            else: print('Invalid Title ID.')

    loop = input('Check for more updates? Y/N: ').upper()