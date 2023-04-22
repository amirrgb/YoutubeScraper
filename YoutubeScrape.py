from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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
    driver.close()
    return URLS

driver = webdriver.Firefox()
URLS = getVideoUrls(driver,"test",5)
for url in URLS:
    print(url)