import pandas as pd
import requests
from bs4 import BeautifulSoup

class HolidayCrawler:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.version_one_url = "https://www.timeanddate.com/holidays/iran/"
        self.version_two_start_url = "https://calendarific.com/holidays/"
        self.version_two_ending_url = "/IR"
        self.years = []
    
    def get_url_page_content(self, url):
        r = requests.get(url)
        if not r.status_code == 200:
            raise RuntimeError('Problem accessing page data.')
        return r.text
    
    def create_years(self):
        self.year = [str(year) for year in range(self.start_year, self.end_year+1)]

    def write_to_create_csv(self, all_rows, version):
        with open('holidays_'+str(self.start_year)+'_'+str(self.end_year)+'_v'+str(version)+'.csv', 'w+') as fp:
            for row in all_rows:
                fp.write(row)

    def read_csv(self, version):
        file_content = pd.read_csv('holidays_'+str(self.start_year)+'_'+str(self.end_year)+'_v'+str(version)+'.csv')
        print(file_content.head())
    
    def run(self):
        self.create_years()
        self.write_to_create_csv([], 1)
        self.read_csv(1)