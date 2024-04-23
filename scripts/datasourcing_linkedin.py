#data sourcing script
#create a .csv file with the data scraped from the third website

#libraries
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import csv
import os
import numpy as np
import pandas as pd

import ast

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re


import warnings 
warnings.filterwarnings("ignore")

#Scrapping LinkedIn Companies

file_path = 'liste_linkedin_entreprise.txt'
csv_file_path = 'entreprise_linkedin.csv'
progress_file_path = 'progress_linkedin_entreprise.txt'

def read_progress(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            line = f.readline()
            if line:
                return int(line.strip()) + 1
    return 0  

def save_progress(file_path, progress):
    with open(file_path, 'w') as f:
        f.write(str(progress))

  
with open(file_path, 'r') as file:
    content = file.read()

liste = content.split('\n')

liste_linkedin = []
for i in range(len(liste)):
    liste_linkedin.append(liste[i].replace(' ','%20'))

def read_progress(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            line = f.readline()
            if line:
                return int(line.strip()) + 1
    return 0  


def save_progress(file_path, progress):
    with open(file_path, 'w') as f:
        f.write(str(progress))

columns = ['company_name','linkedin_company_url', 'site_web', 'taille']
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# see progression with tqdm starting from the last page
driver.get(f"https://www.linkedin.com/search")
cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]')))
cookie_button.click()

mail = 'email'
password = 'password'  

login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
password_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
connect_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')))

login_button.send_keys(mail)
password_button.send_keys(password)
connect_button.click()

start_from = read_progress(progress_file_path)

for i, company in enumerate(tqdm(liste_linkedin[start_from:]), start=start_from):

    driver.get(f"https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22105015875%22%5D&industryCompanyVertical=%5B%2247%22%5D&keywords={company}&origin=FACETED_SEARCH&sid=%3AbD")
    try : 
        first_link_company_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="search-results-container"]/div[2]/div/ul/li[1]/div//*[@class="display-flex"]')))
        first_link_company_button.click()
        try:
            a_propos_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'org-page-navigation__item') and .//text()='À propos']//a")))
            a_propos_button.click()
            linkedin_company_url = driver.current_url
            a_propos_element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//*[@class = 'overflow-hidden']")))
            a_propos = a_propos_element.text.split('\n')
            try :
                index = a_propos.index('Site web')
                site_web = a_propos[index+1]
            except:
                site_web = np.nan
            try:
                index = a_propos.index('Taille de l’entreprise')
                taille = a_propos[index+1]
            except:
                taille = np.nan

            data = {'linkedin_company_url':linkedin_company_url,
                    'site_web':site_web,
                    'taille':taille,
                    'company_name': liste[i]}

        except:
                data = {'linkedin_company_url':linkedin_company_url,
                    'site_web':np.nan,
                    'taille':np.nan,
                    'company_name': liste[i]}
    except:
        data = {'linkedin_company_url':np.nan,
                'site_web':np.nan,
                'taille':np.nan,
                'company_name': liste[i]}
          

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=columns)
                        writer.writerow(data)
                        
    save_progress(progress_file_path, i)


#Scraping LinkedIn profiles
csv_file_path = 'profil_linkedin.csv'
progress_file_path = 'progress_linkedin_profil.txt'

file_path = 'rocket_name_company.csv'
rocket_df = pd.read_csv(file_path)

rocket_df['liste'] = rocket_df['Name'] + ', ' + rocket_df['Current Employer']

liste_linkedin = rocket_df['liste'].tolist()

for i in range (len(liste_linkedin)):
    liste_linkedin[i] = liste_linkedin[i].replace(' ','%20').replace(',','%2C')

columns = ['Name','company_name','linkedin_profil_url']
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# see progression with tqdm starting from the last page
driver.get(f"https://www.linkedin.com/search")
cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="artdeco-global-alert-container"]/div/section/div/div[2]/button[1]')))
cookie_button.click()

mail = 'romain_foucault@icloud.com'
password = '250768Lebigboss'  

login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
password_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
connect_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')))

login_button.send_keys(mail)
password_button.send_keys(password)
connect_button.click()

start_from = read_progress(progress_file_path)

for i, profil in enumerate(tqdm(liste_linkedin[start_from:]), start=start_from):

    driver.get(f"https://www.linkedin.com/search/results/people/?keywords={profil}&origin=SWITCH_SEARCH_VERTICAL&sid=rxf")
    try : 
        first_link_profil_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '(//a[@class="app-aware-link "])[2]')))
        linkedin_profil_url = first_link_profil_button.get_attribute('href')
    except:
        linkedin_profil_url = np.nan

    data = {'linkedin_profil_url':linkedin_profil_url,
            'Name':rocket_df.loc[i,'Name'],
            'company_name': rocket_df.loc[i,'Current Employer']}
          

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=columns)
                        writer.writerow(data)
                        
    save_progress(progress_file_path, i)
