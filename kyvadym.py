from distutils.file_util import move_file
import os
import re
import shutil
import sys



files = {"audio": ["mp3", "ogg", "wav", "amr"],
         "video": ["mp4", "avi", "mov", "mkv", "MOV"],
         "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "rtf", "PDF", "xls"],
         "images": ["jpeg", "png", "jpg", "svg", "bmp", "BMP"],
         "archives": ["zip", "gz", "tar", "tgz", "rar"],
         "other":[]}


def normalize(name):   # Транслитерация c rbhbkbws
    dictionary = {ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "G", ord("Д"): "D", ord("Е"): "E", ord("Ж"): "ZH", ord("З"): "Z",
                  ord("И"): "I", ord("Й"): "J", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O", ord("П"): "P",
                  ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F", ord("Х"): "H", ord("Ц"): "TS", ord("Ч"): "CH",
                  ord("Ш"): "SH", ord("Щ"): "SHCH", ord("Ь"): "", ord("Э"): "E", ord("Ю"): "YU", ord("Я"): "YA", ord("Ъ"): "", ord("Ы"): "Y",
                  ord("Ё"): "E", ord("Є"): "E", ord("І"): "Y", ord("Ї"): "YI", ord("Ґ"): "G",
                  ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "g", ord("д"): "d", ord("е"): "e", ord("ж"): "zh", ord("з"): "z",
                  ord("и"): "y", ord("й"): "j", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o", ord("п"): "p",
                  ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "y", ord("ф"): "f", ord("х"): "h", ord("ц"): "c", ord("ч"): "ch",
                  ord("ш"): "sh", ord("щ"): "shsc", ord("ь"): "", ord("э"): "e", ord("ю"): "yu", ord("я"): "ya", ord("ъ"): "", ord("ы"): "y",
                  ord("ё"): "e", ord("є"): "e", ord("і"): "y", ord("ї"): "yi", ord("ґ"): "g",
                  ord("1"): "1", ord("2"): "2", ord("3"): "3", ord("4"): "4", ord("5"): "5", ord("6"): "6", ord("7"): "7", ord("8"): "8", ord("9"): "9", ord("0"): "0"}
    en_name = name.translate(dictionary)
    fin_name = re.sub(r"(\W)", '_', en_name)
    return fin_name

def create_folders(path):
    #dict_keys = list(dict.keys(files)) # Создание папок
    #print (dict_keys)
    for folder in files:
        os.chdir(path)
        folder = str(folder)
        if not os.path.isdir(folder):
            os.makedirs(folder)


def move(path, main_path):      # Перемещение файлов в папки по назначению
    file_list = os.scandir(path)
    #sort_file = list(files.items())
    for el in filter(os.path.isfile, file_list):
        el_moved = False
        sufix = el.name.split(".")[-1]
        file_name = el.name.split(".")[0:-1]
        for key, value in files.items():
            if sufix in value:
                print(f'Moving {el} in {key} folder\n')
                new_el = (normalize("".join(file_name)) + "." + sufix)
                os.replace(el, os.path.join(main_path, key, new_el))
                el_moved = True
                break
        if not el_moved:
            new_el = (normalize("".join(file_name)) + "." + sufix)
            os.replace(os.path.join(path, el), os.path.join(main_path, 'other', new_el))


def folder_sort(path, start_path):  # Рекурсивный проход по папкам
    if not list(filter(os.path.isdir, os.scandir(path))):
        move(path, start_path)
    for dir in filter(os.path.isdir, os.scandir(path)):
        move(path, start_path)
        folder_sort(dir, start_path)
    # for folderName, subfolders, filenames in os.walk(path):
    #     x = len(path)
    #     dict_keys = list(dict.keys(files))
    #     if ("".join(folderName.split("\\")[x: x+1]) in dict_keys) == False:
    #         move(path, path)
    #     for subfolder in subfolders:
    #         if ((subfolder in dict_keys) == False):
    #             move(os.path.join(path, subfolder), path)
            # for filename in filenames:
            #     if folderName != dict_keys:
            #         move(os.chdir(path), path)


x = str ("\\")

# def remove_empty_dirs(path):  # Удаление пустых директорий
#     for folderName, subfolders, filenames in os.walk(path):
#         x = len(path.split("\\"))
#         if (os.path.isdir(folderName) == True) and (os.listdir(folderName) == []) and (("".join(folderName.split("\\")[x: x+1]) in dict_keys) == False):
#             os.rmdir(folderName)
#         for subfolder in subfolders:
#             if (os.path.isdir(subfolder) == True) and (os.listdir(subfolder) == []) and ((folderName in dict_keys) == False):
#                 os.rmdir(subfolder)
#             for filename in filenames:
#                 if (os.path.isdir(filename) == True) and (os.listdir(filename) == []) and ((folderName in dict_keys) == False):
#                     os.rmdir(filename)

def remove_empty_dirs(path):
    result = []
    for item in list(os.walk(path)):
        try:
            os.removedirs(item[0])
            result.append((item[0], True))
            return item[0], True
        except:
            result.append((item[0], True))
    return result
    # if not list(filter(os.path.isfile, os.scandir(path))) and not list(filter(os.path.isdir, os.scandir(path))):
    #     os.rmdir(os.path.join(path))
    # for dir in os.scandir(path):
    #     if os.path.isdir(os.path.join(path, dir)):
    #         remove_empty_dirs(dir)


def unpackArchive (path):
    file_list = os.listdir(f'{path}\\archives')
    for el in file_list:
        name_archiv = os.path.splitext(el)[0]
        shutil.unpack_archive (f'{path}\\archives\\{el}', os.path.join(path, 'archives', name_archiv))


def entry_point():
    try:
        sort_folder = sys.argv[1]
        create_folders(sort_folder)
        folder_sort(sort_folder, sort_folder)
        print(remove_empty_dirs (sort_folder))
        unpackArchive (sort_folder)
    except IndexError as e:
        print(f"Sorry, i can`t do this. Error: {e}")


if __name__ == "__main__":
    entry_point()
