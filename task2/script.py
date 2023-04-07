import csv
import os
import re
import time
from tokenize import String
from typing import Dict, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from PIL import Image

def screenshot(driver, imgURL):
  path = "screenshots"
  ext = ".png"
  #create folder screenshots if not exists
  if not os.path.exists(path):
    os.makedirs(path)
  
  body = driver.find_element(By.TAG_NAME, 'body')
  driver.set_window_size(1920, body.size['height'])

  imgPath = os.path.join(path, imgURL + ext)
  body.screenshot(imgPath)

  screenshot = Image.open(imgPath)
  #uncomment the below line view each screenshots after saving
  #screenshot.show()

class CSVfile:

  def __init__(self, fileURL: String, headers: List):
    self.file = open(fileURL, 'w')
    self.writer = csv.DictWriter(self.file, fieldnames=headers)
    self.writer.writeheader()
  
  def writeRow(self, row: Dict):
    self.writer.writerow(row)

def main():

  #browser webdriver
  options = Options()
  #options.add_argument('-headless')
  options.add_argument('-start-maximized')
  driver = webdriver.Chrome(options=options)
  driver.implicitly_wait(20)

  #open URL
  driver.get("https://www.vodafone.co.uk/mobile/phones/pay-monthly-contracts")
  print("Loaded")
  
  try:
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    element.click()
    print("Cookies Accepted")
    
    driver.switch_to.parent_frame()
  except WebDriverException:
    print("No Cookie popup")
  
  time.sleep(5)

  #scroll to get all list under the viewport
  element = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section/div/div[6]/div/div[4]')
  actions = ActionChains(driver)

  for i in range(20):
    print('scrolling')
    actions.move_to_element(element).perform()
    time.sleep(2)  

  #fetch page source content as html
  page_soup = BeautifulSoup(driver.page_source, 'html.parser')
  
  #first section contains links to the products
  section_soup = page_soup.find('section')
  print(section_soup.get('class'))

  links = section_soup.find_all('a', {'href' : re.compile(r'^/mobile/phones/pay\-monthly\-contracts/\w+/')})

  urlDict = {}
  for link in links:
    urlDict[link.get('aria-label')] = link.get('href')
    print(link.get('aria-label'),link.get('href'))
  
  keys = list(urlDict)
  keys.sort()

  urlDict_sorted = {i: urlDict[i] for i in keys}

  csvfile = CSVfile('products.csv',headers=['id', 'name', 'url'])
  id = 0
  for (k,v) in urlDict_sorted.items():
    id += 1
    print(k,v)
    csvfile.writeRow({
      'id': id,
      'name': k,
      'url': v
    })
    input()
  
  time.sleep(50)
  
if __name__ == "__main__":
  main()
