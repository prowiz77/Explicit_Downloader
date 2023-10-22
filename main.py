import os
import re
import sys
import shutil
import appdirs
import requests
import platform
import subprocess
from tkinter import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style
from tkinter import filedialog, PhotoImage

# Funktionen
def link_exists(url):
    response = requests.head(url)
    if response.status_code == 200:
        link_label.config(text="valid link", fg="green")
    else:
        error_code = "url is not valid or service isn't available"
        link_label.config(text=error_code, fg="orange")
def get_user_folder_name():
    folder_name = ''
    return folder_name
def gotanynudes(url):
    url = url
    def vid_crawler(url, folder_name):
        def extract_video_links(url):
            response = requests.get(url)
        
            if response.status_code == 200:
                page_content = response.text
                video_links = set()


                video_extensions = ['mp4', 'mov', 'mpeg', 'gif']
                pattern = r'(https?://[^\s/$.?#].[^\s]*)'
                for ext in video_extensions:
                    pattern += f'\.{ext}|'
                pattern = pattern[:-1]  

                matches = re.finditer(pattern, page_content, re.IGNORECASE)
                for match in matches:
                    video_links.add(match.group(0))

                return video_links

            return None
        
        def download_links_from_file(links_file, download_folder):
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
            with open(links_file, "r") as file:
                for line in file:
                    url = line.strip()
                    if url:
                        os.system('clear')
                        print(f"[{Fore.YELLOW}url{Style.RESET_ALL}] -> {url}")
                        print(f"[{Fore.YELLOW}folder{Style.RESET_ALL}] -> {download_folder}")
                        download_file(url, download_folder)
        
        def download_file(url, folder):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
            
                content_length = response.headers.get('Content-Length')
                if content_length is not None:
                    file_size = int(content_length)
                    print(f"[{Fore.YELLOW}filesize{Style.RESET_ALL}] {file_size} Bytes")

                filename = os.path.join(folder, url.split("/")[-1])
                downloaded_bytes = 0  

                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            downloaded_bytes += len(chunk)

                            if file_size is not None:
                            
                                progress = (downloaded_bytes / file_size) * 100
                                print(f"[{Fore.YELLOW}Download{Style.RESET_ALL}] {Fore.YELLOW}{progress:.2f}%{Style.RESET_ALL}", end='\r')

        
        video_links = extract_video_links(url)

        if video_links:
            with open("links.txt", "w") as file:
                for link in video_links:
                    file.write(link + '\n')
            print(f"{Fore.YELLOW}### {Style.RESET_ALL}{Fore.WHITE}[Progress] Video links saved to 'links.txt'{Style.RESET_ALL}{Fore.YELLOW} ###{Style.RESET_ALL}")

        links_file = "links.txt"  
            
        download_folder = os.path.join("download_files", folder_name)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        download_links_from_file(links_file, download_folder)
        print(f"[{Fore.GREEN}downloaded{Style.RESET_ALL}] -> {download_folder}")
        os.remove("links.txt")
    folder_name = get_user_folder_name()
    vid_crawler(url, folder_name)    
def pornhub(url):
    os.chdir('download_files')
    os.system(f"youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' {url}")
