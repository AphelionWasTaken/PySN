import customtkinter
import hmac
import json
import threading
import hashlib
import requests
import os
import queue
import yaml
import time
from fnmatch import fnmatch
from configparser import ConfigParser
import xml.etree.ElementTree as ET
from os import makedirs, path
from enum import Enum
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

#Checks if the download path already exists and if hashes match. Changes the buttons and status label accordingly.
def is_shit_there(self, download_path, index, fileloc, console, sha1):
    if path.exists(fileloc):
        hash = hashlib.sha1()
        hash_match = 1
        self.textbox.dlbutton_list[index].configure(text='Redownload')
        self.textbox.open_button_list[index].configure(text='Open', state='normal', command=lambda: self.open_loc(download_path))
        if sha1 != 'N/A':
            self.textbox.dlbutton_list[index].configure(state='disabled')
            self.textbox.open_button_list[index].configure(state='disabled')
            self.textbox.status_list[index].configure(text_color = 'yellow', text='Checking Hash...')
            with open(fileloc,'rb') as f:
                if console == 'PlayStation 3' or console == 'PlayStation Vita':
                    data = f.read()[:-32]
                else: data = f.read()
                hash.update(data)
                if sha1.upper() == (hash.hexdigest().upper()):
                    hash_match = 1
                else:
                    hash_match = 2
        self.textbox.dlbutton_list[index].configure(state='normal')
        self.textbox.open_button_list[index].configure(state='normal')
        return hash_match

#Creates a directory for the game in the download path.
def create_directories(download_path):
    if not path.exists(download_path):
        makedirs(download_path)
    return download_path


#Handles the config file.
class ConfigSettings():
    def __init__(self):
        super().__init__()

    #Gets settings from the config file.
    def get_config():
        config = ConfigParser()
        config.read('config.ini')
        save_dir = config.get('paths', 'downloads')
        rpcs3_dir = config.get('paths', 'RPCS3')
        return save_dir, rpcs3_dir

    #Saves the config file.
    def save_config(mode, save_dir , rpcs3_dir):
        config = ConfigParser()
        with open('config.ini', mode) as ini:
            config.add_section('paths')
            config.set('paths', 'downloads', save_dir)
            config.set('paths', 'RPCS3', rpcs3_dir)
            config.write(ini)

    #Checks for the config file, and gets the settings from it. Saves default config if none present.
    def check_config():
        normalized_path = os.getcwd().replace('\\','/')
        config_path = (normalized_path + '/config.ini')
        if path.exists(config_path):
            save_dir, rpcs3_dir = ConfigSettings.get_config()
        else:
            save_dir = (normalized_path + '/Updates/')
            rpcs3_dir = 'No Games.yml Location Set!'
            ConfigSettings.save_config('x', save_dir , rpcs3_dir)
        return save_dir, rpcs3_dir
    
save_dir, rpcs3_dir = ConfigSettings.check_config()


#Used to send messages to the queue
class ButtonAction(Enum):
    STOP = 1
    PAUSE = 2
    RESUME = 3


