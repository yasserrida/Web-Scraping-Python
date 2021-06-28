from selenium import webdriver
from bs4 import BeautifulSoup
import time

options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path='./geckodriver', options=options)


def getCategories():
    driver.get("https://paranewera.com/")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    categories = soup.find(class_='top-menu').find_all('a', {'data-depth': '0'})
    return categories
  
  
def getSubCategories(indice):
    driver.get("https://paranewera.com/")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    subs = soup.find_all('ul', {'data-depth': '1'})
    return subs[indice].find_all('a', {'data-depth': '1'})
  

def getPagination(subCategorie):
    driver.get(subCategorie['href'])
    time.sleep(3)
    pagination = BeautifulSoup(driver.page_source, 'lxml').find(class_="page-list").find_all('a')
    if(len(pagination) > 1):
        nb_pages = int(pagination[len(pagination) - 2].text)
    else:
        nb_pages = 1
    return nb_pages
  
  
def LoopByPage(sub):
    try:
        nb_pages = getPagination(sub, driver)
        for i in range(1, nb_pages + 1):
            print('\t\tPage : ' + str(i))
            getProducts(nb_pages['href'] + '?page=' + str(i))
    finally:
        driver.close()
        
def getProducts(url):
    data =  driver.get(url)
    time.sleep(3)
    products = BeautifulSoup(data, 'lxml').find('div', {'id': 'content-wrapper'}).find_all(class_='product-miniature')
    for product in products:
        driver.get(product.find(class_='product-thumbnail')['href'])
        time.sleep(3)
        product_info = BeautifulSoup(driver.page_source, 'lxml')
        getProductInfo(product_info)
        
        
def getProductInfo(product_info):
    name = str(product_info.find(class_='h1').text).replace('"', '').replace('\n', '').replace('&', 'et').strip()
    print('\t\t\tProduct : ' + name)     
          
        
if __name__ == "__main__": 
    for categorie in categories:
        print("Categorie : " + re.sub('[^A-Za-z0-9_À-ÿ ]+','', str(categorie.text).replace('\n', ' ').strip()))
        subs = getSubCategories(cpt)
            for sub in subs:
                print("\tSub Categorie : " + re.sub('[^A-Za-z0-9_À-ÿ ]+', '', str(sub.text).replace('\n', ' ').strip()))
                LoopByPage(sub)
        
