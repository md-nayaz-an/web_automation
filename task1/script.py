from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def main():
  options = Options()
  #options.add_argument('-headless')
  driver = webdriver.Firefox(options=options)
  driver.implicitly_wait(20)
  driver.get("https://shop.ee.co.uk/mobile-phones/pay-monthly/iphone-14-pro-5g/details?CTTag=CT_Sal_HP_H2_Phones_C5_AppleiPhone14Pro_Q4_2023")
  print("loaded")
  vars = driver.find_elements(By.CSS_SELECTOR, ".form__check #colour-switcher-group" )
  for var in vars:
    print(var.text)
    
if __name__ == "__main__":
  main()
