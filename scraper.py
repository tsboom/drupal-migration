from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pickle
import time
import pdb
import url_list
import login_credentials

post_body_raw = None

# get list of URLs from Content Audit ex: ['Ref Id', 'URL']
urls = url_list.get_content_audit_values()


def clean_html(htmlIn):

    '''
    function that will remove inline styles and extra stuff from HTML
    '''
    blacklist = ['style','border','width','height','cellpadding','cellspacing','align','valign','target']
    for tag in htmlIn.recursiveChildGenerator():
        attrKeys = {}        
        try:
            for k in list(tag):
                if k in blacklist:
                    del tag.attrs[k]
        except AttributeError:
            pass
    return htmlIn

def imgHarvest(htmlIn):
    '''
    Harvest img references as long as they are from the USMAI domain. Has some error handling to manage invalid schemes, missing schemes, or external connections.
    '''
    for a in htmlIn.findAll('img'):
        try:
            urlTemp = (a.attrs['src'])
            if 'http://usmai.umd.edu' not in urlTemp:
                url = 'http://usmai.umd.edu' + urlTemp
            else:
                url = urlTemp
            picFile = url.rsplit('/',1)[1]
            r = requests.get(url, allow_redirects=True)
            file = 'page_html/' +  ref_id + '_' + picFile
            open(file, 'wb').write(r.content)
        except requests.exceptions.InvalidSchema:
            continue
        except requests.exceptions.MissingSchema:
            continue
        except requests.exceptions.ConnectionError:
            continue


def attachmentHarvest(htmlIn):
    '''
    Harvest attached files as long as they are from the USMAI domain. Has connection error handling if connection rejected. Shoudl only pick up files from USMAI domain server.
    '''
    for a in htmlIn.findAll('a',href=True):
        try:
            urlTemp = (a.attrs['href'])
            if 'http://usmai.umd.edu' not in urlTemp:
                url = 'http://usmai.umd.edu' + urlTemp
            else:
                url = urlTemp
            filePath = url.rsplit('/',1)[1]
            if 'sites/staff/files/' in url or 'sites/default/files' in url:
                r = requests.get(url, allow_redirects=True)
                file = 'page_html/' + ref_id + '_' + filePath
                open(file, 'wb').write(r.content)
                print(url)
        except requests.exceptions.ConnectionError:
            continue 
#        if filePath.rsplit('.',1)[1] not in fileBlacklist:
#            print(filePath)



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
    title = soup.h1.string

    # get content out of id content-area < class content
    post_body_raw = soup.select('#content-area .content')[0]
    
    post_body_raw = clean_html(post_body_raw)
    imgHarvest(post_body_raw)
    attachmentHarvest(post_body_raw)

    post_body = str(post_body_raw)
    pdb.set_trace()
        
    '''
    more processing should be done on this post_body to remove inline styles.
    we just want the plain HTML tags.
    '''

    # save to html
    try:
        file = 'page_html/' +  ref_id + '_' + title + '.html'
        with open(file, 'w+') as f:
            f.write(post_body)
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
