from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pickle
import time
import pdb
import url_list
import login_credentials


# get list of URLs from Content Audit ex: ['Ref Id', 'URL']
urls = url_list.get_content_audit_values()

def clean_html(post_body):
    '''
    function that will remove inline styles and extra stuff from HTML
    '''
    print('to be continued...')
    clean_post = 'cleaned up post_body'
    return clean_post


def scrape_article(url, ref_id):
    # go to article
    driver = webdriver.Firefox()
    driver.get(url)

    # log into the homepage
    username = driver.find_element_by_name('name')
    username.send_keys(login_credentials.USERNAME)
    password = driver.find_element_by_name('pass')
    password.send_keys(login_credentials.PASSWORD)
    password.send_keys(Keys.RETURN)

    # wait and get content
    time.sleep(3)
    content = driver.find_element_by_id('content').get_attribute('innerHTML')

    # create BS out of HTML
    soup = BeautifulSoup(content, features="html.parser")

    # get title out of BeautifulSoup
    title = soup.h1.string

    # get content out of id content-area < class content
    post_body = soup.select('#content-area .content')[0].prettify()
    '''
    more processing should be done on this post_body to remove inline styles.
    we just want the plain HTML tags.
    '''



    # save to html
    file = 'page_html/' +  ref_id + '_' + title + '.html'
    with open(file, 'w+') as f:
        f.write(post_body)

    driver.close()


'''
scrape html from each url in urls
'''
for urlrefid in urls:
    # parse out ref_id and URL
    ref_id = urlrefid [0]
    url = urlrefid [1]
    # only scrape for valid urls
    if url.startswith('http'):
        scrape_article(url, ref_id)
