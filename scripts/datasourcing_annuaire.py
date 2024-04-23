#data sourcing script
#create a .csv file with the data scraped from the first website

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

#Scrapping Annuaire expert comptable
i_progress_file_path = 'progress_comptable_i3.txt'
d_progress_file_path = 'progress_comptable_d3.txt'
csv_file_path = 'comptable2_3.csv'


def read_progress(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            line = f.readline()
            if line:
                return int(line.strip())
    return 1  # Démarre de 1 si le fichier n'existe pas ou est vide

def save_progress(file_path, progress):
    with open(file_path, 'w') as f:
        f.write(str(progress))


columns = ['company_name', 'forme_juridique', 'telephone', 'nb_exp', 'sites']
# creation du fichier csv si il n'existe pas déjà du à une progression antérieure
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

i_cookie = 55#read_progress(i_progress_file_path)
# ouvrir l'annuaire des experts comptables
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# see progression with tqdm starting from the last page
max_i = 55
# read_progress(i_progress_file_path
for i in tqdm(range(55, max_i+1)):
    driver.get(f"https://annuaire.experts-comptables.org/recherche/{i}?seed=33798")
    if i == i_cookie:
        cookie_accept = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tarteaucitronPersonalize"]')))[0]
        cookie_accept.click()
        driver.maximize_window()
    # read_progress(d_progress_file_path)
    for d in range(1 , 11):
        try:
            base_xpath = f"/html/body/div[1]/div[2]/div/div[2]/div[{d}]"
            societe = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"{base_xpath}/div[2]/div[1]/div/a"))).text
            company_name, forme_juridique = societe.split('\n')[:2]
            try:
                telephone_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"{base_xpath}/div[3]/div/div[1]")))
                telephone_button.click()
                try:
                    telephone = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mailForm"]/div/a'))).text
                except:
                    telephone = np.nan
                close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-close"]')))
                close_button.click()
            except: 
                telephone = np.nan
            try : 
                savoir_plus_button =  WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f'{base_xpath}/div[3]/a')))
                savoir_plus_button.click()
                try :
                    nb_exp = len(WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div/div/div'))))
                except : 
                    nb_exp = np.nan
                try :
                    element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div/p")))
                    sites = element.text
                except:
                    sites = np.nan
                try :
                    bouton_retour = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/div[1]/div/span[2]/a')))
                    bouton_retour.click()
                except :
                    print(f'pas de boutton retour error i: {i}, d:{d}')
                    sys.quit(1)
            except : 
                print(f'pas de boutton en savoir plus error i: {i}, d:{d}')
                sys.quit(1)                
        except:
            print(f'societe non trouvé error i: {i}, d:{d}')
            continue    


        # stockage des données enregistrées
        data = {
            'company_name': company_name,
            'forme_juridique': forme_juridique,
            'telephone': telephone,
            'nb_exp': nb_exp,
            'sites' : sites
        }

        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writerow(data)

        if d == 10:
            save_progress(d_progress_file_path, 1)
        else:
            save_progress(d_progress_file_path, d)

    
    save_progress(i_progress_file_path, i)
