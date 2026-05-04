# PySN
PySN is a program which downloads Title Update PKGs for the PlayStation 3, PlayStation 4, and PlayStation Vita directly from Sony's servers. It can also download Firmware PUP files for all 3 consoles plus the PlayStation 5. 

Features:
- Windows, Linux, and MacOS support
- A clean and easy to use GUI
- SHA-1 hash verification of downloads and owned files
- Ability to search RPCS3's games.yml
- Support for DRM-Free Title Updates
- Most recent Firmware downloads for all 4 consoles
  - Includes PS4 recovery FW, Vita fonts, and Vita preinst FW

If you prefer the command line version of this tool, it can be found [here](https://github.com/AphelionWasTaken/PySN_CMD).

Installation
============
Windows
------------------------
Just download PySN_Windows.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest), extract the folder, and run the .exe.

MacOS
------------------------
Just download PySN_MacOS.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest) and run the executable.

Linux/BSD
------------------------
Just download PySN_Linux.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest) and run the executable.

Using PySN
============
Once the program is open, just type a valid PS3, PS4, or PS Vita Title ID (e.g. BCUS98114) into the search bar, select the proper console from the dropdown menu, and then hit the "Enter" key or the "Search" button.

This program will then locate any Title Updates for that game, list them out, and ask you if you would like to download them.

You can also have PySN scan your RPCS3 games.yml to find updates for all of your installed games at once. On Linux and MacOS, all you need to do is check the "Search Games.yml" checkbox and hit the search button.

On Windows you will need to point PySN to your RPCS3 installation via the settings first.

If you want to download firmware, just type in "fw" or "firmware" and hit enter or click the search button.

File Locations
------------------------
Title Updates are downloaded into an Updates folder within the directory containing PySN by default, and are separated by console and game (e.g. `PySN/Updates/PlayStation 3/[BCUS98114] Gran Turismo 5`).

You can change the update folder location in PySN's settings, as well as the folder naming structure if you prefer to have the game title before the game ID (for sorting alphabetically by title).

On Windows the config file is saved to the directory containing PySN.exe. On MacOS it is in Home/Library/Application Support/PySN. On Linux is is in Home/.config/PySN

Building PySN
============
PySN does not need to be "built". Releases are created via PyInstaller. If you would rather run this directly from the source code, this program requires [Python 3](https://www.python.org/downloads/). It is included with most Linux Distros, although you may need to upgrade to a more recent version.

You will also need the Requests, CustomTkinter, BeautifulSoup, and PyYaml Python modules installed to run this program. To install these, open any terminal and type `pip install requests`, `pip install customtkinter`, `pip install beautifulsoup4`, and `pip install pyyaml`, respectively.

If you have already cloned/downloaded this repo, you can easily install all of these modules by navigating to your PySN directory (where requirements.txt exists), and type `pip install -r requirements.txt`.

Once you have the modules, clone this repo or just click on the green Code button and download the zip folder.

Extract the files and <ins>move the icons from the Icons folder into the root of your PySN folder</ins> (next to PySN.py), then run PySN.py with Python. Or run it in a terminal by navigating to the directory containing PySN.py and typing `python PySN.py`.

Or run it however else you want, I don't care, I'm not a cop.

Screenshots
============
<p align="center">
    <img height = 337 width = 400 src="https://github.com/user-attachments/assets/abe6727c-f83b-4eb8-894b-fdd0203bd064" >
    <img height = 337 width = 400  src="https://github.com/user-attachments/assets/c956cfef-1644-4a43-accf-2f5fc9503fa3" >
    <p align="center">
    <img height = 281.5 width = 400 src="https://github.com/user-attachments/assets/c4fc3cff-4594-4a49-bbb2-4d7e8b6940a1" >
    <img  height = 281.5 width = 400 src="https://github.com/user-attachments/assets/dbca640a-f7e6-456a-b494-ca7cbc5f830a" >
</p>


Contributors
============
- [Aphelion](https://github.com/AphelionWasTaken)
- [GalCiv](https://github.com/RipleyTom) - Thread handling/scheduling for downloads
- [Darkhost](https://github.com/Darkhost1999) - Testing/bug reporting
- [schm1dtmac](https://github.com/schm1dtmac) - Icns file and MacOS arm64 testing
- [FlexBy420](https://github.com/flexby420) - PlayStation 5 firmware searches