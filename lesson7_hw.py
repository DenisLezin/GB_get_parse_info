from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()

driver.get('https://mail.ru/')
assert 'Mail.ru' in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('*****')
elem.send_keys(Keys.RETURN)

try:
    # elem = driver.find_element_by_id('mailbox:password')
    elem = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, 'mailbox:password'))
    )
    elem.send_keys('*****')
    elem.send_keys(Keys.RETURN)
except Exception as e:
    print(e)

letters = driver.find_elements_by_class_name('js-letter-list-item')

ltr = {}
for letter in letters:
    ltr[letter.text] = letter.get_attribute('href')


print(driver.title)

print(ltr)
driver.quit()