from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://geekbrains.ru/login')
assert 'GeekBrains' in driver.title

elem = driver.find_element_by_id('user_email')
elem.send_keys('santar2000@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('anden2000')

elem.send_keys(Keys.RETURN)
assert 'GeekBrains' in driver.title



# print(driver.title)
# driver.quit()