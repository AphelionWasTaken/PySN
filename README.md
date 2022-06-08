# PySN
A simple tool for downloading Title Updates for PlayStation 3, PlayStation 4, and PlayStation Vita games.

Installation
============
Windows
------------------------
Just download PySN.zip from [Releases](https://github.com/AphelionWasTaken/PySN/releases/latest) and extract the contents to a folder somewhere.

Linux/BSD/Mac OS
------------------------
This program uses Python 3. You must have [Python](https://www.python.org/downloads/) installed to run this program. It is included with Mac OS X and most Linux Distros, although you may need to upgrade to a more recent version.

You will also need the Requests Python module installed to run this program. To install this, open any terminal and type `pip install requests`.

Clone this repo or just click on the green Code button and download the zip folder, then run PySN.py with Python. Or run it in a terminal by navigating to the directory containing PySN.py and typing `python PySN.py`. Or run it however else you want, I don't care, I'm not a cop.

Installation through PyPl soon™

Using PySN
============
Once the program is open, just type a valid PS3, PS4, or PS Vita Title ID (e.g. PCSA00007) into the console and press enter. This script will then download any Title Updates for that game, and then it will ask you if you want to search for more. If you do not answer "y" or "Y", then the program closes.

Title Updates are downloaded into `[Folder Containing PySN.py]/Updates/[Console]/[Title ID] [Game Name]/`. Maybe someday I will let you change that without making you dig into the code...

Large PlayStation 4 Title Updates will be split because that's how Sony hosts them. You'll need to use a program like [PKG Merge](https://github.com/aldoblack/pkg-merge/releases/latest) to combine them.
