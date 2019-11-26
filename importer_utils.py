from bs4 import BeautifulSoup
import pdb
# function to replace attachment tables in pages 
def remove_attachment_table(page_html):
    soup = BeautifulSoup(page_html, features="html.parser")
    
    attachment_table = soup.find(id="attachments")
    
    replace_string = "<p>This page has attachments. They can be viewed by clicking the \"...\" to the right of the title of this page. See <a href=\"https://usmai.org/confluence/display/MAIN/Working+with+attachments\">this documentation on working with attachments</a> for further explanation of using attachments in Confluence</p>"
    
    clean_soup = page_html
    
    if attachment_table:
        # attachment_table.decompose()
        clean_soup = attachment_table.replace_with(replace_string)
        # clean_soup = soup.html.append(BeautifulSoup(replace_string, features="html.parser"))
        
        # clean_soup = BeautifulSoup(str(soup).replace(attachment_table.text, replace_string), features="html.parser")
    
    return clean_soup