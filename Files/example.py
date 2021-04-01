with open('data.txt', 'w') as f:
    data = 'some data to be written to the file'
    f.write(data)
import os


with os.scandir('my_directory/') as entries:
    for entry in entries:
        print(entry.name)

os.path.join(os.getcwd(), 'download')

os.scandir()

import zipfile
file_list = ['file1.py', 'sub_dir/', 'sub_dir/bar.py', 'sub_dir/foo.py']
with zipfile.ZipFile('new.zip', 'w') as new_zip:
    for name in file_list:
        new_zip.write(name)

shutil.make_archive('data/backup', 'tar', 'data/')