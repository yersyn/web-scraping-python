import time
import urllib.request
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

from Contact import Contact
from ContactService import ContactService
from FileContacts import FileContacts


class ScrapingMypesPe:
    # Scraping Mypes.pe
    HOME_URL = 'https://mypes.pe'
    INITIAL_PAGE = 0
    contact_service = None

    def __init__(self):
        super().__init__()
        contact_service = ContactService()

    def get_businesses_urls(self, index):
        url_search = f"{self.HOME_URL}/directorio?field_categoria_target_id=All&field_distrito_target_id=All&page={index}"
        print(url_search)
        business = requests.get(url_search)
        business_s = BeautifulSoup(business.content, "html.parser")

        tags = business_s.find_all("h2", class_="home-mini-site-titulo")
        business_urls_tmp = list()
        print(f"numero de empresas: {len(tags)}")
        for tag in tags:
            url = tag.a['href']
            url = self.HOME_URL + url
            business_urls_tmp.append(url)
        return business_urls_tmp

    def extract_detail_business(self, business_url):
        contact = Contact()
        try:
            business = requests.get(business_url)
            business_s = BeautifulSoup(business.content, "html.parser")
            tags = business_s.find_all("div", class_="contacto-interno")
            for tag in tags:
                if len(tag.contents) == 11:
                    contact.email = self.deobfuscate_cf_email(tag.contents[7])
                    contact.phone = tag.contents[5].text
                    formated_contact_temp = contactS.add_pp(contact.ruc, contact.website, contact.email, contact.phone)
                else:
                    contact.email = self.deobfuscate_cf_email(tag.contents[5])
                    contact.phone = tag.contents[3].text
                    formated_contact_temp = contactS.add_pp(contact.ruc, contact.website, contact.email, contact.phone)

            return formated_contact_temp
        except NameError as ex:
            print(ex)

    def deobfuscate_cf_email(self, soup):
        print(soup)
        decode = ""
        for encrypted_email in soup.select('a.__cf_email__'):
            decode = self.decodeEmail(encrypted_email['data-cfemail'])
        return decode

    def decodeEmail(self, e):
        de = ""
        k = int(e[:2], 16)
        for i in range(2, len(e) - 1, 2):
            de += chr(int(e[i:i + 2], 16) ^ k)
        return de


scraping_Mypes = ScrapingMypesPe()
contactS = ContactService()
TOTAL_PAGES = 4

business_urls = list()
businesses_data = list()
PREFIX = "pymes peru"

# Secuencia de proceso de Scraping
# 1.- Recopilar urls de empresas

for cat_url in range(0, TOTAL_PAGES):
    business_urls += scraping_Mypes.get_businesses_urls(cat_url)
    time.sleep(1)

print(f"TENEMOS ESTAS URLS {len(business_urls)}")
# 2.- Extraer datos relevantes
for bu in business_urls:
    print(bu)
    formated_contact = scraping_Mypes.extract_detail_business(bu)

    if formated_contact is not None:
        businesses_data.append(formated_contact)
        # time.sleep(0.5)

print(len(businesses_data))
fileC = FileContacts(PREFIX)
fileC.create_pp_csv(businesses_data)
