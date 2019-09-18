# Drupal-migration


## Installation and usage
1. Create a virtual environment using virtualenv. `virtualenv venv`

2. Enter the virtual environment `source venv/bin/activate`

3. Install the requirements `pip install -r requirements.txt`

4. Duplicate login_credentials_sample.py and name the file login_credentials.py. Enter your log-in information or ask me for mine if you don't have the right permissions to see everything. 

5. Run scraper with `python scraper.py`

6. You will see HTML files written to a directory called `page_html` after Firefox gets opened and closed  to scrape one page at a time.If you want to scrape smaller chunks you can modify the sheet range being used in `url_list.py`. 
