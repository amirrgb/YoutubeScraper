from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import re

def getVideoUrls(driver,Input,nVideos):
    search = Input.replace(' ','+')
    driver.get(f"https://www.youtube.com/results?search_query={search}")

    Count = 0
    URLS = []

    while Count != nVideos:
        videos = driver.find_elements(By.XPATH,"//*[@id=\'video-title\']")
        for video in videos:
            link = video.get_attribute("href")

            if link not in URLS and link != None:
                URLS.append(link)
                Count = Count+1

                if Count >= nVideos:
                    break

        driver.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.CONTROL, Keys.END)

    return URLS


def download(urls, path):
    n = len(urls)
    count = 0
    for url in urls:
        try:
            process = subprocess.Popen(f"yt-dlp -q --progress -P {path} {url}")

            stdout, stderr = process.communicate()

            if stdout:
                for line in stdout.splitlines():
                    pattern = re.compile("([0-9]{1,3})%")
                    matcher = pattern.search(line)
                if matcher and int(matcher.group(1)) == 100:
                    count += 1
                    print(f"{count} out of {n} videos downloaded")
                print(line)

            if stderr:
                print("Here is the standard error of the command (if any):\n")
                print(stderr)
        except subprocess.CalledProcessError as err:
            print(err)


def shownames_and_likes(driver,urls):
    for url in urls:
        driver.get(url)

        driver.implicitly_wait(10)

        video_title = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[1]/h1/yt-formatted-string').text

        view_count = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[3]/div[1]/div/div/yt-formatted-string/span[1]').text

        likes = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/div[1]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span").text

        print(f"title: {video_title}, views:{view_count}, likes: {likes}")
    driver.close()


driver = webdriver.Firefox()
URLS = getVideoUrls(driver,"test",2)
download(URLS,"F:\ForTest")
shownames_and_likes(driver,URLS)