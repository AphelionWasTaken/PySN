import customtkinter
import hmac
import json
import threading
import hashlib
import requests
import os
import queue
import yaml
from configparser import ConfigParser
import xml.etree.ElementTree as ET
from os import makedirs, path
from enum import Enum

requests.packages.urllib3.disable_warnings()

#checks if the download path already exists, changes the buttons accordingly.
def is_shit_there(self, download_path, index, update_file):
    if path.exists(download_path + '/' + update_file):
        self.textbox.dlbutton_list[index].configure(text='Redownload')
        self.textbox.open_button_list[index].configure(text='Open', state='normal', command=lambda: self.open_loc(download_path))
        self.textbox.status_list[index].configure(text_color = 'green', text='Already Owned!')

#creates a directory for the game in the download path.
def create_directories(download_path):
    if not path.exists(download_path):
        makedirs(download_path)
    return download_path

class ConfigSettings():
    def __init__(self):
        super().__init__()

    def get_config():
        config = ConfigParser()
        config.read('config.ini')
        save_dir = config.get('paths', 'downloads')
        rpcs3_dir = config.get('paths', 'RPCS3')
        return save_dir, rpcs3_dir

    def save_config(mode, save_dir , rpcs3_dir):
        config = ConfigParser()
        with open('config.ini', mode) as ini:
            config.add_section('paths')
            config.set('paths', 'downloads', save_dir)
            config.set('paths', 'RPCS3', rpcs3_dir)
            config.write(ini)

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


class ButtonAction(Enum):
    STOP = 1
    PAUSE = 2
    RESUME = 3


#window with save and yml locations.
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

    def button_save_loc(self):
        temporary_temp = self.temp_save
        self.temp_save=customtkinter.filedialog.askdirectory(parent = self)
        if self.temp_save != '':
            self.save_dir_field.configure(state='normal')
            self.save_dir_field.delete('0.0','end')
            self.save_dir_field.insert('0.0', self.temp_save)
            self.save_dir_field.configure(state='disabled')
        else: self.temp_save = temporary_temp

    def button_yml_loc(self):
        temporary_temp = self.temp_rpcs3
        self.temp_rpcs3=customtkinter.filedialog.askdirectory(parent = self)
        if self.temp_rpcs3 != '':
            self.yaml_dir_field.configure(state='normal')
            self.yaml_dir_field.delete('0.0','end')
            self.yaml_dir_field.insert('0.0', self.temp_rpcs3)
            self.yaml_dir_field.configure(state='disabled')
        else: self.temp_rpcs3 = temporary_temp

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

#Window with dl all options. Need to actually make this work properly (Maybe it does?)
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

#Frame where all the fun widgets go.
class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=1)
        self.grid_columnconfigure(( 2, 3, 4), weight=0)
        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.title_label_list = []
        self.size_label_list = []
        self.status_list = []
        self.queue_list = []
        self.dlbutton_list = []
        self.open_button_list = []
        self.prog_bar_list = []

    #creates widgets within the frame, adds appropriate ones to the grid, then adds them to a list.
    def add_item(self, name, title_id, ver, url, console, update_size, sha1, index, download_path, update_file):
        size = str(round((update_size/1024000),2)) + ' MB'
        if ver.startswith(' D') and len(name)>9 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name[:9] + '...', anchor='w')
        elif len(name)>18 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name[:18] + '...', anchor='w') 
        elif len(name)<=18 and not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + ' - ' + name, anchor='w')
        else:
            title_label = customtkinter.CTkLabel(self, text= title_id + ver + name, anchor='w')
        size_label = customtkinter.CTkLabel(self, text=size, anchor='e')
        status = customtkinter.CTkLabel(self, text='', anchor='e', width = 160)
        q = queue.Queue()
        dlbutton = customtkinter.CTkButton(self, text='Download', width=100, height=24)
        open_button = customtkinter.CTkButton(self, text='Open', width=100, height=24, state = 'disabled')
        if self.command is not None:
                dlbutton.configure(command=lambda: self.command(name, title_id, url, console, update_size, sha1, index, download_path, update_file))
                open_button.configure(command=lambda: self.command(download_path, index, update_file))
        prog_bar = customtkinter.CTkProgressBar(self, width=440, height=5)
        prog_bar.set(0)
        if not name.startswith('Invalid ID') and not name.startswith('No updates available for') and name != 'No updates found':  
            title_label.grid(row=len(self.title_label_list), column=0, pady=(0, 10), sticky='w')
            status.grid(row=len(self.title_label_list), column=1, pady=(0, 10),padx=(0, 0), sticky='e') 
            size_label.grid(row=len(self.title_label_list), column=2, padx=(0,5), pady=(0, 10), sticky='e')
            prog_bar.grid(row=len(self.dlbutton_list), column=0, columnspan=3, pady=(15, 0), sticky='w')
            dlbutton.grid(row=len(self.dlbutton_list), column=3, pady=(0, 10), padx=0, sticky='e')
            open_button.grid(row=len(self.dlbutton_list), column=4, pady=(0, 10), padx=(0,0), sticky='e')
        else:
            title_label.grid(row=len(self.title_label_list), column=0, columnspan=8, pady=(0, 10))
            
        self.title_label_list.append(title_label)
        self.size_label_list.append(size_label)
        self.status_list.append(status)
        self.queue_list.append(q)
        self.dlbutton_list.append(dlbutton)
        self.open_button_list.append(open_button)
        self.prog_bar_list.append(prog_bar)

    #iterates through the widgets looking for specific strings. If one is found, the whole line will be deleted.
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

