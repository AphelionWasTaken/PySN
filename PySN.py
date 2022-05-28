import hmac
import hashlib
import requests
import xml.etree.ElementTree as ET
from os.path import basename
requests.packages.urllib3.disable_warnings() 

loop = 'Y'

while(loop=='Y'):
    title_id = input('Enter Title ID: ')

    key = bytearray.fromhex('E5E278AA1EE34082A088279C83F9BBC806821C52F2AB5D2B4ABD995450355114')

    id = bytes('np_' + title_id,'UTF-8')

    hash = (hmac.new(key, id, hashlib.sha256).hexdigest())

    xml_url = ('https://gs-sec.ww.np.dl.playstation.net/pl/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')

    var_url = requests.get(xml_url, verify=False)
    if var_url.status_code == 200:
        if var_url.text != '':
            root = ET.fromstring(var_url.content)
            for item in root.iter('package'):
                url = (item.get('url'))
                update_file = basename(url)
                print('downloading ' + update_file)
                open(update_file,'wb').write(requests.get(url).content)
            print('Finished.')
        else: print('No updates available for this game.')
    else: print('Invalid Title ID')

    loop = input('Check for more updates? Y/N: ')
