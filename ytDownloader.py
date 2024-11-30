import os
import platform
import time
import yt_dlp

def clear_screen():
    os.system("cls")  

def home():
    clear_screen()
    print("\033[31mYouTube Video Downloader\033[0m")
    print("1. Download Video \n2. See Download History \n3. Delete Downloaded Video \n4. Exit")
    choice = input("> ").strip().lower()
    
    if choice == "1":
        download_video()
    elif choice == "2":
        view_history()
    elif choice == "3":
        delete_video()
    elif choice == "4":
        print("\033[33mExiting the program...\033[0m")
        time.sleep(1)
        clear_screen()
        exit()
    else:
        print("\033[31mInvalid input. Returning to menu...\033[0m")
        time.sleep(2)
        home()

def download_video():
    clear_screen()
    url = input("Enter the YouTube Video URL: ").strip()
    ydl_opts = {
        'format': 'best',  
        'outtmpl': '%(title)s.%(ext)s',  
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get("title", "Unknown Title")
            views = info_dict.get("view_count", 0)
            filename = ydl.prepare_filename(info_dict)
            
            print("\n\033[32mVideo Details:\033[0m")
            print(f"Title      : {title}")
            print(f"Views      : {views:,}")
            print(f"File Name  : {filename}")
            print("\033[32mDownloading...\033[0m")
            
            ydl.download([url])

            print("\033[32mDownload complete!\033[0m")
            
            with open("history.yt", "a+", encoding="utf-8") as f:
                f.write(f"Video URL  : {url}\n")
                f.write(f"Title      : {title}\n")
                f.write(f"Views      : {views:,}\n")
                f.write(f"File Name  : {filename}\n")
                f.write("-" * 30 + "\n")

            time.sleep(2)
            home()
    except Exception as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")
        time.sleep(2)
        home()

def view_history():
    clear_screen()
    if not os.path.exists("history.yt"):
        print("\033[31mNo download history found.\033[0m\n")
    else:
        with open("history.yt", "r", encoding="utf-8") as f:
            history = f.read()
            if history.strip() == "":
                print("\033[31mNo download history found.\033[0m\n")
            else:
                print("\033[32mDownload History:\033[0m\n")
                print(history)
    input("\nPress Enter to return to menu...")
    home()

def delete_video():
    clear_screen()
    print("\033[31mDelete Downloaded Videos\033[0m\n")
    files = [f for f in os.listdir() if os.path.isfile(f)]
    video_files = [f for f in files if f.endswith((".mp4", ".mkv", ".webm", ".flv", ".avi"))]

    if not video_files:
        print("\033[31mNo video files found in the current directory.\033[0m\n")
    else:
        print("\033[32mAvailable Video Files:\033[0m")
        for idx, file in enumerate(video_files, start=1):
            print(f"{idx}. {file}")

        print("\nEnter the number of the file you want to delete, or '0' to cancel.")
        choice = input("> ").strip()

        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(video_files):
                file_to_delete = video_files[choice - 1]
                try:
                    os.remove(file_to_delete)
                    print(f"\033[32mFile '{file_to_delete}' deleted successfully.\033[0m")

                    if os.path.exists("history.yt"):
                        with open("history.yt", "r", encoding="utf-8") as f:
                            lines = f.readlines()
                        with open("history.yt", "w", encoding="utf-8") as f:
                            skip = False
                            for line in lines:
                                if f"File Name  : {file_to_delete}" in line:
                                    skip = True
                                elif skip and line.strip() == "-" * 30:
                                    skip = False
                                elif not skip:
                                    f.write(line)

                    print("\033[32mRelated history entry removed successfully.\033[0m")
                except Exception as e:
                    print(f"\033[31mError deleting file: {e}\033[0m")
            elif choice == 0:
                print("\033[33mDeletion canceled. Returning to menu...\033[0m")
            else:
                print("\033[31mInvalid choice. Returning to menu...\033[0m")
        else:
            print("\033[31mInvalid input. Returning to menu...\033[0m")
    time.sleep(2)
    home()

if __name__ == "__main__":
    home()
