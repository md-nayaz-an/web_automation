import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def main():

  #browser webdriver
  options = Options()
  options.add_argument('-headless')
  options.add_argument('-start-maximized')
  driver = webdriver.Chrome(options=options)
  driver.implicitly_wait(20)

  #open URL
  driver.get("https://shop.ee.co.uk/mobile-phones/pay-monthly/iphone-14-pro-5g/details?CTTag=CT_Sal_HP_H2_Phones_C5_AppleiPhone14Pro_Q4_2023")
  print("Loaded")
  
  try:
    WebDriverWait(driver, 100).until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "truste_popframe")))
    driver.find_element(By.CLASS_NAME, 'call').click()
    print("Cookies Accepted")
    
    driver.switch_to.parent_frame()
  except WebDriverException:
    print("No Cookie popup")
  
  time.sleep(5)
  
  #fetch page source content as html
  page_soup = BeautifulSoup(driver.page_source, 'html.parser')
  
  #item name from metadata
  itemName = page_soup.find('span', {'data-content-id' : 'product-title'}).getText()

  #tags with color variants input radio button
  colorStarch = page_soup.find_all('input', {'name' : 'colour-switcher-group'})
  colorId = {}
  for ele in colorStarch:
    colorId[ele.get('id')] = ele.next_sibling.get('data-content-id')

  #tags with capacity variant input radio button
  capacityStarch = page_soup.find_all('input', {'name' : 'capacity-selector-group'})
  capacityId = []
  for ele in capacityStarch:
    capacityId.append(ele.get('id'))

  #iterate over each combination
  for color in colorId.keys():
    colorText = colorId[color]

    #wait and click color variant
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'assistive-' + color))).click()
    time.sleep(10)
    
    for capacity in capacityId:
      capacityText = capacity.split('-')[-1]

      #wait and click capacity variant
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'assistive-' + capacity))).click()
      
      #check if 'view all plans is clickable'
      try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="show-viewAllPlans"]'))).click()
      except WebDriverException:
        None

      time.sleep(5)

      #form image Url for the screenshot
      imgUrl = itemName + '_' + colorText + '_' + capacityText
      print(f'Saving "{imgUrl}.png"')
      screenshot(driver, imgUrl)
  
  driver.quit()

      
if __name__ == "__main__":
  main()
