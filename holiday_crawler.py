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
        self.years = [str(year) for year in range(self.start_year, self.end_year+1)]

    def write_to_create_csv(self, all_rows, version):
        with open('holidays_'+str(self.start_year)+'_'+str(self.end_year)+'_v'+str(version)+'.csv', 'w+') as fp:
            for row in all_rows:
                fp.write(row)

    def read_csv(self, version):
        file_content = pd.read_csv('holidays_'+str(self.start_year)+'_'+str(self.end_year)+'_v'+str(version)+'.csv')
        print(file_content.head())


    def get_page_contents_of_all_years(self, main_url, end_url =''):
        all_pages = {}
        for year in self.years:
            r = self.get_url_page_content(main_url+year+end_url)
            all_pages[year] = r
        return all_pages

    def get_holidays_from_table(self, all_pages, version):
        all_holiday_tables = {}
        for year in self.years:
            soup = BeautifulSoup(all_pages[year], 'html.parser')
            if version == 1:
                holiday_table = soup.find("table", {"id":"holidays-table"})
                if not holiday_table == None:
                    all_holiday_tables[year] = holiday_table
            elif version == 2:
                holiday_table = soup.find("table")
                if 'holiday-list' in str(holiday_table):
                    all_holiday_tables[year] = holiday_table
        return all_holiday_tables

    def get_rows_from_tables(self, all_holiday_tables, version):
        all_holiday_rows = {}
        for year in self.years:
            all_holiday_rows[year] = []
            holiday_rows = all_holiday_tables[year].find_all('tr')
            if version == 2:
                holiday_rows = holiday_rows[1:]
            for row in holiday_rows:
                if version == 1:
                    if 'data-date' in str(row):
                        all_holiday_rows[year].append(row)
                elif version == 2:
                    all_holiday_rows[year].append(row)
            print('For year {} the number of holidays are  {}'.format(year, len(all_holiday_rows[year])))
        return all_holiday_rows

    def get_holidays_and_occasions(self, all_holiday_rows, version):
        all_holidays_and_occasions = {}
        if version == 1:
            for year in self.years:
                all_holidays_and_occasions[year] = []
                for i in range(len(all_holiday_rows[year])):
                    holiday_date = all_holiday_rows[year][i].find('th').text
                    occasion = all_holiday_rows[year][i].find('a').text
                    all_holidays_and_occasions[year].append([holiday_date, occasion])
        elif version ==2:
            all_holidays_and_occasions = {}
            for year in self.years:
                all_holidays_and_occasions[year] = []
                for i in range(len(all_holiday_rows[year])):
                    this_holidays_data = all_holiday_rows[year][i].find_all('td')
                    date = this_holidays_data[2].text
                    day = this_holidays_data[1].text
                    occasion = this_holidays_data[0].text.strip()
                    all_holidays_and_occasions[year].append([date, day, occasion])
        return all_holidays_and_occasions

    def create_holidays_list(self, all_holidays_and_occasions, version):
        finalized_holidays = []
        if version == 1:
            finalized_holidays.append('Date,Occasion\n')
            month_mappings = {'Jan': '01', 'Feb': '02', 'Mär': '03', 'Apr': '04', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Okt':'10', 'Nov': '11', 'Dez': '12'}
            for year in self.years:
                for row in all_holidays_and_occasions[year]:
                    date = row[0].split()
                    h_date = str(year)+'-'+month_mappings[date[1]]+'-'+date[0].replace('.', '')
                    finalized_row = h_date+','+row[1]+'\n'
                    finalized_holidays.append(finalized_row)
        elif version ==2:
            finalized_holidays.append('Date,Day,Occasion\n')
            month_mappings_2 = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October':'10', 'November': '11', 'December': '12'}
            for year in self.years:
                for row in all_holidays_and_occasions[year]:
                    date = row[0].split()
                    h_date = str(year)+'-'+month_mappings_2[date[0]]+'-'+date[1]
                    row[2] = row[2].replace(',',' ')
                    row[2] = row[2].replace('\n',' ')
                    finalized_row = h_date+','+row[1]+','+row[2]+'\n'
                    finalized_holidays.append(finalized_row)
        return finalized_holidays

    def crawl_website_1(self):
        all_pages = self.get_page_contents_of_all_years(self.version_one_url)
        all_holiday_tables = self.get_holidays_from_table(all_pages, 1)
        all_holiday_rows = self.get_rows_from_tables(all_holiday_tables, 1)
        all_holidays_and_occasions = self.get_holidays_and_occasions(all_holiday_rows, 1)
        return self.create_holidays_list(all_holidays_and_occasions, 1)
    
    def crawl_website_2(self):
        all_pages = self.get_page_contents_of_all_years(self.version_two_start_url, self.version_two_ending_url)
        all_holiday_tables = self.get_holidays_from_table(all_pages, 2)
        all_holiday_rows = self.get_rows_from_tables(all_holiday_tables, 2)
        all_holidays_and_occasions = self.get_holidays_and_occasions(all_holiday_rows, 2)
        return self.create_holidays_list(all_holidays_and_occasions, 2)
        
    
    def run(self):
        self.create_years()
        print('website 1 ...')
        holidays_1 = self.crawl_website_1()
        self.write_to_create_csv(holidays_1, 1)
        print('website 2 ...')
        holidays_2 = self.crawl_website_2()
        self.write_to_create_csv(holidays_2, 2)
        # self.read_csv(1)


