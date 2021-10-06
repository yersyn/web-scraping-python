import time
import urllib.request
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

from Contact import Contact
from ContactService import ContactService
from FileContacts import FileContacts


class ScrapingPP:
    # Scraping Peru Pymes
    HOME_URL = 'https://perupymes.com'
    INITIAL_PAGE = 1
    TOTAL_PAGES = 3
    contact_service = None

    def __init__(self):
        super().__init__()
        contact_service = ContactService()

    def get_category_urls(self):
        # URLS DE CATEGORIAS
        home = urllib.request.urlopen(self.HOME_URL)
        home_s = BeautifulSoup(home, "html.parser")

        sections = home_s.find_all("h5", {"class": "fuen_cat list_cat"})
        category_urls_tmp = list()
        for sect in sections:
            category_urls_tmp.append(sect.contents[0].get('href'))

        print(len(category_urls_tmp))
        return category_urls_tmp

    def get_businesses_url_by_category(self, url_category):
        business = urllib.request.urlopen(url_category)
        business_s = BeautifulSoup(business, "html.parser")

        tags = business_s.find_all("div", class_="panel cuadroempresa")
        business_urls_tmp = list()
        print(f"numero de empresas: {len(tags)}")

        for tag in tags:
            url = tag.contents[1].a['href']
            business_urls_tmp.append(url)
        return business_urls_tmp

    def extract_detail_business(self, business_url):
        contact = Contact()
        try:
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            # req = urllib.request.Request(url=business_url, headers=headers)
            # business = urllib.request.urlopen(req).read()
            business = requests.get(business_url)
            business_s = BeautifulSoup(business.content, "html.parser")
            tags = business_s.find_all("ul", class_="list-unstyled")
            print(business_url)
            for tag in tags:
                # # print(tag.contents)
                # print(tag.contents[1].text)
                # print(tag.contents[3].a['href'])
                # print(tag.contents[5].a.text)
                # print(tag.contents[7].text)

                contact.ruc = tag.contents[1].text if tag.contents[1].text is not None else "None"
                contact.website = tag.contents[3].a['href'] if tag.contents[3].a['href'] is not None else "None"
                contact.email = tag.contents[5].a.text if tag.contents[5].a.text is not None else "None"
                contact.phone = tag.contents[7].text if tag.contents[7].text is not None else "None"
                formated_contact_temp = contactS.add_pp(contact.ruc, contact.website, contact.email, contact.phone)
                print(formated_contact_temp)
            return formated_contact_temp
        except NameError:
            print("Fallo algo")


scraping_PP = ScrapingPP()
contactS = ContactService()

category_urls = list()
business_urls = list()
businesses_data = list()
PREFIX = "pymes peru"

# Secuencia de proceso de Scraping
# 1.- Recopilar urls de empresas
category_urls = scraping_PP.get_category_urls()
for cat_url in category_urls:
    business_urls += scraping_PP.get_businesses_url_by_category(cat_url)

print(f"TENEMOS ESTAS URLS {len(business_urls)}")
# print(business_urls)
# 2.- Extraer datos relevantes
for bu in business_urls:
    formated_contact = scraping_PP.extract_detail_business(bu)

    if formated_contact is not None:
        businesses_data.append(formated_contact)
        # time.sleep(0.5)

print(len(businesses_data))
fileC = FileContacts(PREFIX)
fileC.create_pp_csv(businesses_data)
