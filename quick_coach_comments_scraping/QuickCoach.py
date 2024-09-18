import csv
import os
import time
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from var import (base_directory, executablePath, logFilePath, output_file,
                 terminalLogFilePath)


def goEndOfPage(driver):
    driver.find_element(By.XPATH, "//body").send_keys(Keys.END)
    time.sleep(1)


def startSession():
    option = webdriver.ChromeOptions()
    option = workOption(option)
    caps = DesiredCapabilities().CHROME
    s = Service(executablePath)
    caps["pageLoadStrategy"] = "normal"
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(service=s, options=option, desired_capabilities=caps)
    driver.maximize_window()
    return driver


def loadUrl(driver):
    while True:
        try:
            driver.get("https://app.quickcoach.fit/login")
            time.sleep(3)
            return driver
        except Exception as e:
            log("Error in loadUrl : " + str(e))
            time.sleep(3)
            continue


def workOption(option):
    option.add_argument("--start-maximized")
    option.add_argument("disable-infobars")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--disable-gpu")
    option.add_argument("--no-sandbox")
    # option.add_argument('--ignore-certificate-errors')
    # option.add_argument("headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    chromePrefers = {}
    option.experimental_options["prefs"] = chromePrefers
    chromePrefers["profile.default_content_settings"] = {"images": 2}
    chromePrefers["profile.managed_default_content_settings"] = {"images": 2}
    return option


def login():
    while True:
        try:
            if "ok" in input(
                "Please enter 'ok' when you have successfully logged in: "
            ):
                print("Alright, let's go...")
                break
        except Exception as e:
            log(
                "Whoops, looks like there's a glitch in the login, try again..."
                + str(e)
            )
            time.sleep(3)
            continue


def goToClientsPart(driver):
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[2]/li[2]/div"))
            ).click()
            time.sleep(3)
            break
        except Exception as e:
            log("Error in goToClientsPart method : " + str(e))
            time.sleep(3)
            continue


def log(logText):
    print(logText)
    print(logText, file=open(terminalLogFilePath, "a"))
    print(logText, file=open(logFilePath, "a"))


def getRows(driver):
    rows = driver.find_elements(By.XPATH, "//tbody//tr")
    return rows


def goToEachClientPage(driver):
    # this loop for waiting until the page is loaded
    while True:
        lenOfPages = len(driver.find_elements(By.XPATH, "//tfoot//nav/ul//li")) - 2
        if lenOfPages == -2:
            time.sleep(3)
            print("Connecting...")
            continue
        else:
            break

    print("len of pages : ",lenOfPages)
    for pageNumber in range(lenOfPages):
        print("Page",pageNumber+1,">>>>>>>>>>>>>",len(getRows(driver))," rows")
        rowNumber = 1
        for row in getRows(driver):
            print("row",rowNumber," : ",row.text)
            client = row.find_element(By.XPATH, "./td[1]").text
            pending_plans = row.find_element(By.XPATH, "./td[2]").text
            last_plan = row.find_element(By.XPATH, "./td[3]").text
            last_comment = row.find_element(By.XPATH, "./td[4]").text
            insertClientToCSV(client, pending_plans, last_plan, last_comment)
            rowNumber+=1
        print("one page collected","this is page ",pageNumber+1)
        if pageNumber != lenOfPages - 1:
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//tfoot//nav/ul/li[last()]/button")
                    )
                ).click()
                time.sleep(3)
                if "ok" in input("go next page ?"):
                    print("ok lets collect")
            except Exception as e:
                log("Error in goToEachClientPage method: " + str(e))
                time.sleep(3)
                continue


def insertClientToCSV(client, pending_plans, last_plan, last_comment):
    with open(output_file, "a", newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow([client, pending_plans, last_plan, last_comment])


def main():
    if os.path.exists(output_file):
        os.remove(output_file)

    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    if not os.path.exists(output_file):
        insertClientToCSV("client", "pending_plans", "last_plan", "last_comment")

    start = datetime.now()
    log("Start time: " + str(start))
    driver = startSession()
    driver = loadUrl(driver)
    login()
    goToClientsPart(driver)
    goToEachClientPage(driver)
    end = datetime.now()
    log("End time: " + str(end) + " Total time: " + str(end - start))
    driver.close()


main()
