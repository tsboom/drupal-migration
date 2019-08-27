from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pickle
import time


article_url = "http://usmai.umd.edu/documents/aleph-tables"


driver = webdriver.Firefox()
driver.get(article_url)

# log into the homepage
username = driver.find_element_by_name('name')
username.send_keys('tiffany')
password = driver.find_element_by_name('pass')
password.send_keys('tiffany1')
password.send_keys(Keys.RETURN)

# save cookie
pickle.dump(driver.get_cookies() , open('cookies.pkl', 'wb'))

#new driver
driver = webdriver.Firefox()



# go to article


driver= driver.get(article_url)
time.sleep(5)
# load cookies
cookies = pickle.load(open('cookies.pkl', 'rb'))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh_page()
time.sleep(5)


content = driver.find_element_by_css_selector('.content').get_attribute('innerHTML')

print(content)
# soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
# print soup.prettify()

'''
requests version
'''
s = requests.Session()
data = {'name':'tiffany', 'pass':'tiffany1'}
url = "http://usmai.umd.edu"

r = s.post(url, data=data)
html
