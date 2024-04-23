#data sourcing script
#create a .csv file with the data scraped from the second website

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

#Scrapping Pappers
progress_file_path = 'progress_papers_test.txt'
csv_file_path = 'pappers_comptable_test.csv'
liste_file_path = 'liste_pappers.txt'

def convert_to_float(s):
    if s == '' or s == np.nan:
        return np.nan
    if not isinstance(s, str):  # Ensure chaine is a string
        return s
    # Replace commas with periods to handle European decimal format and remove spaces
    s = s.replace(',', '.').replace(' ', '')
    multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9}
    # Identify if the last character is a multiplier
    last_char = s[-1].upper()  # Use upper to handle lowercase letters
    if last_char in multipliers:
        # Convert the numeric part to float and apply the multiplier
        return float(s[:-1]) * multipliers[last_char]
    else:
        # If there's no multiplier, directly convert to float
        return float(s)


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


with open(liste_file_path, 'r') as file:
    content = file.read()
liste = content.split('\n')
for i in range(len(liste)):
    liste[i] = liste[i].replace("'",'')


token = "d25b6f1b63f9439193fd13f95a21d97421ba8670669"
proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)
proxies = {
    "http": proxyModeUrl,
    "https": proxyModeUrl,
}

columns = ['nom_beneficiaire','qualite','age','date_de_naissance','company_name', 'siren', 'adresse', 'effectif', 'annee_performance', 'CA', 'resultat_net', 'ebitda', 'papers_link']
# creation du fichier csv si il n'existe pas déjà du à une progression antérieure

if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

start_from = read_progress(progress_file_path)

def session_requests(prox, verify=False):
    session = requests.Session()
    session.proxies = prox
    session.verify = verify
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session



def scrape_data(url, session):
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        actif_span = soup.find('span', class_='actif')
        if actif_span:  # Vérifie si `actif_span` n'est pas None
            status_text = actif_span.get_text(strip=True)
            if status_text != 'Active':
                return
        else:
            return
        
        
        # Siren extraction
        siren = url.split('-')[-1] if url else np.nan

        # Adresse extraction
        adresse_element = soup.find("th", text="Adresse :")
        adresse = adresse_element.find_next_sibling("td").text.strip() if adresse_element and adresse_element.find_next_sibling("td") else np.nan

        # Effectif extraction
        effectif_element = soup.find("th", text="Effectif :")
        effectif = effectif_element.find_next_sibling("td").text.strip().split('\n')[0] if effectif_element and effectif_element.find_next_sibling("td") else np.nan

        # Année de performance extraction
        annee_performance_element = soup.find("th", text="Performance")
        annee_performance = annee_performance_element.find_next_sibling("th").text.strip() if annee_performance_element and annee_performance_element.find_next_sibling("th") else np.nan

        # Chiffre d'affaires extraction
        ca_element = soup.find("th", text=re.compile("Chiffre d'affaires"))
        ca = ca_element.parent.find("td").text.strip() if ca_element and ca_element.parent and ca_element.parent.find("td") else np.nan
        ca = convert_to_float(ca) if ca is not np.nan else np.nan

        # Résultat net extraction
        resultat_net_element = soup.find("th", text="Résultat net (€)")
        resultat_net = resultat_net_element.find_next_sibling("td").text.strip() if resultat_net_element and resultat_net_element.find_next_sibling("td") else np.nan
        resultat_net = convert_to_float(resultat_net) if resultat_net is not np.nan else np.nan

        # EBITDA extraction
        ebitda_element = soup.find("th", text="EBITDA - EBE (€)")
        ebitda = ebitda_element.find_next_sibling("td").text.strip() if ebitda_element and ebitda_element.find_next_sibling("td") else np.nan
        ebitda = convert_to_float(ebitda) if ebitda is not np.nan else np.nan

        company_name = ' '.join([part.upper() for part in url.split('/')[-1].split('-') if not part.isdigit() and part])


        if ebitda is np.nan and resultat_net is not np.nan:
            ebitda = resultat_net * 1.25

        for li in soup.select('.beneficiaire'):
        # Nom du bénéficiaire
            nom_element = li.find('a', class_='nom')
            nom = nom_element.text.strip() if nom_element else np.nan
            
            # Qualité du bénéficiaire
            qualite_element = li.find('span', class_='qualite')
            qualite = qualite_element.text.strip() if qualite_element else np.nan
            
            # Âge et date de naissance du bénéficiaire
            age_element = li.find('span', class_='age')
            if age_element:
                age_details = age_element.text.strip().split('-')
                age = age_details[0].strip() if age_details else np.nan
                date_de_naissance = age_details[-1].strip() if len(age_details) > 1 else np.nan
            else:
                age = np.nan
                date_de_naissance = np.nan

            data = {
                'nom_beneficiaire': nom,
                'qualite': qualite,
                'age': age,
                'date_de_naissance': date_de_naissance,
                'company_name': company_name,  
                'siren': siren,
                'adresse': adresse,
                'effectif': effectif,
                'annee_performance': annee_performance,
                'CA': ca,
                'resultat_net': resultat_net,
                'ebitda': ebitda,
                'papers_link': url  
            }

            return data
    else:
        return 

def main(liste, start_from, proxies, csv_file_path, progress_file_path, columns):
    print(f"Starting scraping from index {start_from}")
    liste_url = []
    for i in range(len(liste)):
        url = f"https://www.pappers.fr/entreprise/{liste[i]}"
        liste_url.append(url)
    session = session_requests(proxies)
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scrape_data, s, session): s for s in liste_url[start_from:]}
        for i, future in enumerate(tqdm(concurrent.futures.as_completed(futures), total=len(liste_url[start_from:]), desc="Progression du scraping")):
            s = futures[future]
            try:
                result = future.result()
                if result:
                    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=columns)
                        writer.writerow(result)
            
            except Exception as e:
                print(f"An error occurred for {s}: {str(e)}")
            finally:
                save_progress(progress_file_path, i)

if __name__ == "__main__":
    main(liste, start_from, proxies, csv_file_path, progress_file_path, columns)
