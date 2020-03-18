from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

class web_scraper():
  def get_wine_info(self, search):
    options = Options()
    options.add_argument("--headless")
    print('Getting Wine Info..........')
    driver = webdriver.Chrome(executable_path=r"webdriver\chromedriver.exe", options=options)

    driver.get("https://www.google.com")
    search_bar = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@type='text']")))
    search_bar.send_keys(search)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@value='Google Search'])[2]"))).click()

    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//h3)[1]"))).click()
    print('Compiling Report..........')
    description =  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='description']"))).text
    rating = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='user-rating']"))).text
    price =  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='info medium-9 columns'])[1]/span/span"))).text
    designation = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='info medium-9 columns'])[2]/span/span"))).text
    variety = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='info medium-9 columns'])[3]/span/a"))).text
    appelation = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='info medium-9 columns'])[4]/span/a"))).text
    winery = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "(//*[@class='info medium-9 columns'])[5]/span/span/a"))).text
    # temp = 
    price = list(map(int, re.findall(r'\d+',price))) 
    wine_info = {'description':description,'rating':rating,'price':str(price[0]),'designation':designation,'variety':variety,'appelation':appelation,'winery':winery}

    return wine_info

# scraper = web_scraper()
# wine_info = scraper.get_wine_info('HOYA DECADENAS RESERVA TEMPRANILLO 2014 ESTATE wine enthusiast')
# print(wine_info)