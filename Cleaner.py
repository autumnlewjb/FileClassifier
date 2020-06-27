import os
import sys
from time import sleep

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
    new_dir = str(break_dir[0]) + "(" + str(no) + ")" + str(break_dir[1])
    return new_dir


class Cleaner:
    def __init__(self, only_folder_exist):
        self.only_folder_exist = only_folder_exist
        self.track_dir = os.getcwd()
        self.li_filename = None
        self.destination_dir = None

    def validate_dir(self):
        check_list = [self.track_dir, self.only_folder_exist]
        i = 0
        while i < len(check_list):
            if check_list[i] == self.track_dir:
                new_word = check_list[i].replace('/', '\\')
                if new_word[len(check_list) - 1] != '\\':
                    check_list[i] += '\\'
                self.track_dir = check_list[i]
            elif check_list[i] == self.only_folder_exist:
                check_list[i] = check_list[i].replace('/', '').replace('\\', '')
                self.only_folder_exist = check_list[i]
            i += 1

        self.destination_dir = self.track_dir + self.only_folder_exist

    def detect_new_folder(self):
        ans = False
        if not os.path.exists(self.destination_dir):
            os.mkdir(self.destination_dir)
        self.li_filename = os.listdir(self.track_dir)

        for filename in self.li_filename:
            file_dir = self.track_dir + filename
            if filename != self.only_folder_exist and file_dir != sys.executable:
                ans = True
                break
            else:
                ans = False
        return ans

    def moving_file(self, extension_dict):
        for filename in self.li_filename:
            file_dir = self.track_dir + filename
            if filename != self.only_folder_exist and file_dir != sys.executable:
                old_dir = self.track_dir + filename
                new_dir = self.identify_destination(filename, extension_dict)
                exist = os.path.exists(new_dir)
                if not exist:
                    os.mkdir(new_dir)

                new_dir = new_dir + '\\' + filename
                print(new_dir)
                if not os.path.isfile(new_dir):
                    os.rename(old_dir, new_dir)
                else:
                    count = 1
                    new_new_dir = rename_repetition(new_dir, count)
                    print(new_new_dir)
                    while os.path.exists(new_new_dir):
                        count += 1
                        new_new_dir = rename_repetition(new_dir, count)
                        print("enter loop")

                    os.rename(old_dir, new_new_dir)

    def identify_destination(self, filename, extension_dict):
        ext = 'none'
        repeat = True
        file_extension = str(os.path.splitext(self.track_dir + filename)[1])
        for file_type in extension_dict:
            for extension in extension_dict[file_type]:
                if file_extension == extension:
                    ext = file_type
                    repeat = False
                    break

            if not repeat:
                break
        return self.destination_dir + '\\' + type

    def main_process(self):
        if self.detect_new_folder():
            self.moving_file(extensions)


if __name__ == '__main__':
    print(sys.executable)
    main_folder = str(input('What name would you like for the main folder? '))
    obj = Cleaner(main_folder)
    obj.validate_dir()
    print('Clearing ' + obj.track_dir + '...')
    print('Destination Folder at ' + obj.destination_dir)
    permission = str(input('Proceed?(Y/N) ')).lower()[0]
    count = 0
    while permission == 'y':
        try:
            obj.main_process()

            sleep(3)
            count += 1
            print(count)
            if count == 50:
                count = 0
                permission = str(input('Proceed?(Y/N) ')).lower()[0]
        except KeyboardInterrupt:
            break
    print('PROCESS ENDED...')