#Window with save and rpcs3/games.yml locations.
class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes('-topmost', 1)
        self.geometry('540x320')
        self.resizable(0,0)
        self.title('Settings')
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.temp_save, self.temp_rpcs3 = ConfigSettings.check_config()

        self.save_dir_label = customtkinter.CTkLabel(master=self, text='Download Update PKGs To This Folder:',justify = 'center', anchor='center')
        self.save_dir_label.grid(row=0, column=1, columnspan=4, padx=5, pady=(20,0), sticky='sew')

        self.save_dir_field = customtkinter.CTkTextbox(master=self, height=25, wrap='none')
        self.save_dir_field.grid(row=1, column=1, columnspan=3, padx=5, pady=(0,0), sticky='new')
        self.edit_button1 = customtkinter.CTkButton(master=self, width = 50, text='Edit', command = self.button_save_loc)
        self.edit_button1.grid(row=1, padx=5, pady=(0,0), column=4, sticky='new')

        self.rpcs3_dir_label = customtkinter.CTkLabel(master=self, text='Folder containing RPCS3:', anchor='center')
        self.rpcs3_dir_label.grid(row=2, column=1, columnspan=4, padx=0, pady=(0,0), sticky='sew')

        self.yaml_dir_field = customtkinter.CTkTextbox(master=self, height=25, width = 400, wrap='none')
        self.yaml_dir_field.grid(row=3, column=1, columnspan=3, padx=5, pady=(0,25), sticky='new')
        self.edit_button2 = customtkinter.CTkButton(master=self, width = 50, text='Edit', command = self.button_yml_loc)
        self.edit_button2.grid(row=3, padx=5, pady=(0,0), column=4, sticky='new')
        
        self.save_button = customtkinter.CTkButton(master=self, text='Save', width = 100,  command = self.button_save)
        self.save_button.grid(row=4, padx=(0,5), column=2, sticky='e')
        self.cancel_button = customtkinter.CTkButton(master=self, text='Cancel', width = 100, command=self.destroy)
        self.cancel_button.grid(row=4, padx=(5,135), column=3, columnspan=2, sticky='w')
       
        self.save_dir_field.insert('0.0',self.temp_save)
        self.save_dir_field.configure(state='disabled')
        self.yaml_dir_field.insert('0.0',self.temp_rpcs3)
        self.yaml_dir_field.configure(state='disabled')

    #Button to change update save location. Assigns the chosen path to a temporary variable and populates the text bar with it.
    def button_save_loc(self):
        temporary_temp = self.temp_save
        self.temp_save=customtkinter.filedialog.askdirectory(parent = self)
        if self.temp_save != '':
            self.save_dir_field.configure(state='normal')
            self.save_dir_field.delete('0.0','end')
            self.save_dir_field.insert('0.0', self.temp_save)
            self.save_dir_field.configure(state='disabled')
        else: self.temp_save = temporary_temp

    #Button to change rpcs3 location. Assigns the chosen path to a temporary variable and populates the text bar with it.
    def button_yml_loc(self):
        temporary_temp = self.temp_rpcs3
        self.temp_rpcs3=customtkinter.filedialog.askdirectory(parent = self)
        if self.temp_rpcs3 != '':
            self.yaml_dir_field.configure(state='normal')
            self.yaml_dir_field.delete('0.0','end')
            self.yaml_dir_field.insert('0.0', self.temp_rpcs3)
            self.yaml_dir_field.configure(state='disabled')
        else: self.temp_rpcs3 = temporary_temp

    #Save button. assigns the temp variables to global variables for the save directory.
    #Some handling to endure the directory is appended with a /.
    def button_save(self):
        global rpcs3_dir
        global save_dir
        if self.temp_save.endswith('/'):
            save_dir = self.temp_save
        else: 
            save_dir = self.temp_save + '/'
        if self.temp_rpcs3.endswith('!') or self.temp_rpcs3.endswith('/'):
            rpcs3_dir = self.temp_rpcs3
        else:
            rpcs3_dir = self.temp_rpcs3 + '/'
        ConfigSettings.save_config('w', save_dir , rpcs3_dir)
        self.destroy()


#Download All window. I did not create the downall function as part of this class for whatever reason...
class DownloadAllWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('400x240')
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.save_dir_label = customtkinter.CTkLabel(master=self, text='You are about to download all of the updates in the list!\n\n\nContinue?\n', anchor='center')
        self.save_dir_label.grid(row=1, column=2, columnspan=2, padx=20, pady=0, sticky='ew')

        self.only_new_check = customtkinter.CTkCheckBox(master=self, text="Only Download Updates That I Don't Have")
        self.only_new_check.grid(row=2, column=2, columnspan=2, padx=50, sticky='ew')

        self.save_button = customtkinter.CTkButton(master=self, width = 100, text='Okay')
        self.save_button.grid(row=4, padx=(55,5), column=2, sticky='e')

        self.cancel_button = customtkinter.CTkButton(master=self, width = 100, text='Cancel', command=self.destroy)
        self.cancel_button.grid(row=4, padx=(5,55), column=3, sticky='w')


