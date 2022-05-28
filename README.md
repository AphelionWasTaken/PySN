# PySN
Fetches title updates for PlayStation Vita and PlayStation 3 games. I might look into support for PS4 Title Updates. Maybe even a GUI. Who knows.

Installation
============
You must have [Python](https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe) installed to run this program. If you need to install it, be sure to check "Add Python to PATH" on the very first screen.

You will also need the requests python module installed to run this program. To install this, open any terminal (Command Prompt, MSVC, etc.) and type `pip install requests`.

Click on the green code button and download the zip folder, then run PySN.py with Python. Or run it in a terminal by navigating to the directory containing PySN.py and typing `python PySN.py`. Or run it however else you want, I don't care, I'm not a cop.

Installation through PyPl soon™

Using PySN
============
Once the program is open, just type a valid PS Vita or PS3 Title ID (e.g. PCSA00007) into the console and press enter. This script will then download any Title Updates for that game, and then it will ask you if you want to search for more. If you do not answer "y" or "Y", then the program closes.

Title Updates are downloaded into `[Folder Containing PySN.py]/Updates/[Console]/[Title ID] [Game Name]/`. Maybe someday I will let you change that without making you dig into the code...
