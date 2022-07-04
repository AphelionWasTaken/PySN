# PySN
A simple tool for downloading Title Updates for PlayStation 3, PlayStation 4, and PlayStation Vita games.

Installation
============
Windows
------------------------
Just download PySN.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest) and extract the folder.

Linux/BSD/Mac OS
------------------------
This program uses Python 3. You must have [Python](https://www.python.org/downloads/) installed to run this program. It is included with Mac OS X and most Linux Distros, although you may need to upgrade to a more recent version.

You will also need the Requests and Clint Python modules installed to run this program. To install these, open any terminal and type `pip install requests` and `pip install clint`, respectively.

Clone this repo or just click on the green Code button and download the zip folder, then run PySN.py with Python. Or run it in a terminal by navigating to the directory containing PySN.py and typing `python PySN.py`. Or run it however else you want, I don't care, I'm not a cop.

Using PySN
============
Once the program is open, just type a valid PS3, PS4, or PS Vita Title ID (e.g. BCUS98114) into the console and press enter.

This script will then locate any Title Updates for that game, and ask you if you would like to download them. Replying with y/Y will download all of the updates found for that game, and then it will ask if you would like to search for another game. Replying with y/Y will prompt you for another Title ID, while any other input will close the program.

Title Updates are downloaded into an Updates folder within the PySN directory, and are split by console and game (e.g. `PySN/Updates/PlayStation 3/BCUS98114 Gran Turismo 5`). Maybe someday I will let you change that without making you dig into the code...
