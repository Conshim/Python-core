import os
import glob
import shutil
import unicodedata
import sys

def normalize(filename):
    cleaned_filename = unicodedata.normalize('NFD', filename).encode('ascii', 'ignore').decode("utf-8")
    cleaned_filename = ''.join(c if c.isalnum() else '_' for c in cleaned_filename)
    return cleaned_filename

file_formats = {   
    'jpeg': "images",
    'png': "images",
    'jpg': "images",
    'svg': "images",
    'avi': "video",
    'mp4': "video",
    'mov': "video",
    'mkv': "video",
    'gif': "video",
    'doc': "document",
    'docx': "document",
    'txt': "document",
    'pdf': "document",
    'xlsx': "document",
    'pptx': "document",
    'pdf': "document",
    'mp3': "music",
    'ogg': "music",
    'wav': "music",
    'amr': "music",
    'zip': "archive",
    'gz': "archive",
    'tar': "archive"
}

def delete_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):  
                os.rmdir(folder_path)
                print(f"Видалено порожню папку: {folder_path}")
            else:
                filse_to_move = os.listdir(folder_path)
                for file in filse_to_move:
                    src = os.path.join(folder_path, file)
                    dst = os.path.join(path, file)
                    if os.path.isfile(src):
                        shutil.move(src, dst)
                        print(f"Переміщений файл: {file} з {folder_path} до {path}") 
                os.rmdir(folder_path)
                print(f"Видалено непорожню папку та переміщено її вміст до {path}")

        
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print(f"Використовуйте: python sort.py {sys.argv}") 
        sys.exit (1)

    path=sys.argv[1]

if not os.path.exists(path):
    print("Вказаний шлях не існує.")
    sys.exit(1) 

if not os.path.isdir(path): 
    print("Вказаний шлях не є папкою.")
    sys.exit (1)


delete_empty_folders(path)

for file_format, folder_name in file_formats.items():
    files = glob.glob(os.path.join(path, f"*.{file_format}"))
    print(f"Знайдено {len(files)} файл(-ов) з розширенням {file_format}.")
    if not os.path.isdir(os.path.join(path, folder_name)) and files: 
        os.mkdir(os.path.join(path, folder_name))
        print(f"Створена папка {folder_name}")

for file_format, folder_name in file_formats.items():
    files = glob.glob(os.path.join(path, f"*.{file_format}"))

    for file in files: 
        basename = os.path.basename(file)
        cleaned_basename = normalize(basename)
        name, ext = os.path.splitext(cleaned_basename)
        dst = os.path.join(path, folder_name, f"{name}.{file_format}")
        print(f"Перейменований файл {basename} в {cleaned_basename}")
        print(f"Перенесений файл {file} в {dst}")
        shutil.move(file, dst)

other_folder = os.path.join(path, 'other')
if not os.path.isdir(other_folder):
    os.mkdir(other_folder)
    print("Створена папка other для залишених файлів")

remaining_files = [f for f in glob.glob(os.path.join(path, "*")) if os.path.isfile(f)]
for file in remaining_files:
    if file != sys.argv[0]:  
        basename = os.path.basename(file)
        cleaned_basename = normalize(basename)
        dst = os.path.join(other_folder, cleaned_basename)
        print(f"Перенесений файл {file} в {dst} (в папку other)")
        shutil.move(file, dst)

input("Натисніть Enter, щоб закрити програму...")
