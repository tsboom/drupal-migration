import pdb
import importer_utils
import os
import pytest

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test_html'
)

all_html = pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'EDU-CAL-064_test 1.html'),
    os.path.join(FIXTURE_DIR, 'EDU-GR-AC-AGSG-IRSS-014.html'),
    os.path.join(FIXTURE_DIR, 'EDU-GR-INAC-TG-Av18-031_v18_upgrade_privileges.ppt.html'),
    )


@all_html
def test_remove_attachment_table(datafiles):
    for html in datafiles.listdir():
        clean_html = importer_utils.remove_attachment_table(html)
        
        attachments = "<table class=\"sticky-enabled sticky-table\" id=\"attachments\">"
        assert attachments not in clean_html
        
        replacement = "<p>This page has attachments."
        assert replacement in clean_html