#Frame where all the fun widgets go. This gets put inside the textbox.
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.command = command
        self.title_label_list = []
        self.size_label_list = []
        self.status_list = []
        self.queue_list = []
        self.dlbutton_list = []
        self.open_button_list = []
        self.prog_bar_list = []

    #Creates widgets within the frame, adds appropriate ones to the grid, then adds them to a list.
    def add_item(self, name, title_id, ver, url, console, update_size, sha1, index, download_path, fileloc):

        #Truncates the name depending on it's length. Assigns the title id, version, and name to a label on the left side of the frame.
        if len(title_id) == 2 and sha1 == 'N/A':
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name, anchor='w')
        elif ver.startswith(' D') and len(name)>9 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name[:9] + '...', anchor='w')
        elif len(name)>18 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name[:18] + '...', anchor='w') 
        elif len(name)<=18 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name, anchor='w')
        else:
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + name, anchor='center')
        
        #Creates labels for size and status, buttons for downloading and opening the file, a progress bar, and establishes the queue for threading.
        size = str(round((update_size/1024000),2)) + ' MB'
        size_label = customtkinter.CTkLabel(self, text=size, anchor='e', width = 70)
        status = customtkinter.CTkLabel(self, text='', anchor='e', width = 160)
        dlbutton = customtkinter.CTkButton(self, text='Download', width=100, height=24)
        open_button = customtkinter.CTkButton(self, text='Open', width=100, height=24, state = 'disabled')
        prog_bar = customtkinter.CTkProgressBar(self, width=440, height=5)
        prog_bar.set(0)
        q = queue.Queue()

        #Configures the buttons to take a command with appropriate variables. Places all of the widgets on the grid.
        if self.command is not None:
                dlbutton.configure(command=lambda: self.command(name, title_id, url, console, update_size, sha1, index, download_path, fileloc))
                open_button.configure(command=lambda: self.command(download_path, index, fileloc))
        if not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label.grid(row=len(self.title_label_list), column=0, pady=(0, 10), sticky='w')
            status.grid(row=len(self.title_label_list), column=2, pady=(0, 10),padx=(0, 0), sticky='e') 
            size_label.grid(row=len(self.title_label_list), column=3, padx=(10, 5), pady=(0, 10), sticky='e')
            prog_bar.grid(row=len(self.dlbutton_list), column=0, columnspan=3, pady=(15, 0), sticky='w')
            dlbutton.grid(row=len(self.dlbutton_list), column=4, pady=(0, 10), padx=0, sticky='e')
            open_button.grid(row=len(self.dlbutton_list), column=5, pady=(0, 10), padx=(0, 0), sticky='e')
        else:
            title_label.grid(row=len(self.title_label_list), column=0, columnspan=8, pady=(0, 10))

        #Appends the list of widgets, so that we can refer to them specifically later.    
        self.title_label_list.append(title_label)
        self.size_label_list.append(size_label)
        self.status_list.append(status)
        self.queue_list.append(q)
        self.dlbutton_list.append(dlbutton)
        self.open_button_list.append(open_button)
        self.prog_bar_list.append(prog_bar)

    #Iterates through the widgets looking for specific strings. If one is found, the whole line will be deleted.
    def clear_items(self):
        for title_label, size_label, status, dlbutton, open_button, prog_bar, q in zip(self.title_label_list, self.size_label_list, self.status_list, self.dlbutton_list, self.open_button_list, self.prog_bar_list, self.queue_list):
            if title_label.cget('text').startswith('Invalid ID') or title_label.cget('text').startswith('No updates available for'):
                title_label.destroy()
                size_label.destroy()
                status.destroy()
                dlbutton.destroy()
                open_button.destroy()
                prog_bar.destroy()
                self.title_label_list.remove(title_label)
                self.size_label_list.remove(size_label)
                self.status_list.remove(status)
                self.queue_list.remove(q)
                self.dlbutton_list.remove(dlbutton)
                self.open_button_list.remove(open_button)
                self.prog_bar_list.remove(prog_bar)


