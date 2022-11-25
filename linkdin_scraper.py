import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from parsel import Selector

import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  
# Chrome driver install
driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')
sleep(5)
# getting the variables name and login
username = driver.find_element(By.CLASS_NAME, 'input__input')
username.send_keys('rfortney@hotmail.com ') # username field

password = driver.find_element(By.NAME, 'session_password')
password.send_keys('Pu6zjGqA') # password field
sleep(3)
log_in_button = driver.find_element(By.CLASS_NAME,'sign-in-form__submit-button') # submit button
log_in_button.click() # click the submit button
sleep(2)
# Making the google query
driver.get('https://www.google.com/')
search_bar = driver.find_element(By.NAME, 'q')
search_bar.send_keys('site:linkedin.com/in/ AND "python" AND "Django"')


search_bar.send_keys(Keys.ENTER) # Automating the enter key

# Saving the linkedin users urls in an array to do the scraping

profile_urls = []
a=1
for page in range(0,13):
    while a <= page:
        linkedin_users_urls_list = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]/a[@href]')
        [profile_urls.append(users.get_attribute("href")) for users in linkedin_users_urls_list]
        driver.find_element(By.XPATH,"//*[contains(local-name(), 'span') and contains(text(), 'Next')]").click()
        a = a+1




# To check the list content we run the following command
# [profile_urls.append(users.get_attribute("href")) for users in linkedin_users_urls_list]

fields = ['Name','Job Title','Company','University','Location','followers','connections','URL']
sel = Selector(text=driver.page_source)
# What we need from the profile


with open('results.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(fields)
    for profiles in profile_urls:
        driver.get(profiles)
        sel = Selector(text=driver.page_source)
        sleep(3)
        name = sel.xpath('.//*[starts-with(@class, "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0")]/text()').extract_first()
        if name:
            name = name.strip()
        else:
            name = None
        job_title = sel.xpath('.//h2[starts-with(@class, "top-card-layout__headline break-words font-sans text-md leading-open text-color-text")]/text()').extract_first()
        if job_title:
            job_title = job_title.strip()
        else:
            job_title = None
        company = sel.xpath('.//*[@data-section="currentPositionsDetails"]/div/span/text() | .//*[@data-section="currentPositionsDetails"]/a/span/text()').extract_first()
        if company:
            company = company.strip()
        else:
            company = None
        university = sel.xpath('.//*[@data-section="educationsDetails"]/div/span/text() | .//*[@data-section="educationsDetails"]/a/span/text()').extract_first()
        if university:
            university = university.strip()
        else:
            university = None
        location = sel.xpath('.//h3[@class="top-card-layout__first-subline font-sans text-md leading-open text-color-text-low-emphasis"]/div/text()').extract_first()
        if location:
            location = location.strip()
        else:
            location = None
        linkedin_url = driver.current_url
        
        followers = sel.xpath('.//h3[@class="top-card-layout__first-subline font-sans text-md leading-open text-color-text-low-emphasis"]/span[1]/text()').extract_first()
        if followers:
            followers = followers.strip('followers')
        else:
            followers = None

        connections = sel.xpath('.//h3[@class="top-card-layout__first-subline font-sans text-md leading-open text-color-text-low-emphasis"]/span[2]/text()').extract_first()
        if connections:
            connections = connections.strip('connections')
        else:
            connections = None    

        writer.writerow([name, job_title, company, university, location,followers,connections,linkedin_url])
    
