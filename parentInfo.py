
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
import var
from datetime import datetime
from os.path import basename



url = os.environ['DemoReporturl']
username = os.environ['DemoReportus']
password = os.environ['DemoReportpa']
lea = os.environ['DemoReportex']


def DemoReport():
    driver = webdriver.Chrome()
    driver.get(url);
    user = driver.find_element(By.NAME,'Username')
    passw = driver.find_element(By.NAME,'Password')
    user.clear()
    user.send_keys(username)
    passw.clear()
    passw.send_keys(password)
    passw.send_keys(Keys.RETURN)
    driver.get(lea)
    xpath = ['//*[@id="include-options"]/legend/button[1]',
             '/html/body/div[3]/div[2]/div[2]/form/fieldset/label[4]',
             '/html/body/div[3]/div[2]/div[2]/form/div/fieldset[1]/legend/button[1]',
            '//*[@id="content"]/div[2]/form/div/fieldset[1]/legend/button[2]',
            '//*[@id="generate"]']
    seconds = 0
    dl_wait = True
    now = datetime.now()
    today = now.strftime("%Y%m%d")
    path_to_downloads = os.path.expanduser("~")+"/Downloads/"
    
    for x in xpath:
        button = driver.find_element(By.XPATH, x)
        button.click()
    

    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
        
    driver.close()
    path = path_to_downloads +"StudentDemographicExport_" + today + ".csv"
    return path
