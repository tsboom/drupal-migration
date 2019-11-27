from bs4 import BeautifulSoup
import pdb
# function to replace attachment tables in pages 
def remove_attachment_table(page_html):
    soup = BeautifulSoup(page_html, features="html.parser")
    
    attachment_table = soup.find(id="attachments")
    
    replace_string = "<p>This page has attachments. They can be viewed by clicking the \"...\" to the right of the title of this page. See <a href=\"https://usmai.org/confluence/display/MAIN/Working+with+attachments\">this documentation on working with attachments</a> for further explanation of using attachments in Confluence</p>"
    
    if attachment_table:
        # remove attachment table
        attachment_table.decompose()
        
        # add replace_string
        soup.find('div', {"class": "content"}).append(BeautifulSoup(replace_string, 'html.parser'))
        
        clean_soup = str(soup)
    else: 
        clean_soup = page_html
    
    return clean_soup
    
def fix_relative_links(page_html):
    soup = BeautifulSoup(page_html, features="html.parser")
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/'):
            prefix = 'http://usmai.umd.edu'
            link['href'] = prefix + href
            
    fixed_soup = str(soup)
    return fixed_soup