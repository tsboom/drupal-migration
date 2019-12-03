import pdb
from bs4 import BeautifulSoup
# function to replace attachment tables in pages 
def remove_attachment_table(soup):
    attachment_table = soup.find(id="attachments")
    
    replace_string = "<p>This page has attachments. They can be viewed by clicking the \"...\" to the right of the title of this page. See <a href=\"https://usmai.org/confluence/display/MAIN/Working+with+attachments\">this documentation on working with attachments</a> for further explanation of using attachments in Confluence</p>"
    
    if attachment_table:
        # remove attachment table
        attachment_table.decompose()
        
        # add replace_string
        soup.find('div', {"class": "content"}).append(BeautifulSoup(replace_string, 'html.parser'))
        
        clean_soup = str(soup)
    else: 
        clean_soup = soup
    
    return clean_soup
    
def fix_relative_links(soup):
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/'):
            prefix = 'http://usmai.umd.edu'
            link['href'] = prefix + href
            
    fixed_soup = str(soup)
    return fixed_soup
    
def write_links(ref_id, soup, f):
    link_list = []
    usmai_links = []
    usmai_links.append(ref_id)
    for link in soup.find_all('a', href=True):
        link_text = link['href']
        if "usmai.umd.edu" in link_text:
            usmai_links.append(link_text)
        else:
            link_list.append(link['href'])
    total_list = usmai_links + link_list
    write_line = ','.join([i for i in total_list]) + '\n'
    f.write(write_line)
    
    
        
        
        
    
    

    