def xhamster(url):
    def rename_to_mp4(folder_path):
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                original_path = os.path.join(folder_path, filename)
                if os.path.isfile(original_path):
                    file_name, file_extension = os.path.splitext(filename)
                    if file_extension != '.mp4':
                        new_extension = '.mp4'
                        new_filename = file_name + new_extension
                        new_path = os.path.join(folder_path, new_filename)
                        os.rename(original_path, new_path)
                        print(f"Renamed: {file_name}{file_extension} to {file_name}{new_extension}")
        else:
            print(f"The folder '{folder_path}' does not exist.")
    def find_and_save_mp4_links(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            mp4_pattern = re.compile(r'https?://.*\.mp4')
            with open('mp4_links.txt', 'w') as mp4_file:
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href and mp4_pattern.search(href):
                        mp4_url = urljoin(url, href)  
                        mp4_file.write(mp4_url + '\n')
            
            print(f"[{Fore.YELLOW}process{Style.RESET_ALL}] -> .mp4-link saved to 'mp4_links.txt'")
        
        except Exception as e:
            print(f'[{Fore.RED}error{Style.RESET_ALL}] Error occured while downloading or analyying element {e}')   
    def download_hamster():
        def get_user_folder_name():
            folder_name = ''
            return folder_name

        def download_mp4_files(links, download_directory):
            if not os.path.exists(download_directory):
                os.makedirs(download_directory)
        
            for link in links:
                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    file_name = link.split("/")[-1]
                    file_path = os.path.join(download_directory, file_name)
                    with open(file_path, 'wb') as mp4_file:
                        mp4_file.write(response.content)
                
                    print(f'[{Fore.GREEN}downloaded{Style.RESET_ALL}] -> file stored in {download_directory}')
            
                except Exception as e:
                    print(f'[{Fore.RED}error{Style.RESET_ALL}] Error while downloading file {e}')

        folder_name = get_user_folder_name()
        script_directory = os.path.dirname(os.path.abspath(__file__))
        download_directory = os.path.join(script_directory, 'download_files', folder_name)
        with open('mp4_links.txt', 'r') as file:
            mp4_links = file.read().splitlines()

        download_mp4_files(mp4_links, download_directory)
        os.remove("mp4_links.txt")
    find_and_save_mp4_links(url)
    download_hamster()
    folder_path = "download_files"
    rename_to_mp4(folder_path)
def xvideos(url_orig):
    def remove_characters_until_https(input_string):
        https_index = input_string.find("https://")
        
        if https_index != -1:
            result_string = input_string[https_index:]
            return result_string
        else:
            return input_string

    def download_link(url, destination):
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(destination, 'wb') as file:
                file.write(response.content)

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] while downloading link: {e}")

    def find_hls_1080p_url(m3u8_file_path):
        try:
            with open(m3u8_file_path, 'r') as file:
                lines = file.readlines()
                for line_number, line in enumerate(lines):
                    if line.strip().startswith("hls-1080p"):
                        return line.strip(), line_number
            return None, -1
        except FileNotFoundError:
            print(f"[ERROR] file {m3u8_file_path} not found.")
            return None, -1

    def replace_characters(input_string, replacement):
        return input_string.replace('hls.m3u8', replacement)

    def filter_hls_lines(input_file_path, output_file_path):
        try:
            with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                for line in input_file:
                    if line.strip().startswith("hls"):
                        output_file.write(line)
            
        except FileNotFoundError:
            print(f"[ERROR] file {input_file_path} not found.")

    def remove_hls_m3u8_from_link(link):
        new_link = link.replace('hls.m3u8', '')
        return new_link

    def insert_link_to_each_line(file_path, new_link, output_file_path):
        try:
            with open(file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                for line in input_file:
                    updated_line = new_link + line
                    output_file.write(updated_line)
            
        except FileNotFoundError:
            print(f"[ERROR] file {file_path} not found.")

    def download_links_from_file(file_path, download_directory):
        try:
            with open(file_path, 'r') as file:
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if line:
                        try:
                            response = requests.get(line, stream=True)
                            response.raise_for_status()

                            file_name = f"{line_number}.ts"
                            file_path = f"{download_directory}/{file_name}"

                            with open(file_path, 'wb') as downloaded_file:
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        downloaded_file.write(chunk)

                            print(f"File {file_name} downloaded")
                        except requests.exceptions.RequestException as e:
                            print(f"[ERROR] while downloading line {line_number}: {e}")
            
        except FileNotFoundError:
            print(f"[ERROR] file {file_path} not found")

    def combine_ts_files(input_folder, output_file):
        
        ts_files = [f for f in os.listdir(input_folder) if f.endswith('.ts')]
        ts_files.sort(key=lambda x: int(x.split('.')[0]))

        if not ts_files:
            print("[ERROR] no .ts-File in folder found.")
            return

        
        with open('filelist.txt', 'w') as filelist:
            for ts_file in ts_files:
                filelist.write(f"file '{os.path.join(input_folder, ts_file)}'\n")

    
        os.system(f"ffmpeg -f concat -safe 0 -i filelist.txt -c copy {output_file}")

    
        os.remove('filelist.txt')

        

    def ts_to_mp4(input_ts_file, output_mp4_file):
        try:
            cmd = f'ffmpeg -i {input_ts_file} -c:v copy -c:a aac -strict experimental -y {output_mp4_file}'
            subprocess.run(cmd, shell=True, check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] while converting file {input_ts_file}: {e}")

    def get_title_from_link(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            return title
        except Exception as e:
            print(f"[ERROR] while fetching title: {e}")
            return None

    def entferne_sonderzeichen(text):
        return re.sub(r'[^A-Za-z0-9\s]', '', text)

    def entferne_leerzeichen(text):
        return text.replace(" ", "")
    #----------------get_link_hls.m3u8----------------------------------------
    if not os.path.exists('download_files'):
        os.mkdir('download_files')
    os.chdir('download_files')
    os.mkdir('ts_downloads')

    user_input = url_orig
    title = get_title_from_link(user_input)
    if title:
        print(f"[title] {title}")
    else:
        print("[ERROR] title not found")
    response = requests.get(user_input)
    html_content = response.text


    pattern = r'(.*?hls\.m3u8)'


    matches = re.findall(pattern, html_content)

    if matches:
        for match in matches:
            print("Found link for hls.m3u8-File:", match)
    else:
        print("[ERROR] no hls.m3u8-File found in source-code.")

    #----------------print_link_hls.m3u8--------------------------------------
    result = remove_characters_until_https(match)
    print(result)
    #----------------download_link_hls.m3u8-----------------------------------
    url = result  
    ziel_datei = "hls.m3u8"
    download_link(url, ziel_datei)
    #----------------read_hls.m3u8--------------------------------------------

    available_resolutions = {}  

    with open("hls.m3u8", 'r') as hls_file:
        lines = hls_file.readlines()
        resolution = None

        for line in lines:
            if line.startswith("#EXT-X-STREAM-INF"):
                
                resolution = re.search(r'RESOLUTION=(\d+x\d+)', line).group(1)
            elif line.startswith("hls-"):
                
                available_resolutions[resolution] = line.strip()


    highest_resolution = max(available_resolutions.keys(), key=lambda x: int(x.split('x')[0]))


    selected_m3u8_file = available_resolutions[highest_resolution]
    download_link(selected_m3u8_file, selected_m3u8_file)
    print(f"highest resolution: ",{highest_resolution}) 

    result = remove_characters_until_https(match)
    input_string = result
    replacement = selected_m3u8_file
    result3 = replace_characters(input_string, replacement)
    
    #----------------download_hls-highest-quality.m3u8----------------------------------
    url = result3  
    ziel_datei = selected_m3u8_file
    download_link(url, ziel_datei)
    #----------------edit_hls-highest-quality.m3u8--------------------------------------
    input_file_path = selected_m3u8_file  
    output_file_path = "new_hls.m3u8"

    filter_hls_lines(input_file_path, output_file_path)
    #----------------download-.ts-files-from-new_hls.m3u8---------------
    link = result
    new_link = remove_hls_m3u8_from_link(link)
    

    file_path = "new_hls.m3u8"
    new_link = new_link
    output_file_path = "link_plus_new_hls.m3u8"

    insert_link_to_each_line(file_path, new_link, output_file_path)

    file_path = "link_plus_new_hls.m3u8"
    download_directory = "ts_downloads"

    download_links_from_file(file_path, download_directory)
    #----------------combine_ts_files_into_mp4_file---------------------------
    input_folder = download_directory
    output_file = 'movie.ts'
    combine_ts_files(input_folder, output_file)

    input_ts_file = 'movie.ts'
    output_mp4_file = title
    output_mp4_file_new = entferne_leerzeichen(entferne_sonderzeichen(output_mp4_file) + '.mp4')
    ts_to_mp4(input_ts_file, output_mp4_file_new)
    #----------------delete_files---------------------------------------------
    os.remove('hls.m3u8')
    os.remove(selected_m3u8_file)
    os.remove('link_plus_new_hls.m3u8')
    os.remove('new_hls.m3u8')
    os.remove('movie.ts')
    shutil.rmtree('ts_downloads')

    subprocess.run(["rm", "-rf", "~/.local/share/Trash"])
def xnxx(url):
    xvideos(url)
def get_video_folder():
    video_folder = appdirs.user_data_dir(appname='ExplicitDownloader', appauthor=False)
    return video_folder
def download_file():
    url = link_field.get()  
    video_folder = get_video_folder()
    link_exists(url)

    os.makedirs(video_folder, exist_ok=True)

    if re.search(r'gotanynudes\.com', url):
        canvas.create_image(250, 80, image=logo_img_hex333366)
        canvas.create_image(250, 80, image=logo_img_gotanynudes)
        gotanynudes(url)
    elif re.search(r'pornhub\.com', url):
        canvas.create_image(250, 80, image=logo_img_hex333366)
        canvas.create_image(250, 80, image=logo_img_pornhub)
        pornhub(url)
    elif re.search(r'xhamster\.com', url):
        canvas.create_image(250, 80, image=logo_img_hex333366)
        canvas.create_image(250, 80, image=logo_img_xhamster)
        xhamster(url)
    elif re.search(r'xvideos\.com', url):
        canvas.create_image(250, 80, image=logo_img_hex333366)
        canvas.create_image(250, 80, image=logo_img_xvideos)
        xvideos(url)
    elif re.search(r'xnxx\.com', url):
        canvas.create_image(250, 80, image=logo_img_hex333366)
        canvas.create_image(250, 80, image=logo_img_xnxx)
        xnxx(url)
    else:
        link_label.config(text="Unknown URL", fg="red", bg="#333366")

# -------------------------------------------------------------------------------
# TKinter-Setup
screen = Tk()
title = screen.title("Explicit Downloader")
canvas = Canvas(screen, width=500, height=500, bg="#333366")
canvas.pack()

# -------------------------------------------------------------------------------
# Bild-Logos
logo_img_main = PhotoImage(file="logos/explicit2.png",)
logo_img_main = logo_img_main.subsample(4, 4)

logo_img_hex333366 = PhotoImage(file="logos/333366.png")
logo_img_hex333366 = logo_img_hex333366.subsample(2, 2)

logo_img_gotanynudes = PhotoImage(file="logos/gotanynudes.png")
logo_img_gotanynudes = logo_img_gotanynudes.subsample(2, 2)

logo_img_pornhub = PhotoImage(file="logos/pornhub.png")
logo_img_pornhub = logo_img_pornhub.subsample(8, 8)

logo_img_xhamster = PhotoImage(file="logos/xhamster.png")
logo_img_xhamster = logo_img_xhamster.subsample(12, 12)

logo_img_xvideos = PhotoImage(file="logos/xvideos.png")
logo_img_xvideos = logo_img_xvideos.subsample(12, 12)

logo_img_xnxx = PhotoImage(file="logos/xnxx.png")
logo_img_xnxx = logo_img_xnxx.subsample(12, 12)

# Standard-Logo
canvas.create_image(250, 80, image=logo_img_main)

# -------------------------------------------------------------------------------
# Link-Feldf
link_field = Entry(screen, width=50, fg="white", bg="#575791")
link_label = Label(screen, text="input download-link: ", fg="white", bg="#333366")

# Widgets zum Fenster hinzufügen
canvas.create_window(250, 170, window=link_label)
canvas.create_window(250, 220, window=link_field)

# -------------------------------------------------------------------------------
# Download-Button
download_btn = Button(screen, text="download", command=download_file)
canvas.create_window(250, 390, window=download_btn)

# -------------------------------------------------------------------------------
screen.mainloop()
