# Stream Shard Updater
*A tool to dynamically update shard names on streams.*

If you ever livestream Toontown private servers, you know the hassle of people asking you what district you're in. When you're bothered about that, you put your current district as an overlay on your stream. What happens when you change districts, or the game crashes? You have to update it again, and the whole process is downright annoying. This is where the Steam Shard Updater comes in.

After configuring the application, it will automatically scan the latest file available at whatever interval you've selected. When it detects a district, the files `district.txt` and `district_name.txt` are generated. The first file contains `District Name: <district>`, whereas the latter simply holds the name of the district.

Currently, this application is very TTR-biased, however that will change as other servers emerge.

## Usage:

When opening the application for the first time, you will be asked to input the directory to your game and an update variable.
Commonly, you'll want to use `C:\Program Files (x86)\Toontown Rewritten\logs\` for the directory, and you can set any cardinal number (meaning whole numbers 1 and above.)

After the initial configuration, the application will immediately begin to read the latest log file available in that directory.

The log reading will occur in the background on a seperate thread. This means you are able to take advantage of a built in command line. While there is not much functionality, type `help` for more information.

## Troubleshooting

The application will need read/write access in whatever directory you run it from. Ensure you run this somewhere outside of the `Program Files` folders (such as your desktop or documents), or you will almost certainly run into permission problems.

## Compilation

Some users feel uncertain downloading a pre-compiled program, and rightfully so. If you wish to compile the application yourself, follow these steps:

**Note:** Ensure you are running Python 2.7, any version of Python 3 will not work.

1. Clone the repository by typing `git clone https://github.com/misread/stream-shard-updater/
2. Install all necessary requirements by typing `pip install -r requirements.txt`
3. Compile the application by typing `pyinstaller main.py --clean -n shards` This will generate `shards.exe` under the `dist` folder.

**Optional:** You can also add the argument `-F` to place all of the DLLs and PYD files in the application itself, effectively leaving you with one exe file. However, this is prone to triggering anti-virus more easily.
