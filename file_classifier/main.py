import os
import sys
import shutil
# from Extension import extensions
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

extensions = {
    'Audio': ['.aif', '.cda', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl'],
    'Compressed': ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip'],
    'Media': ['.bin', '.dmg', '.iso', '.toast', '.vcd'],
    'Data': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml'],
    'Email': ['.email', '.eml', '.emlx', '.msg', '.oft', '.ost', '.pst', '.vcf'],
    'Exe': ['.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.exe', '.gadget', '.jar', '.msi', '.py', '.wsf'],
    'Font': ['.fnt', '.fon', '.otf', '.ttf'],
    'Image': ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff'],
    'Internet': ['.asp', '.aspx', '.cer', '.cfm', '.cgi', '.pl', '.css', '.htm', '.html', '.js', '.jsp', '.part',
                 '.php', '.py', '.rss', '.xhtml'],
    'Presentation': ['.key', '.odp', '.pps', '.ppt', '.pptx'],
    'Programming': ['.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb'],
    'Spreadsheet': ['.ods', '.xls', '.xlsm', '.xlsx'],
    'System': ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi',
               '.sys', '.tmp'],
    'Video': ['.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf',
              '.vob', '.wmv'],
    'Text': ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd'],
}


def rename_repetition(new_dir, no):
    break_dir = os.path.splitext(new_dir)
    new_dir = f"{break_dir[0]}({no}){break_dir[1]}"
    return new_dir


class Cleaner:
    def __init__(self):
        self.only_folder_exist = 'only_folder_exist'
        self.track_dir = Path.home() / 'Desktop' / 'test'
        self.destination_dir = None

    @property
    def destination_dir(self):
        return self._destination_dir

    @destination_dir.setter
    def destination_dir(self, value):
        if value is None:
            self.only_folder_exist = self.only_folder_exist.replace('/', '').replace('\\', '')

            self._destination_dir = self.track_dir / self.only_folder_exist

            if not os.path.exists(str(self._destination_dir)):
                os.mkdir(str(self._destination_dir))

    def moving_file(self, extension_dict):
        print(os.listdir(str(self.track_dir)))
        for filename in os.listdir(str(self.track_dir)):
            if filename != self.only_folder_exist:
                old_dir = self.track_dir / filename
                new_dir = self.identify_destination(filename, extension_dict)
                exist = os.path.exists(str(new_dir))
                if not exist:
                    os.mkdir(str(new_dir))

                new_dir = new_dir / filename

                count = 1
                while os.path.isfile(new_dir):
                    new_dir = rename_repetition(new_dir, count)
                    count += 1
                shutil.move(f'{old_dir}', f'{new_dir}')
                # TODO: The process cannot access the file because it is being used by another process

    def identify_destination(self, filename, extension_dict):
        file_extension = str(os.path.splitext(filename)[1])
        for folder_name, extension_list in extension_dict.items():
            if file_extension in extension_list:
                return self._destination_dir / folder_name

        return self.destination_dir / 'none'


class EventHandler(FileSystemEventHandler):
    def __init__(self):
        self.cleaner = Cleaner()

    def on_modified(self, event):
        print('Something happened')
        self.cleaner.moving_file(extensions)


if __name__ == '__main__':
    observer = Observer()
    event_handler = EventHandler()

    print('Clearing ' + str(event_handler.cleaner.track_dir) + '...')
    print('Destination Folder at ' + str(event_handler.cleaner.destination_dir))
    observer.schedule(event_handler, str(event_handler.cleaner.track_dir), recursive=True)
    observer.start()
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
