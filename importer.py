from atlassian import Confluence
from bs4 import BeautifulSoup
import datetime
import csv
import os
import pdb
import time
import pprint
import url_list
import importer_utils


# log file 
today = datetime.datetime.today().strftime("%Y%m%d")
now = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
importer_log = f'importer_log_{today}'

# write start of log
with open(importer_log, 'a+') as f:
    f.write(f"\n\n\n --- importer started {now}\n\n\n")

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
        # url='https://usmai-wwwdev.lib.umd.edu/portal',
        url='https://usmai-wwwdev.lib.umd.edu/portal',
        username='admin',
        password='COOKIN1586')
    return confluence
confluence = login_confluence()
    
# external link tracking filepath

external_links_file = f"external_links_{today}.csv"
internal_links_file = f"internal_links_{today}.csv"

# get spreadsheet values from content audit 
row_values = url_list.get_content_audit_values()

# loop over files in page_html directory
# page_directory = '../page_html'
page_directory = os.path.abspath('page_html')
attachments_dir = os.path.abspath('attachments')
imgs_dir = os.path.abspath('imgs')

for file in sorted(os.listdir(page_directory)):
    
    if file.endswith('.html'):
        # get html into a variable
        with open(page_directory+ '/' + file, 'r') as f:
            page_html = f.read()
        
        # create soup
        soup = soup = BeautifulSoup(page_html, features="html.parser")
        
        # get filename without the html at the end and remove leading/trailing whitespace
        page_title = os.path.splitext(file)[0].strip()
        # find ref id
        ref_id = page_title.split('_')[0]
        
        # fix relative links so they link to usmai.umd.edu 
        page_html = importer_utils.fix_relative_links(soup)
        
        # write columns of external links 
        with open(external_links_file, 'a+', newline='') as f_ext, open (internal_links_file, 'a+', newline='') as f_int:
            ext_writer = csv.writer(f_ext, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            int_writer = csv.writer(f_int, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            importer_utils.write_links(ref_id, soup, ext_writer, int_writer)
        
        # take out attachments table
        page_html = importer_utils.remove_attachment_table(soup)
        
    
        '''
        targeted space import
        '''
        # find the space for the row
        space = 'NA'
        for row in row_values: 
            if len(row) > 2: 
                if ref_id == row[0]:
                    try:    
                        space = row[8]
                    except:
                        with open(importer_log, 'a+') as f:
                            f.write(f"ERROR: row is missing send to space value\n{row}\n")

        #create page if space is not NA 
        if space != "NA": 
            
            space = space_mapping[space]
        
            # Check page exists
            exists = confluence.page_exists(space, page_title)
            # get page_id
            page_id = confluence.get_page_id(space, page_title)

            # create page if it doesn't exist
            if not exists: 
                file_status = confluence.create_page(space, title=page_title, body=page_html, parent_id=None, type='page', representation='storage')
                
                # get page_id of page that just uploaded
                page_id = confluence.get_page_id(space, page_title)
                try:
                    print(file_status['title'] + " created in " + space + " space\n")
                    with open(importer_log, 'a+') as f:
                        f.write(file_status['title'] + " created in " + space + " space\n")
                except:
                    # for some reason some pages that do exist are coming up as False  in the .page_exists method. 
                    print(page_title + 'already exists.\n')
            else:
                update_status = confluence.update_page(parent_id=None, page_id=page_id, title=page_title, body=page_html, type='page', representation='storage')
                try:
                    print(update_status['title'] + " updated in " + space + " space\n")
                    with open(importer_log, 'a+') as f:
                        f.write(update_status['title'] + " updated in " + space + " space\n")
                except:
                    with open(importer_log, 'a+') as f:
                        f.write(f"update_page {page_title} failed\n")
            
            # find matching images imgs directory
            for file in os.listdir(imgs_dir):
                img_ref_id = file.split('_')[0]
                filename = 'imgs/' + file
                if ref_id == img_ref_id:
                    file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space=space, comment=None)
                    try:
                        print('\t' + file_status['metadata']['comment']+'\n')
                        with open(importer_log, 'a+') as f:
                            f.write('\t3 ' + file_status['metadata']['comment']+'\n')
                    except KeyError:
                        try:
                            if file_status['statusCode'] == 500:
                                print(f"'img attachment {filename} failed because of 500 server error\n")
                                with open(importer_log, 'a+') as f:
                                    f.write(f"ERROR: img attachment {filename} failed because of 500 server error\n")
                                continue
                        except:
                            print('\t' + file_status['results'][0]['metadata']['comment']+'\n')
                            with open(importer_log, 'a+') as f:
                                f.write('\t4 '+file_status['results'][0]['metadata']['comment']+'\n')
                    except:
                        print('\t' + filename)
            
            
            # find matching attachments in attachments directory
            for file in os.listdir(attachments_dir):
                attachment_ref_id = file.split('_')[0]
                filename = 'attachments/' + file
                if ref_id == attachment_ref_id:
                    file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space=space, comment=None)
                    try:
                        print('\t' + file_status['metadata']['comment'])
                        with open(importer_log, 'a+') as f:
                            f.write('\t1 ' + file_status['metadata']['comment'] + '\n')
                    except KeyError:
                        try:
                            if file_status['statusCode'] == 500:
                                print(f"attachment {filename} failed because of 500 server error\n")
                                with open(importer_log, 'a+') as f:
                                    f.write(f"attachment {filename} failed because of 500 server error\n")
                                continue
                        except:
                            print('\t' + file_status['results'][0]['metadata']['comment'])
                            with open(importer_log, 'a+') as f:
                                f.write('\t2 '+ file_status['results'][0]['metadata']['comment']+'\n')
                    except: 
                        print('\t' + filename)
        
# write end of log
end_now = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
with open(importer_log, 'a+') as f:
    f.write(f"\n\n\n --- importer ended {end_now}\n\n\n")
