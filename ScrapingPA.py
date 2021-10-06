from selenium import webdriver
import time

from ContactService import ContactService
from FileContacts import FileContacts

# Scraping Paginas amarillas max => 1097
BASE_URL = 'https://www.paginasamarillas.com.pe/servicios/grafico?page='
INITIAL_PAGE = 1
TOTAL_PAGES = 3
PREFIX = f"EMP-grafico-{INITIAL_PAGE}-{TOTAL_PAGES}"
contactS = ContactService()

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

for page in range(INITIAL_PAGE, TOTAL_PAGES):
    driver.get(BASE_URL + str(page))
    driver.page_source.encode('utf-8')
    items = driver.find_elements_by_class_name('business')
    print(f"PAGINA {page}")
    time.sleep(0.1)
    c = 0
    for i in items:
        idTag = f"phone-list-{c}"   
        try:
            button = i.find_element_by_id("ver-telefonos")
            name = i.find_element_by_class_name('companyName').text
            if i.is_displayed():
                button.click()
                phone = i.find_element_by_id(idTag).text
                if contactS.validate_phone(phone):
                    contactS.add(contactS.format_name(name), phone)
        except Exception as e:
            print(e)
        c += 1

fileC = FileContacts(PREFIX)
fileC.create_csv(contactS.get_contacts_list())
