import csv
import os
import re
import time
from typing import Dict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from PIL import Image

def screenshot(driver, path, imgURL, clip = False ):
  if(clip):
    height = 1080
  else:
    body = driver.find_element(By.TAG_NAME, 'body')  
    height = body.size['height']

  path = os.path.join("screenshots", path)
  ext = ".png"

  #create folder screenshots if not exists
  if not os.path.exists(path):
    os.makedirs(path)
  
  body = driver.find_element(By.TAG_NAME, 'body')
  driver.set_window_size(1920, height)

  imgPath = os.path.join(path, imgURL + ext)
  body.screenshot(imgPath)

  screenshot = Image.open(imgPath)
  #uncomment the below line view each screenshots after saving
  #screenshot.show()

class CSVfile:

  def __init__(self, *args):

    if len(args) > 1:
      self.file = open(args[0], 'w')
      self.writer = csv.DictWriter(self.file, fieldnames=args[1])
      self.writer.writeheader()
    elif len(args) == 1:
      self.file = open(args[0])
    else:
      print('Provide arguments to create object')

  def writeRow(self, row: Dict):
    self.writer.writerow(row)

  def readCsv(self):
    return csv.reader(self.file)

  def fileClose(self):
    self.file.close()


def main():

  #browser webdriver
  options = Options()
  options.add_argument('-headless')
  options.add_argument('-start-maximized')
  driver = webdriver.Chrome(options=options)
  driver.implicitly_wait(20)

  #open URL
  driver.get("https://www.vodafone.co.uk/mobile/phones/pay-monthly-contracts")
  print("Loaded")

  #handle cookie popup  
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

  print('scrolling...')
  for i in range(20):
    actions.move_to_element(element).perform()
    time.sleep(2)

  #fetch page source content as html
  page_soup = BeautifulSoup(driver.page_source, 'html.parser')
  
  #first section contains links to the products
  section_soup = page_soup.find('section')

  #product links
  links = section_soup.find_all('a', {'href' : re.compile(r'^/mobile/phones/pay\-monthly\-contracts/\w+/')})

  #store it in a dictionary
  urlDict = {}
  for link in links:
    urlDict[link.get('aria-label')] = link.get('href')
  
  #Sorting
  keys = list(urlDict)
  keys.sort()
  urlDict_sorted = {i: urlDict[i] for i in keys}

  #Save as CSV
  csvfile = CSVfile('products.csv',['id', 'name', 'url'])
  id = 0
  for (k,v) in urlDict_sorted.items():
    id += 1
    csvfile.writeRow({
      'id': id,
      'name': k,
      'url': "https://www.vodafone.co.uk" + v
    })
  
  csvfile.fileClose()
  print('CSV saved\n')

  time.sleep(5)

def automate(n):
  csvfile = CSVfile('products.csv')
  rows = csvfile.readCsv()
  next(rows)

  #browser webdriver options
  options = Options()
  options.add_argument('-headless')
  options.add_argument('-start-maximized')
  
  #iterate over n products
  for i in range(1,n+1):
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20)

    row = next(rows)

    productName = row[1]
    productURL = row[2]

    print(productName)

    #open URL
    driver.get(productURL)
    print("Loaded", end=' > ')

    #Handle popup cookie
    try:
      element = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
      element.click()
      print("Cookies Accepted", end=' > ')

      driver.switch_to.parent_frame()
    except WebDriverException:
      print("No Cookie popup", end=' > ')

    time.sleep(30)
    
    #save PDP.png
    screenshot(driver, productName, 'PDP')
    
    time.sleep(15)

    #Pay for your phone in one go
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//a[@data-di-id="di-id-eeb5254d-6b9c18b7"]')))
    element.click()
    print("Pay popup", end=' > ')

    time.sleep(15)

    #save MSRP.png
    screenshot(driver, productName, 'MSRP', clip=True)

    #Close Pay popup
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, "vfuk-Modal__close")))
    element.click()
    print("Popup closed", end=' > ')

    time.sleep(15)

    driver.switch_to.parent_frame()

    #Build your Phone Plan
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="vfuk-HandsetContainerBingo__button-no-margin-top"]')))
    element.click()
    print("Build Plan", end=' > ')

    time.sleep(15)

    #I'm a New Customer
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="Interactionstyle__Button-sc-e1xkgc-0 iGJLLD Buttonstyle__Button-sc-twej8-0 drJemV"]')))
    element.click()
    print("New customer", end=' > ')

    time.sleep(15)

    #Phoneplan.png
    screenshot(driver, productName, 'Phoneplan')

    #Click Continue
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="Interactionstyle__Button-sc-e1xkgc-0 iGJLLD Buttonstyle__Button-sc-twej8-0 gvvVMf"]')))
    element.click()
    print("Continue", end=' > ')

    time.sleep(15)

    #Click No
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="Interactionstyle__Button-sc-e1xkgc-0 iGJLLD Buttonstyle__Button-sc-twej8-0 lkbsyd"]')))
    element.click()
    print("No")

    time.sleep(15)

    #Wait for the content to load
    element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="vfuk-Button__button vfuk-PlanCardMiniButton__button vfuk-Button__full vfuk-Button__primary margin-top-1 margin-bottom-1 margin-left-sm-0 margin-right-sm-0"]')))
    
    #Airtime.png
    screenshot(driver, productName, 'Airtime')

    print('Saved all Screenshots\n')
    driver.quit()

  csvfile.fileClose()

if __name__ == "__main__":
  main()
  automate(n=4)