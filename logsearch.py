import tkinter as tk
from tkinter import filedialog
import os
import time

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Bir klasör seçin")
    return folder_path

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Bir dosya seçin", filetypes=[("Text files", "*.txt")])
    return file_path

def case_insensitive_search(term, line):
    return term.lower() in line.lower()

def search_and_save(folder_path, search_term):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    result_file_path = os.path.join(current_directory, f"{search_term.replace(' ', '_')}.txt")

    start_time = time.time()
    try:
        with open(result_file_path, 'w', encoding='utf-8') as result_file:
            for root_dir, dirs, files in os.walk(folder_path):
                for file_name in files:
                    if file_name.endswith('.txt'):
                        file_path = os.path.join(root_dir, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                for line in file:
                                    if case_insensitive_search(search_term, line):
                                        result_file.write(line)
                        except UnicodeDecodeError:
                            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                                for line in file:
                                    if case_insensitive_search(search_term, line):
                                        result_file.write(line)
        elapsed_time = time.time() - start_time
        print(f"Arama sonuçları '{result_file_path}' dosyasına kaydedildi.")
        print(f"Arama süresi: {elapsed_time:.2f} saniye")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def clear_and_format_user_pass(file_path):
    formatted_lines = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                cleaned_line = line.strip()
                if '://' in cleaned_line:
                    cleaned_line = cleaned_line.split(' ')[-1]
                parts = cleaned_line.split(':')
                if len(parts) >= 2:
                    username = parts[-2].strip()
                    password = parts[-1].strip()
                    if username and password:
                        formatted_lines.add(f"{username}:{password}")

        output_file_path = os.path.splitext(file_path)[0] + '_formatted_user_pass.txt'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for formatted_line in formatted_lines:
                output_file.write(formatted_line + '\n')

        print(f"Veriler '{output_file_path}' dosyasına temizlenmiş olarak kaydedildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__": 
    folder_path = None  

    while True:
        print("\n1. Klasör seç")
        print("2. Arama yap")
        print("3. Dosyayı user:pass formatında temizle ve formatla")
        print("4. Çıkış yap")
        choice = input("Seçiminizi yapın (1/2/3/4): ")

        if choice == '1':
            folder_path = select_folder()
            if folder_path:
                print(f"'{folder_path}' klasörü seçildi.")
            else:
                print("Hiçbir klasör seçilmedi.")
        elif choice == '2':
            if not folder_path:
                print("Önce bir klasör seçmeniz gerekiyor.")
            else:
                search_term = input("Aramak istediğiniz kelimeyi girin: ")
                if search_term.strip():
                    search_and_save(folder_path, search_term)
                else:
                    print("Arama terimi boş olamaz.")
        elif choice == '3':
            file_path = select_file()
            if file_path:
                clear_and_format_user_pass(file_path)
            else:
                print("Hiçbir dosya seçilmedi.")
        elif choice == '4':
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçim.")
