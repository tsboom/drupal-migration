from atlassian import Confluence
import os
import pdb
import url_list



confluence = Confluence(
    url='https://usmai-wwwdev.lib.umd.edu/confluence',
    username='admin',
    password='COOKIN1586')


# loop over files in page_html directory
page_directory = 'page_html'

for file in os.listdir(page_directory):
    print(file)
    if file.endswith('.html'):
        # get html into a variable
        with open(page_directory+ '/' + file, 'r') as f:
            page_html = f.read()

        # get filename without the html at the end
        page_title = os.path.splitext(file)[0]

        # find related attachments
        ref_id = file.split('_')[0]

        # get page_id
        page_id = confluence.get_page_id('USMAI', page_title)
        pdb.set_trace()
        
        # find matching attachments in imgs directory
        for file in os.listdir('imgs'):
            img_ref_id = file.split('_')[0]
            filename = 'imgs/' + file
            if ref_id == img_ref_id:
                file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space='USMAI', comment=None)
                print(file_status)


        # find matching attachments in attachments directory
        for file in os.listdir('attachments'):
            attachment_ref_id = file.split('_')[0]
            filename = 'attachments/' + file
            if ref_id == attachment_ref_id:
                file_status = confluence.attach_file(filename, name=file, content_type=None, page_id=page_id, title=None, space='USMAI', comment=None)
                print(file_status)
