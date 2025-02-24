# PySN
A simple tool for downloading Title Updates for PlayStation 3, PlayStation 4, and PlayStation Vita games.

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
Once the program is open, just type a valid PS3, PS4, or PS Vita Title ID (e.g. BCUS98114) into the search bar, select the proper console from the dropdown menu, and hit "Search".

This program will then locate any Title Updates for that game, list them out, and ask you if you would like to download them.

By default, Title Updates are downloaded into an Updates folder within the PySN directory, and are separated by console and game (e.g. `PySN/Updates/PlayStation 3/BCUS98114 Gran Turismo 5`). You can change the update folder location in the settings, but your updates will always be separated out by console and game.

You can also point PySN to your RPCS3 installation via the settings. If you do so, you can then check the "Search Games.yml" box and hit "Search" to find updates for all of the games you have in RPCS3 at once.

Known Bugs
============
Keep your eye on the Issues page for anything not listed here.
- Sometimes the Download All button just doesn't download all of the updates. Not sure why, as it should iterate through all of the buttons in the array. Pretty sure it's a threading issue. Just double check that it didn't miss anything if you use this feature.

Contributors
============
- [Aphelion](https://github.com/AphelionWasTaken)
- [GalCiv](https://github.com/RipleyTom) - Thread handling/scheduling
- [Darkhost](https://github.com/Darkhost1999) - Testing/Bug reporting
