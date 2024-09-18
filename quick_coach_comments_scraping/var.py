import datetime
import os
import platform

os_type = platform.system()

if os_type == "Windows":
    executablePath = "chromedriver.exe"
elif os_type == "Darwin":
    executablePath = "chromedriver"


now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d_%H-%M-%S")

base_directory = "logs/"

terminalLogFilePath = f"{base_directory}terminalLog.txt"
logFilePath = f"{base_directory}log.txt"
output_file = f"{base_directory}{current_date}_cilents.csv"
