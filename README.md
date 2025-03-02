# PySN
PySN is a program which downloads Title Update PKGs and Firmware PUPs for the PlayStation 3, PlayStation 4, and PlayStation Vita directly from Sony's servers.

Features:
- Windows, Linux, and MacOS support
- A clean and easy to use GUI
- SHA-1 hash verification of downloads and owned files
- Ability to search RPCS3's games.yml
- Support for DRM-Free Title Updates
- Most recent Firmware downloads for all 3 consoles
  - Includes PS4 recovery FW, Vita fonts, and Vita preinst FW

If you prefer the command line version of this tool, it can be found [here](https://github.com/AphelionWasTaken/PySN_CMD).

Installation
============
Windows
------------------------
Just download PySN.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest), extract the folder, and run the .exe.

Linux/BSD/Mac OS
------------------------
This program uses Python 3. You must have [Python](https://www.python.org/downloads/) installed to run this program. It is included with Mac OS X and most Linux Distros, although you may need to upgrade to a more recent version.

You will also need the Requests, CustomTkinter, and PyYaml Python modules installed to run this program. To install these, open any terminal and type `pip install requests`, `pip install customtkinter`, and `pip install pyyaml`, respectively.

Clone this repo or just click on the green Code button and download the zip folder, then run PySN.py with Python. Or run it in a terminal by navigating to the directory containing PySN.py and typing `python PySN.py`. Or run it however else you want, I don't care, I'm not a cop.

Using PySN
============
Once the program is open, just type a valid PS3, PS4, or PS Vita Title ID (e.g. BCUS98114) into the search bar, select the proper console from the dropdown menu, and then hit the "Enter" key or the "Search" button.

This program will then locate any Title Updates for that game, list them out, and ask you if you would like to download them.

By default, Title Updates are downloaded into an Updates folder within the PySN directory, and are separated by console and game (e.g. `PySN/Updates/PlayStation 3/BCUS98114 Gran Turismo 5`). You can change the update folder location in the settings, but your updates will always be separated out by console and game.

You can also point PySN to your RPCS3 installation via the settings. If you do so, you can then check the "Search Games.yml" box and hit "Search" to find updates for all of the games you have in RPCS3 at once.

If you want to download firmware, just type in "fw" or "firmware" and hit enter or click the search button.

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
- [GalCiv](https://github.com/RipleyTom) - Thread handling/scheduling
- [Darkhost](https://github.com/Darkhost1999) - Testing/Bug reporting
