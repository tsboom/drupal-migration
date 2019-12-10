import pdb
import importer_utils
import os
import pytest
from bs4 import BeautifulSoup

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test_html'
)

# list of test_html files from tests
test_html_files = sorted(os.listdir(FIXTURE_DIR))

# read html files into beautiful soup html and save in list
html_list = []
for file in test_html_files:
    with open(os.path.join('tests', 'test_html', file), 'r') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, features='html.parser')
    html_list.append(soup)


@pytest.mark.parametrize('html', html_list)
def test_remove_attachment_table(html):
    clean_html = importer_utils.remove_attachment_table(html)
    
    attachments = "<table class=\"sticky-enabled sticky-table\" id=\"attachments\">"
    if attachments in html:
        assert attachments not in clean_html
        replacement = "<p>This page has attachments."
        assert replacement in clean_html

@pytest.mark.parametrize('html', html_list)        
def test_fix_relative_links(html):
    fixed_html = importer_utils.fix_relative_links(html)
    
    soup = BeautifulSoup(fixed_html, features='html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        assert href.startswith('http') == True