#main window and some button functionality
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__() 
        width = self.winfo_screenwidth()/3
        height = self.winfo_screenheight()/3
        self.geometry('760x640')
        self.title('PySN')
        self.resizable(0,0)
        self.minsize(760, 200)
        self.maxsize(760, 640)
        self.toplevel_window = None
        self.stop_down = False
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        self.entry = customtkinter.CTkEntry(master=self, placeholder_text='Enter Serial', width = 125)
        self.entry.grid(row=0, column=0, padx=(4,2), pady=(6,0), sticky='ew')
        self.combobox = customtkinter.CTkComboBox(master=self, values=['PlayStation 3', 'PlayStation 4', 'PlayStation Vita'], width = 125)
        self.combobox.grid(row=0, column=1, columnspan=1, padx=(2,2), pady=(6,0), sticky='ew')
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
    
    #If you want to clear the text box, the search button will destroy it and recreate it, then search.
    #Otherwise it will clear labels such as 'Invalid ID' before appending the list.
    def open_loc(self, download_path):
        customtkinter.filedialog.askopenfilenames(initialdir=download_path)

    def search_type(self):
        if self.checkbox.get() == 0:
            title_id = (self.entry.get()).upper()
            console = self.combobox.get()
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

#assigns hashes and urls based on console, checks if the url is valid, returns the xml root and game name.
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
                
    #this should probably be global? or the global shit should go in App?
    #requests game/update info and creates widgets in the frame based on that info.
    def search(self, title_id, console):
        root, game_name = self.request_update(title_id, console)

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

                name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '').strip()
                download_path = save_dir + console + '/' + title_id + ' ' + name
                update_file = path.basename(url)      
                self.textbox.add_item(game_name, title_id, ' v' + ver, url, console, update_size, sha1, index, download_path, update_file)
                is_shit_there(self, download_path, index, update_file)
        elif game_name == 'Invalid ID': 
            self.textbox.add_item('Invalid ID: ' + title_id, '', '', '', '', 0, '', '', '', '')
        else: self.textbox.add_item('No updates available for ' + title_id, '', '', '', '', 0, '', '', '', '')

    def search_no_drm(self, title_id, console):
        root, game_name = self.request_update(title_id, console)
        if root != 0:
            for item in root.iter('package'):
                ver = 'DRM-Free v' + (item.get('version'))
            for item in root.iter('url'):
                index = len(self.textbox.dlbutton_list) 
                url = (item.get('url'))
                sha1 = (item.get('sha1sum'))
                update_size = int((item.get('size')))
                name = game_name.replace(':', ' -').replace('/', ' ').replace('?', '').strip()
                download_path = save_dir + console + '/' + title_id + ' ' + name
                update_file = 'DRM-Free ' + path.basename(url)    
                self.textbox.add_item(game_name, title_id, ' ' + ver, url, console, update_size, sha1, index, download_path, update_file)
                is_shit_there(self, download_path, index, update_file)
        elif game_name == 'Invalid ID':
                self.textbox.clear_items()
                self.textbox.add_item('Invalid ID: ' + title_id, '', '', '', '', 0, '', '', '', '')
        else:
            self.textbox.clear_items() 
            self.textbox.add_item('No updates available for ' + title_id, '', '', '', '', 0, '', '', '', '')
    
    def toggle_pause(self, index):
        if self.textbox.dlbutton_list[index].cget('text') == 'Pause':
            self.textbox.dlbutton_list[index].configure(text='Resume')
            self.textbox.queue_list[index].put(ButtonAction.PAUSE)
        else:
            self.textbox.dlbutton_list[index].configure(text='Pause')
            self.textbox.queue_list[index].put(ButtonAction.RESUME)

    def cancel(self, index):
        self.textbox.dlbutton_list[index].configure(text='Download')
        self.textbox.queue_list[index].put(ButtonAction.STOP)
    
    def download_updates(self, url, download_path, size, hash, index, title_id, name, console, update_file, sem):
        with sem:
            create_directories(download_path)
            self.textbox.dlbutton_list[index].configure(text='Pause', command=lambda: self.toggle_pause(index))
            self.textbox.open_button_list[index].configure(text='Cancel', state = 'normal', command=lambda: self.cancel(index))
            sha1 = hashlib.sha1()
            fileloc = (download_path + '/' + update_file)
            i=0
            h=0
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

            self.textbox.dlbutton_list[index].configure(command=lambda: App.frame_button_download(self, name, title_id, url, console, size, hash, index, download_path, update_file))
            self.textbox.open_button_list[index].configure(text='Open', state = 'disabled', command=lambda: None)
            if self.textbox.status_list[index].cget('text') == 'Download Cancelled!':
                os.remove(fileloc)
            else:
                is_shit_there(self, download_path, index, update_file)   
                self.textbox.dlbutton_list[index].configure(state='disabled')
                self.textbox.open_button_list[index].configure(state='disabled')
                self.textbox.status_list[index].configure(text_color = 'yellow', text='Checking Hash...')
                with open(fileloc,'rb') as f:
                    if console == 'PlayStation 3' or console == 'PlayStation Vita':
                        data = f.read()[:-32]
                    else: data = f.read()
                    sha1.update(data)
                if hash.upper() == (sha1.hexdigest().upper()):
                    self.textbox.status_list[index].configure(text_color = 'green', text='Download Complete!')
                else:
                    self.textbox.status_list[index].configure(text_color = 'red', text='HASH MISMATCH DETECTED!')
                self.textbox.dlbutton_list[index].configure(state='normal')
                self.textbox.open_button_list[index].configure(state='normal')

    #Downloads all files, or only new files based on the check box in the downall window.
    #pretty sure this shit should be in the window class...
    def downall(self):
        self.toplevel_window.destroy()
        if self.toplevel_window.only_new_check.get() == 0:
            for item in self.textbox.dlbutton_list:
                item.invoke()
        else:
            for item in self.textbox.dlbutton_list:
                if item.cget('text') == 'Download':
                    item.invoke()

    def button_search(self):
        if self.clearbox.get() == 1:
            self.textbox.destroy()
            self.textbox = ScrollableLabelButtonFrame(master=self, height=540, command=self.frame_button_download, corner_radius=5)
            self.textbox.grid(row=1, column=0, columnspan=8, padx=4, pady=0, sticky='ew')
            self.search_type()
        else:
            self.textbox.clear_items()
            self.search_type()

    def frame_button_download(self, game_name, title_id, url, console, update_size, sha1, index, download_path, update_file):
        semaphore = threading.Semaphore(2)
        threading.Thread(target = self.download_updates, args=(url, download_path, update_size, sha1, index, title_id, game_name, console, update_file, semaphore), daemon = True).start()

    #opens the download all window.
    def button_downall(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DownloadAllWindow(self)  # create window if it's None or destroyed
            self.toplevel_window.title('Download')
            self.toplevel_window.resizable(0,0)
            self.toplevel_window.attributes('-topmost', 1)
            self.toplevel_window.save_button.configure(command=self.downall)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    #clears the list.            
    def button_clear(self):
        self.textbox.destroy()
        self.textbox = ScrollableLabelButtonFrame(master=self, height=540, command=self.frame_button_download, corner_radius=5)
        self.textbox.grid(row=1, column=0, columnspan=8, padx=4, pady=0, sticky='ew')

    #opens the settings window.
    def button_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SettingsWindow(self)
        else:
            self.toplevel_window.focus()


save_dir, rpcs3_dir = ConfigSettings.check_config()


if __name__ == '__main__':
    app = App()
    app.mainloop()
