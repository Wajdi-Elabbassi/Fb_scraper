#imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from time import sleep
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import pandas as pd


driver_service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")

#code by pythonjar, not me
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

#initialisation
content_list=[]
time_list=[]
name_list=[]

#specify the path to chromedriver.exe 
driver = webdriver.Chrome(service = driver_service)



#open the webpage
driver.get("http://www.facebook.com")
driver.maximize_window()

#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

#enter username and password of the account you're using here
username.clear()
username.send_keys("scraper@gmail.com")
password.clear()
password.send_keys("scraper123")

#target the login button and click it
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
#We are logged in!


#Enter the url of the page to scape in mbasic format
sleep(1)
driver.get("https://mbasic.facebook.com/url")

sleep(1)
link = driver.find_element_by_link_text("Journal")
link.click()
#Page loaded


soup=BeautifulSoup(driver.page_source,"html.parser")

feed = soup.find("section")

all_posts = feed.find_all("article")
for post in all_posts:
    names=post.find("h3",{"class":"_52ja _52jh _4vc- _lqt"})
    namel=names.text.split("<strong>")

    times=post.find("div",{"class":"mfss fcg"})
    time=times.text.split("<abbr>")
    timel=time[0].split(' · ')[0]

    contents = post.find("div",{"class":"_5rgn"})
    content = contents.find("span")
    contentl = content.text.split("<p>")

    content_list.append(contentl)
    time_list.append(time)
    name_list.append(namel)


sleep(5)
df=pd.DataFrame({"name":name_list,"content":content_list,"time":time_list})

#choose the name of the csv file in the output
df.to_csv("data.csv") 
driver.quit()