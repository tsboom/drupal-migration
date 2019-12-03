from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
import os
import pdb
import url_list
import importer_utils


# space name from content audit to space key mapping
space_mapping = {
    "Archive": "Archive",
    "CLD": "CLD",
    "EBOOK": "EBOOK",
    "IRSS": "IRSS",
    "Main": "MAIN",
    "META":"MS",
    "RALS":"RALS",
    "RALS-ERM": "ERMTNTG",
    "RIS": "RIS",
    "SAS": "SAS",
    "SPASS": "SPASS",
    "UES": "UES"
    }
    
def login_confluence():
    # log in credentials for confluence api
    confluence = Confluence(
        url='https://usmaidev.org/portal',
        username='admin',
        password='COOKIN1586')
    return confluence
confluence = login_confluence()
    
# external link tracking filepath
today = datetime.datetime.today().strftime('%Y%m%d')
links_file = f"external_links_{today}.csv"

# get spreadsheet values from content audit 
row_values = url_list.get_content_audit_values()

# loop over files in page_html directory
# page_directory = '../page_html'
page_directory = os.path.abspath('page_html')

for file in sorted(os.listdir(page_directory)):
    print(file)
    if file.endswith('.html'):
        # get html into a variable
        with open(page_directory+ '/' + file, 'r') as f:
            page_html = f.read()
        
        # create soup
        soup = soup = BeautifulSoup(page_html, features="html.parser")
        # take out attachments table
        page_html = importer_utils.remove_attachment_table(soup)
        
        # fix relative links so they link to usmai.umd.edu 
        page_html = importer_utils.fix_relative_links(soup)
        
        # get filename without the html at the end
        page_title = os.path.splitext(file)[0]
        # find ref id
        ref_id = file.split('_')[0]

        # write columns of external links 
        with open(links_file,'a+') as f:
            importer_utils.write_links(ref_id, soup, f)

        '''
        targeted space import
        '''
        # find the space for the row
        space = 'NA'
        for row in row_values: 
            if len(row) > 2: 
                if ref_id == row[0]:
                    space = row[8]
                    
        #create page if space is not NA 
        if space != "NA": 
            
            space = space_mapping[space]
            
            # create the page if doesn't exist, update if exists
            # Check page exists
            exists = confluence.page_exists(space, page_title)
            # get page_id
            page_id = confluence.get_page_id(space, page_title)
            # create page if it doesn't exist
            if not exists: 
                file_status = confluence.create_page(space, title=page_title, body=page_html, parent_id=None, type='page', representation='storage')
                print(file_status)
            else:
                update_status = confluence.update_page(parent_id=None, page_id=page_id, title=page_title, body=page_html, type='page', representation='storage')
                print(update_status)
            
            # find matching attachments in imgs directory
            for file in os.listdir(os.path.abspath('imgs')):
                img_ref_id = file.split('_')[0]
                filename = 'imgs/' + file
                if ref_id == img_ref_id:
                    file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space=space, comment=None)
                    print(file_status)


            # find matching attachments in attachments directory
            for file in os.listdir(os.path.abspath('attachments')):
                attachment_ref_id = file.split('_')[0]
                filename = 'attachments/' + file
                if ref_id == attachment_ref_id:
                    file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space=space, comment=None)
                    print(file_status)

