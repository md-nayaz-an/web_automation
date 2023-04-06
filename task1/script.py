from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def main():
  
  #browser webdriver
  options = Options()
  options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)
  driver.implicitly_wait(20)
  
  #open URL
  driver.get("https://shop.ee.co.uk/mobile-phones/pay-monthly/iphone-14-pro-5g/details?CTTag=CT_Sal_HP_H2_Phones_C5_AppleiPhone14Pro_Q4_2023")
  print("loaded")

  #fetch page source content as html
  page_soup = BeautifulSoup(driver.page_source, 'html.parser')
  
  #tags with color variants input radio button
  colorStarch = page_soup.find_all('input', {'name' : 'colour-switcher-group'})
  colorId = []
  for ele in colorStarch:
    colorId.append(ele.get('id'))
  print(colorId)

  #tags with capacity variant input radio button
  capacityStarch = page_soup.find_all('input', {'name' : 'capacity-selector-group'})
  capacityId = []
  for ele in capacityStarch:
    capacityId.append(ele.get('id'))
  print(capacityId)


if __name__ == "__main__":
  main()
