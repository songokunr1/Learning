import os
import shutil
from easygui import *


class Files:
    file_types = {"zdjęcia": ['gif', 'jpg', 'png', 'jpeg', 'tiff', "psd","raw","svg"],
                  "exe": ["exe"], "dokumenty": ["pdf", "docx", "doc", "docm", ],"Muzyka" : ["mp3","flac"], "Filmy" : ["mp4","avi","dvd","flv","mov","mpg",],"Niestandardowe": []}
    choices = ["Wybierz folder docelowy", "Wybierz folder do posortowania", "Continue"]
    moved_files = []
    ready_to_continue = False

    def __init__(self, from_folder_path=None, in_folder_path=None):
        self.from_folder = from_folder_path
        self.in_folder = in_folder_path

    def move_files(self, file_type_to_move="zdjęcia"):
        for file_name in os.listdir(self.from_folder):
            if file_name.split(".")[-1].lower() in self.file_types[file_type_to_move]:
                from_file_path = self.from_folder + fr"\{file_name}"
                should_we_break = self.move_file(from_file_path, file_name)
                self.moved_files.append(file_name)
                if should_we_break:
                    break
    def move_file(self, from_file_path, file_name):
        try:
            shutil.move(from_file_path, self.in_folder)
        except PermissionError as error:
            choices = ["Spróbuj ponownie", "Pomiń", "Zakończ działanie programu"]
            choice = buttonbox(f"nie udało sie przenieść pliku {file_name} \n Możliwe rozwiązania \n 1. Zamknij plik jeśli jest otwarty \n 2. Sprawdź czy plik nie znajduje się w folderze docelowym \n treść błędu: {error}",
                "Wykryto Błąd", choices)
            if choice == "Spróbuj ponownie":
                self.move_file(from_file_path, file_name)
            if choice == "Pomiń":
                pass
            if choice == "Zakończ działanie programu":
                return True
        except shutil.Error as error:
            os.remove(fr"{self.in_folder}\{file_name}")
            print(fr"remove {self.in_folder}\{file_name}")
            self.move_file(from_file_path, file_name)
    def select_files_type(self):
        msg = "Wybierz rodzaj plików króre chcesz posortować"
        title = ""
        choices = [key for key in self.file_types.keys()]
        self.file_type = choicebox(msg, title, choices)
        if self.file_type == "Niestandardowe":
            key = ""
            value = []
            msg = "Wybierz rozszerzenia które chcesz filtrować"
            title = "narzędzie filtrów niestandardowych"
            choices = ['gif', 'jpg', 'png', 'jpeg', 'tiff', "psd","raw","svg","exe","pdf", "docx", "doc", "docm","mp3","flac", "mp4","avi","dvd","flv","mov","mpg"]
            value = multchoicebox(msg, title, choices)
            key = enterbox("Wprowadź nazwę filtra", "narzędzie filtrów niestandardowych")
            self.file_types[key] = value
            self.select_files_type()
        return self.file_type

    def select_folder_from(self):
        self.from_folder = diropenbox("Wybierz Folder")

    def select_folder_in(self):
        self.in_folder = diropenbox("Wybierz Folder")

    def select_folders(self, reply=""):
        msg = "Wybierz Foldery".center(80, " ")
        reply = buttonbox(msg, choices=self.choices)
        msgreplay1 = "folder docelowy - " + self.in_folder if self.in_folder else "Wybierz folder docelowy"
        msgreplay2 = 'folder do posortowania - ' + self.from_folder if self.from_folder else "Wybierz folder do posortowania"
        print(reply)
        if reply == msgreplay1:
            self.select_folder_in()
            self.choices[0] = 'folder docelowy - ' + przeniesienie.in_folder
        if reply == msgreplay2:
            self.select_folder_from()
            self.choices[1] = 'folder do posortowania - ' + przeniesienie.from_folder
        if reply == "Continue":
            if self.in_folder != None and self.from_folder != None and msgreplay2.split(" ")[-1] != msgreplay1.split(" ")[-1]:
                self.ready_to_continue = True
            else:
                if self.in_folder == None or self.from_folder == None:
                    msgbox("Nie wybrano Folderów", "", "Ok")
                if msgreplay2.split(" ")[-1] == msgreplay1.split(" ")[-1]:
                    msgbox("Wybrano te same foldery", "", "Ok")


przeniesienie = Files()
while przeniesienie.ready_to_continue is False:
    przeniesienie.select_folders()
file_type = przeniesienie.select_files_type()
przeniesienie.move_files(file_type)
tekst = ""
for file_name in przeniesienie.moved_files:
    tekst = tekst + "-" + file_name + "\n"
msgbox(f"Przeniesiono pliki:\n\n{tekst}", ok_button="Ok")
print(przeniesienie.moved_files)
