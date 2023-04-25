from YoutubeScrape import getVideoUrls, download, show_title_views_and_likes
from selenium import webdriver
from tkinter import *
from threading import Thread
from selenium.webdriver.firefox.options import Options


def update_text(text_widget, message):
    text_widget.insert(END, message)
    text_widget.see(END)

def update_text(text_widget, message):
    text_widget.insert(END, message)
    text_widget.see(END)


def ScrapeVideos():
    global URLS, path

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    search_key_word = keyword_entry.get()
    num_videos = int(nvideos_entry.get())
    path = path_entry.get()

    download_button.config(state=DISABLED)

    update_text(text_widget, f"Searching for {num_videos} videos related to '{search_key_word}'...\n")

    def search_videos():
        global URLS

        URLS = getVideoUrls(driver, search_key_word, num_videos)

        update_text(text_widget, f"Found {len(URLS)} videos!\n")

        video_datas = show_title_views_and_likes(driver, URLS)
        update_text(text_widget, "\nTitle, Views and Likes of the videos: \n")
        for video_data in video_datas:
            update_text(text_widget, video_data)

        download_button.config(state=NORMAL)

    Thread(target=search_videos).start()

def start_download():
    global URLS
    download_button.config(state=DISABLED)
    update_text(text_widget, "Downloading, this may take some minutes. Please wait till the end...\n")

    def download_videos():
        global URLS
        download(URLS, path)
        update_text(text_widget, "Download was successful!\n")
        download_button.config(state=NORMAL)

    Thread(target=download_videos).start()

root = Tk()
root.title("YouTube Video Scraper")
root.geometry("600x400")
root.configure(bg="#ADD8E6")


keyword_label = Label(root, text="Enter keyword to search:", font=("Arial", 12), bg="#f1c40f")
keyword_label.pack()
keyword_entry = Entry(root, font=("Arial", 12))
keyword_entry.pack()


nvideos_label = Label(root, text="How many videos to download?", font=("Arial", 12), bg="#f1c40f")
nvideos_label.pack()
nvideos_entry = Entry(root, font=("Arial", 12))
nvideos_entry.pack()


path_label = Label(root, text="Where do you want to save?", font=("Arial", 12), bg="#f1c40f")
path_label.pack()
path_entry = Entry(root, font=("Arial", 12))
path_entry.pack()

scrape_button = Button(root, text="Scrape", font=("Arial", 12), bg="#2980b9", fg="white", command=ScrapeVideos)
scrape_button.pack()

download_button = Button(root, text="Download", state=DISABLED, font=("Arial", 12), bg="#2980b9", fg="white", command=start_download)
download_button.pack()


text_widget = Text(root)
text_widget.pack()



root.mainloop()