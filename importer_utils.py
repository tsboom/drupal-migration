import pdb
from bs4 import BeautifulSoup
# function to replace attachment tables in pages 
def remove_attachment_table(soup):
    attachment_table = soup.find(id="attachments")
    
    replace_string = "<p>This page has attachments. They can be viewed by clicking the \"...\" to the right of the title of this page. See <a href=\"https://usmai.org/portal/display/MAIN/Working+with+attachments\">this documentation on working with attachments</a> for further explanation of using attachments in Confluence</p>"
    
    if attachment_table:
        # remove attachment table
        attachment_table.decompose()
        
        # add replace_string
        soup.find('div', {"class": "content"}).append(BeautifulSoup(replace_string, 'html.parser'))
        
        clean_soup = str(soup)
    else: 
        clean_soup = str(soup)
    
    return clean_soup
    
def fix_relative_links(soup):
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith('/'):
            prefix = 'http://usmai.umd.edu'
            link['href'] = prefix + href
            
    fixed_soup = str(soup)
    return fixed_soup
    
def write_links(ref_id, soup, ext_writer, int_writer):
    external_links = []
    external_links.append(ref_id)
    usmai_links = []
    usmai_links.append(ref_id)
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        # skip anchor tags and emails
        if '#' in href or 'mailto:' in href:
            continue
        else: 
            # save usmai links
            if "usmai.umd.edu" in href:
                usmai_links.append(href)
            else:
                # save external links
                external_links.append(href)

    # write links to csvs
    int_writer.writerow(usmai_links)
    ext_writer.writerow(external_links)
    
    
        
        
        
    
    

    