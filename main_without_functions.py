from selenium import webdriver
from bs4 import BeautifulSoup
import time

# ======================================================== Start =====================================================
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options)

try:
    driver.get("https://paranewera.com/")
    soup = BeautifulSoup(driver.page_source, 'lxml')
    f = open("paranewera.json", "a")
    f.write('[')
    
    # =============================================== Get Categories =======================================================
    categories = soup.find(class_='top-menu').find_all('a', {'data-depth': '0'})
    subs = soup.find_all('ul', {'data-depth': '1'})
    cpt = 0
    for categorie in categories:
        if(cpt <= 12):
            print('Categorie : ' + str(categorie.text).replace('\n', ' ').strip())
            f.write('\n\t{\n\t\t"categorie": "' + str(categorie.text).replace('\n', ' ').strip() + '",\n\t\t"items": [')
            # =============================================== Get Sub Catégories =======================================================
            sub_categorie = subs[cpt].find_all('a', {'data-depth': '1'})
            for sub in sub_categorie:
                f.write('\n\t\t\t\t{\n\t\t\t\t\t"sub_categorie": "' + str(sub.text).replace('\n', ' ').strip() + '",\n\t\t\t\t\t"items": [')
                driver.get(sub['href'])
                time.sleep(5)
                try:
                    pagination = BeautifulSoup(driver.page_source, 'lxml').find(class_="page-list").find_all('a')
                    if(len(pagination) > 1):
                        nb_pages = int(pagination[len(pagination) - 2].text)
                    else:
                        nb_pages = 1
                    print('\tSub Categorie : ' + str(sub.text).replace('\n',' ').strip() + ' (' + str(nb_pages) + ') ' + sub['href'])
                    for i in range(1, nb_pages + 1):
                        print('\t\tPage : ' + str(i) + ' (' + sub['href'] + '?page=' + str(i) + ')')
                        driver.get(sub['href'] + '?page=' + str(i))
                        time.sleep(5)
                        # =============================================== Get  Products =======================================================
                        products = BeautifulSoup(driver.page_source, 'lxml').find('div', {'id': 'content-wrapper'}).find_all(class_='product-miniature')
                        for product in products:
                            driver.get(product.find(class_='product-thumbnail')['href'])
                            time.sleep(5)
                            product_info = BeautifulSoup(
                                driver.page_source, 'lxml')
                            # ===================================== Get Product info ===============================================
                            try:
                                name = str(product_info.find(class_='h1').text).replace('"', '').replace('\n', '').replace('&', 'et').strip()
                                print('\t\t\tProduct : ' + name)
                                f.write('\n\t\t\t\t\t\t{ "Produit": "' + name + '",')
                            except (ValueError, Exception):
                                f.write('"\nproduit": "",')
                            try:
                                f.write(' "prix": "' + str(product_info.find(class_="price").text).strip() + '",')
                            except (ValueError, Exception):
                                f.write('"prix": "",')
                            try:
                                f.write('"image": "' + str(product_info.find(class_='js-qv-product-cover')['src']) + '",')
                            except (ValueError, Exception):
                                f.write('"image": "",')
                            try:
                                desc_container = product_info.find(class_="product-description").find_all('p')
                                description = ""
                                for desc in desc_container:
                                    description = description + desc.text
                                    description = str(description).replace('"', '').replace('&', 'et').replace(' ', '').replace('\n', '').replace('&', 'et').strip()
                                f.write(' "desc": "' + description + '"},')
                            except (ValueError, Exception):
                                f.write('"desc": ""},')
                except (ValueError, Exception):
                    continue
                f.write('\n\t\t\t\t\t]\n\t\t\t\t},')
            f.seek(0, 2)
            size = f.tell()
            f.truncate(size - 1)
            f.write('\n\t\t]\n\t},')
        cpt = cpt + 1
    f.seek(0, 2)
    size = f.tell()
    f.truncate(size - 1)
    f.write(']')
finally:
    driver.close()
    f.close()
