from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import datetime
import pickle
import time
import pdb
import url_list
import login_credentials

post_body_raw = None

# get list of URLs from Content Audit ex: ['Ref Id', 'URL']
urls = url_list.get_content_audit_values()


def clean_html(html):

    '''
    function that will remove inline styles and extra stuff from HTML
    '''
    blacklist = ['style','border','width','height','cellpadding','cellspacing','align','valign','target']
    for tag in html.recursiveChildGenerator():
        attrKeys = {}        
        try:
            for k in list(tag):
                if k in blacklist:
                    del tag.attrs[k]
        except AttributeError:
            pass
    return html

def img_harvest(html):
    '''
    Harvest img references as long as they are from the USMAI domain. Has some error handling to manage invalid schemes, missing schemes, or external connections.
    '''
    for a in html.findAll('img'):
        try:
            url_temp = (a.attrs['src'])
            if 'http://usmai.umd.edu' not in url_temp:
                url = 'http://usmai.umd.edu' + url_temp
            else:
                url = url_temp
            pic_file = url.rsplit('/',1)[1]
            r = requests.get(url, allow_redirects=True)
            file = 'page_html/' +  ref_id + '_' + pic_file
            open(file, 'wb').write(r.content)
        except requests.exceptions.InvalidSchema:
            continue
        except requests.exceptions.MissingSchema:
            continue
        except requests.exceptions.ConnectionError:
            continue


def attachment_harvest(html):
    '''
    Harvest attached files as long as they are from the USMAI domain. Has connection error handling if connection rejected. Should only pick up files from USMAI domain server.
    '''
    for a in html.findAll('a',href=True):
        try:
            url_temp = (a.attrs['href'])
            if 'http://usmai.umd.edu' not in url_temp:
                url = 'http://usmai.umd.edu' + url_temp
            else:
                url = url_temp
            filepath = url.rsplit('/',1)[1]
            if 'sites/staff/files/' in url or 'sites/default/files' in url:
                r = requests.get(url, allow_redirects=True)
                file = 'page_html/' + ref_id + '_' + filepath
                open(file, 'wb').write(r.content)
                with open('log', 'a+') as f:
                    f.write(filepath + ' saved\n')
                print(url)
        except requests.exceptions.ConnectionError:
            with open('log', 'a+') as f:
                f.write(filepath + ' failed to save: connection error\n')
            continue     

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
    time.sleep(5)
    content = driver.find_element_by_id('content').get_attribute('innerHTML')

    # create BS out of HTML
    soup = BeautifulSoup(content, features="html.parser")
    
    # get title out of BeautifulSoup
    if soup.h1:
        title = soup.h1.string
    else: 
        title = "no h1 found"

    # get content out of id content-area < class content
    post_body_raw = soup.select('#content-area .content')[0]
    
    post_body_raw = clean_html(post_body_raw)
    img_harvest(post_body_raw)
    attachment_harvest(post_body_raw)

    post_body = str(post_body_raw)

    '''
    more processing should be done on this post_body to remove inline styles.
    we just want the plain HTML tags.
    '''

    # save to html
    try:
        file = 'page_html/' +  ref_id + '_' + title + '.html'
        with open(file, 'w+') as f:
            f.write(post_body)
            print(ref_id)
        f.close()
        driver.close()
    except IOError:
        file = 'page_html/' +  ref_id +'.html'
        with open(file, 'w+') as f:
            f.write(post_body)
        f.close()
        driver.close()


'''
scrape html from each url in urls
'''
'''
Wrapper to run scrape function and write log
'''
f = open('log','a+')
for urlrefid in urls:
    # parse out ref_id and URL
    ref_id = urlrefid [0]
    url = urlrefid [1]
    # only scrape for valid urls
    if url.startswith('http'):
        try:
            scrape_article(url, ref_id)
            f.write(ref_id + '\n')
        except IndexError:
            pass
            f.write(ref_id + ' failed \n')

f.close()