#Main window and some button functionality. Vaguely named widgets are in order of how they appear on screen.
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('760x640')
        self.title('PySN')
        self.resizable(0,0)
        self.toplevel_window = None
        self.stop_down = False
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.bind('<Return>', lambda event: self.button_search())
        
        self.entry = customtkinter.CTkEntry(master=self, placeholder_text='Enter Serial', width = 125)
        self.entry.grid(row=0, column=0, padx=(4,2), pady=(6,0), sticky='ew')
        self.combobox = customtkinter.CTkComboBox(master=self, values=['PlayStation 3', 'PlayStation 4', 'PlayStation Vita'], width = 125)
        self.combobox.grid(row=0, column=1, columnspan=1, padx=(2,2), pady=(6,0), sticky='ew')
        self.combobox.configure(state = 'readonly')
        self.checkbox = customtkinter.CTkCheckBox(master=self, text='Search Games.yml')
        self.checkbox.grid(row=0, column=2, columnspan=2, padx=(2,4), pady=(6,0), sticky='w')
        self.button1 = customtkinter.CTkButton(master=self, command=self.button_search, text='Search', width = 125)
        self.button1.grid(row=0, column=7, padx=4, pady=(6,0), sticky='ew')
        
        self.textbox = ScrollableLabelButtonFrame(master=self, height=540, command=self.frame_button_download, corner_radius=5)
        self.textbox.grid(row=1, column=0, columnspan=8, padx=4,  pady=(0,0), sticky='ew')

        self.button2 = customtkinter.CTkButton(master=self, command=self.button_downall, text='Download All', width = 125)
        self.button2.grid(row=2, column=0, padx=(4,2), pady=(0,6), sticky='ew')
        self.button3 = customtkinter.CTkButton(master=self, command=self.button_clear, text='Clear', width = 125)
        self.button3.grid(row=2, column=1, padx=(2,2), pady=(0,6), sticky='ew')
        self.clearbox = customtkinter.CTkCheckBox(master=self, text='Clear List On Search')
        self.clearbox.grid(row=2, column=2, columnspan=2, padx=(2,4), pady=(0,6), sticky='w')
        self.clearbox.select()
        self.button4 = customtkinter.CTkButton(master=self, command=self.button_settings, text='Settings', width = 125 )
        self.button4.grid(row=2, column=7, padx=4, pady=(0,6), sticky='ew')
    
    #Opens the file location. Used with the open button.
    def open_loc(self, download_path):
        customtkinter.filedialog.askopenfilenames(initialdir=download_path)

    #If the "search games.yml" box is not checked, assign the title id and console based on the users input, the search. If the console is PS3, search for DRM-free updates too.
    #If the "search games.yml" box is checked, automatically assign the console to PS3, and search for each title id on the games.yml.
    def search_type(self):
        if self.checkbox.get() == 0:
            title_id = (self.entry.get()).upper()
            console = self.combobox.get()
            if title_id.upper() == 'FIRMWARE' or title_id.upper() == 'FW':
                self.search_fw(title_id, console)
            else:
                self.search(title_id, console)
                if console == 'PlayStation 3':
                    self.search_no_drm(title_id, console)
        else:
            console = 'PlayStation 3'
            with open(rpcs3_dir+'config/games.yml', 'r') as f:
                file = yaml.safe_load(f)
                alist = list(file)
                for index in alist:
                    title_id = index
                    self.search(title_id, console)
                    self.search_no_drm(title_id, console)  

    #Assigns hashes and urls based on console and title id, checks if the url is valid, returns the xml and game name.
    def request_update(self, title_id, console):
        root = 0
        id = bytes('np_' + title_id, 'UTF-8')

        if console == 'PlayStation Vita':
            key = bytearray.fromhex('E5E278AA1EE34082A088279C83F9BBC806821C52F2AB5D2B4ABD995450355114')
            hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
            xml_url = ('https://gs-sec.ww.np.dl.playstation.net/pl/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
        elif console == 'PlayStation 4':
            key = bytearray.fromhex('AD62E37F905E06BC19593142281C112CEC0E7EC3E97EFDCAEFCDBAAFA6378D84')
            hash = (hmac.new(key, id, hashlib.sha256).hexdigest())
            xml_url = ('https://gs-sec.ww.np.dl.playstation.net/plo/np/' + title_id + '/' + hash + '/' + title_id + '-ver.xml')
        else:
            xml_url = 'https://a0.ww.np.dl.playstation.net/tpl/np/' + title_id + '/' + title_id + '-ver.xml'
        var_url = requests.get(xml_url, stream = True, verify=False)
        
        if var_url.status_code == 200 and var_url.text != '':
            root = ET.fromstring(var_url.content)
            name = (root.find('./tag/package/paramsfo/').text).replace('\n', ' ')
            for item in root.iter('titlepatch'):
                title_id = item.get('titleid')
        elif var_url.status_code == 200 and var_url.text == '':
            name = 'No updates available for this game'
        else:
            name = 'Invalid ID'
        
        return root, name
                
    #Requests game/update info and creates widgets in the frame based on that info.
    def search(self, title_id, console):
        root, game_name = self.request_update(title_id, console)

        #If the xml exists, iterate through the package element to get info about the update. If it's a PS4 title, load and iterate through the JSON for data.
        if root != 0:
            for item in root.iter('package'):
                index = len(self.textbox.dlbutton_list)
                ver = (item.get('version'))
                if console == 'PlayStation 4':
                    man_url = (item.get('manifest_url'))
                    json_url = requests.get(man_url, stream = True)
                    json_cont = json.loads(json_url.content)
                    for item in (json_cont['pieces']):
                        url = (item.get('url'))
                        sha1 = (item.get('hashValue'))
                        update_size = (item.get('fileSize'))
                else:        
                    url = (item.get('url'))
                    sha1 = (item.get('sha1sum'))
                    update_size = int((item.get('size')))

                #Assign a download path with some handling for odd characters in the game name. Add Widgets to the textbox and check if the file already exists.
                name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '').strip()
                download_path = save_dir + console + '/' + title_id + ' ' + name
                update_file = path.basename(url)
                fileloc = (download_path + '/' + update_file) 
                self.textbox.add_item(game_name, title_id, ' v' + ver, url, console, update_size, sha1, index, download_path, fileloc)
                
                #Check the hash in case an incomplete or corrupt file already exists. Then handle errors in search results.
                hash_match = is_shit_there(self, download_path, index, fileloc, console, sha1)
                if hash_match == 1:
                    self.textbox.status_list[index].configure(text_color = 'green', text='Already Owned!')
                elif hash_match == 2:
                    self.textbox.status_list[index].configure(text_color = 'red', text='HASH MISMATCH DETECTED!')
                else: pass               
        elif game_name == 'Invalid ID': 
            self.textbox.add_item('Invalid ID: ' + title_id, '', '', '', '', 0, '', '', '', '')
        else: self.textbox.add_item('No updates available for ' + title_id, '', '', '', '', 0, '', '', '', '')

    #Searches specifically for PS3 DRM-free update info, and populates the widgets in the frame based on that info.
    def search_no_drm(self, title_id, console):
        root, game_name = self.request_update(title_id, console)
        
        #If the XML exists, make sure that there is a URL element before continuing.
        if root != 0:
            drm_free_check = False
            element_list = root.findall('.//')
            if fnmatch(str(element_list),'*url*') == True:
                drm_free_check = True

            #If a URL element is found, create a list for the elements.
            if drm_free_check == True:
                i=0
                package_list = []
                index_list = []
                drmfree_list = []
                sha1_list = []
                update_size_list = []
                name_list = []
                url_list = []
            
                #Append lists with version info from the package element, and update info from the URL element.
                #Then iterate through the lists for the download path and widget info. Also places widgets in the textbox.
                for item in root.iter('package'):
                    package_list.append(item.get('version'))
                for item in root.iter('url'):
                    drmfree_list.append(root.get('url'))
                    url_list.append(item.get('url'))                
                    sha1_list.append(item.get('sha1sum'))
                    update_size_list.append(int((item.get('size'))))
                    name_list.append(game_name.replace(':', ' -').replace('/', ' ').replace('?', '').strip())         
                for version in package_list:
                    download_path = (save_dir + console + '/' + title_id + ' ' + name_list[i])
                    update_file = 'DRM-Free ' + path.basename(url_list[i])
                    fileloc = (download_path + '/' + update_file)
                    index_list.append(len(self.textbox.dlbutton_list))
                    self.textbox.add_item(game_name, title_id, ' DRM-Free v' + version, url_list[i], console, update_size_list[i], sha1_list[i], index_list[i], download_path, fileloc)
                    
                    #Check the hash in case an incomplete or corrupt file already exists. Errors in search results are handled by the other search, so we just pass here.
                    hash_match = is_shit_there(self, download_path, index_list[i], fileloc, console, sha1_list[i])
                    if hash_match == 1:
                        self.textbox.status_list[index_list[i]].configure(text_color = 'green', text='Already Owned!')
                    elif hash_match == 2:
                        self.textbox.status_list[index_list[i]].configure(text_color = 'red', text='HASH MISMATCH DETECTED!')
                    else: pass  
                    i = i+1
            else: pass
        else: pass
    
    #Searches for firmware info, and populates the widgets in the frame based on that info.
    def search_fw(self, title_id, console):
        
        #Set the game name so it shows up nicely in the UI. Establish a list of known firmware locales.
        if console == 'PlayStation Vita':
            locale_list = ['us', 'eu', 'jp', 'kr', 'uk', 'mx', 'au', 'sa', 'tw', 'ru', 'cn']
        else:
            locale_list = ['us', 'eu', 'jp', 'kr', 'uk', 'mx', 'au', 'sa', 'tw', 'ru', 'cn', 'br']

        #if the console is PS3, split the text in the text file by ; and pull strings that match certain criteria.
        if console == 'PlayStation 3':
            for locale in locale_list:
                txt_url = 'http://f' + locale + '01.ps3.update.playstation.net/update/ps3/list/' + locale + '/ps3-updatelist.txt'
                var_url = requests.get(txt_url, stream = True, verify=False)
                if var_url.status_code == 200 and var_url.text != '':
                    soup = BeautifulSoup(var_url.text, 'html.parser')
                    text = soup.string.split(';')
                    for item in text:
                        if fnmatch(str(item),'*CompatibleSystemSoftwareVersion*') == True:
                            ver = item[32:36]
                        if fnmatch(str(item),'*# *') == True:
                            region = item[2:4].upper()
                        if fnmatch(str(item),'*UPDAT.PUP') == True:
                            url = item[4:]
                            update_url = requests.get(url, stream=True)
                            update_size = int(update_url.headers.get('Content-Length'))  

                #There's no hash to check, so sha1 gets assigned N/A. Title ID becomes region for formatting. set paths and populate widgets.
                sha1 = 'N/A'
                index = len(self.textbox.dlbutton_list)
                title_id = region
                game_name = console + ' Firmware'
                download_path = save_dir + console + '/' + game_name + '/' + region
                update_file = 'v' + ver + ' ' + path.basename(url)
                fileloc = (download_path + '/' + update_file) 
                self.textbox.add_item(game_name, title_id, ' v' + ver, url, console, update_size, sha1, index, download_path, fileloc)
        
        #if the console is PS4 or Vita, we can parse through some XML.
        else:
            update_size_list = []
            url_list = []
            ver_list = []
            index_list = []
            region_list = []
            update_data_list = []
            i=0

            #Gets XML and parses through certain elements to populate the lists above.
            for locale in locale_list:
                if console == 'PlayStation Vita':
                    xml_url = 'http://f' + locale + '01.psp2.update.playstation.net/update/psp2/list/' + locale + '/psp2-updatelist.xml'
                else:
                    xml_url = 'http://f' + locale + '01.ps4.update.playstation.net/update/ps4/list/' + locale + '/ps4-updatelist.xml'
                var_url = requests.get(xml_url, stream = True, verify=False)
                root = ET.fromstring(var_url.content)
                for item in root.iter('image'):
                    update_size_list.append(int(item.get('size')))
                    url_list.append((''.join(item.itertext())[:-8].strip()))
                    for item in root.iter('region'):
                        region_list.append(item.get('id').upper())
                    
                    if console == 'PlayStation Vita':   
                        for item in root.iter('version'):
                            ver_list.append(item.get('label'))
                        for item in root.iter('update_data'):
                            update_data_list.append(item.get('update_type'))
                        for item in root.iter('recovery'):
                            update_data_list.append(item.get('spkg_type'))
                    else:
                        for item in root.iter('system_pup'):
                            ver_list.append(item.get('label'))
                        for item in root.iter('update_data'):
                            update_data_list.append(item.get('update_type'))
                        for item in root.iter('recovery_pup'):
                            update_data_list.append(item.get('type'))

            #Do some renaming so we know what we're actually looking at in the UI.
            for url in url_list:
                if update_data_list[i] == 'full':
                    update_data_list[i] = 'Firmware'
                elif update_data_list[i] == 'systemdata':
                    update_data_list[i] = 'Fonts'
                elif update_data_list[i] == 'preinst':
                    update_data_list[i] = 'Preinst'
                elif update_data_list[i] == 'default':
                    update_data_list[i] = 'Recovery'

                #Assign hash to N/A, assign title_id to region and make the game name look nice.
                sha1 = 'N/A'
                index_list.append(len(self.textbox.dlbutton_list))
                title_id = region_list[i]
                game_name = console + ' ' + update_data_list[i]
                download_path = save_dir + console + '/' + console + ' Firmware' + '/' + region_list[i]
                update_file = 'v' + ver_list[i] + ' ' + update_data_list[i] + ' ' + path.basename(url)
                fileloc = (download_path + '/' + update_file)
                self.textbox.add_item(game_name, title_id, ' v' + ver_list[i], url, console, update_size_list[i], sha1, index_list[i], download_path, fileloc)
                i = i+1

    #Pauses and resumes download and sends pause message to the queue.
    def toggle_pause(self, index):
        if self.textbox.dlbutton_list[index].cget('text') == 'Pause':
            self.textbox.dlbutton_list[index].configure(text='Resume')
            self.textbox.queue_list[index].put(ButtonAction.PAUSE)
        else:
            self.textbox.dlbutton_list[index].configure(text='Pause')
            self.textbox.queue_list[index].put(ButtonAction.RESUME)

    #Cancels download and sends stop message to the queue.
    def cancel(self, index):
        self.textbox.dlbutton_list[index].configure(text='Download')
        self.textbox.queue_list[index].put(ButtonAction.STOP)
    
    #Creates directories, updates buttons, downloads the update file, and checks the hash.
    def download_updates(self, url, download_path, size, sha1, index, title_id, name, console, fileloc, sem):
        with sem:
            if path.exists(download_path) == False:
                create_directories(download_path)
            self.textbox.dlbutton_list[index].configure(text='Pause', command=lambda: self.toggle_pause(index))
            self.textbox.open_button_list[index].configure(text='Cancel', state = 'normal', command=lambda: self.cancel(index))
            i=0
            h=0

            #send a request to the update files URL. Handle threads and download behavior based on the button state.
            with requests.get(url, stream = True) as r:
                r.raise_for_status()
                with open(fileloc,'wb') as f:
                    while True:
                        try:
                            action = self.textbox.queue_list[index].get_nowait()
                            if action == ButtonAction.PAUSE:
                                self.textbox.status_list[index].configure(text_color = 'yellow', text='Paused')
                                new_action = self.textbox.queue_list[index].get()
                                if new_action == ButtonAction.RESUME:
                                    self.textbox.status_list[index].configure(text_color = 'green', text='Downloading')
                                    continue
                                elif new_action == ButtonAction.STOP:
                                    self.textbox.status_list[index].configure(text_color = 'red', text='Download Cancelled!')
                                    break
                            elif action == ButtonAction.STOP:
                                self.textbox.status_list[index].configure(text_color = 'red', text='Download Cancelled!')
                                break
                        except queue.Empty:
                            pass
                        
                        #Download the file and update the progress bar and status label based on how much has downloaded.
                        for chunk in r.iter_content(chunk_size=(1024*1024)):
                            if chunk:
                                f.write(chunk)
                                f.flush()
                                i = i+(1/(size/(1024*1024)))
                                h = round(h+((1024*1024)/1024000),2)
                                self.textbox.prog_bar_list[index].set(i)
                                self.textbox.status_list[index].configure(text_color = 'green', text= str(h) + '/' + str(round((size/1024000),2)) + 'MB' )
                            if self.textbox.queue_list[index].empty() == False: break
                        else: break

            #After the file is downloaded, reconfigure the dl and open button behavior.
            #Then remove the file if the dl was cancelled. If it completed, run is_shit_there to check the hash and configure buttons properly.
            self.textbox.dlbutton_list[index].configure(command=lambda: App.frame_button_download(self, name, title_id, url, console, size, sha1, index, download_path, fileloc))
            self.textbox.open_button_list[index].configure(text='Open', state = 'disabled', command=lambda: None)            
            if self.textbox.status_list[index].cget('text') == 'Download Cancelled!':
                os.remove(fileloc)
            else:
                hash_match = is_shit_there(self, download_path, index, fileloc, console, sha1)
                if hash_match == 1:
                    self.textbox.status_list[index].configure(text_color = 'green', text='Download Complete!')
                elif hash_match == 2:
                    self.textbox.status_list[index].configure(text_color = 'red', text='HASH MISMATCH DETECTED!')
                else: pass

    #Downloads all files, or only new files based on the check box in the downall window. Pretty sure it belongs in the DownloadAllWindow class.
    def downall(self):
        self.toplevel_window.destroy()
        if self.toplevel_window.only_new_check.get() == 0:
            for item in self.textbox.dlbutton_list:
                item.invoke()
        else:
            for item in self.textbox.dlbutton_list:
                if item.cget('text') == 'Download':
                    item.invoke()

    #If you want to clear the frame on each search, the search button will destroy it and recreate it, then search.
    #Otherwise it will clear error labels such as 'Invalid ID' before appending the list.
    def button_search(self):
        if self.clearbox.get() == 1:
            self.textbox.destroy()
            self.textbox = ScrollableLabelButtonFrame(master=self, height=540, command=self.frame_button_download, corner_radius=5)
            self.textbox.grid(row=1, column=0, columnspan=8, padx=4, pady=0, sticky='ew')
            self.search_type()
        else:
            self.textbox.clear_items()
            self.search_type()

    #Behavior for the Download button.
    def frame_button_download(self, game_name, title_id, url, console, update_size, sha1, index, download_path, fileloc):
        semaphore = threading.Semaphore(2)
        threading.Thread(target = self.download_updates, args=(url, download_path, update_size, sha1, index, title_id, game_name, console, fileloc, semaphore), daemon = True).start()
        time.sleep(.001)
        

    #Behavior for the Download All button. Opens the download all window.
    def button_downall(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DownloadAllWindow(self)  # create window if it's None or destroyed
            self.toplevel_window.title('Download')
            self.toplevel_window.resizable(0,0)
            self.toplevel_window.attributes('-topmost', 1)
            self.toplevel_window.save_button.configure(command=self.downall)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    #Behavior for the Clear button. Clears the list.            
    def button_clear(self):
        self.textbox.destroy()
        self.textbox = ScrollableLabelButtonFrame(master=self, height=540, command=self.frame_button_download, corner_radius=5)
        self.textbox.grid(row=1, column=0, columnspan=8, padx=4, pady=0, sticky='ew')

    #Behavior for the Settings button. Opens the settings window.
    def button_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SettingsWindow(self)
        else:
            self.toplevel_window.focus()


if __name__ == '__main__':
    app = App()
    app.mainloop()
