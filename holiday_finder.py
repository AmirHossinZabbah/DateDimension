import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
import time

MONTH_MAPP = {
    'فروردین' : 1,
    'اردیبهشت' : 2,
    'خرداد' : 3,
    'تیر' : 4,
    'اَمرداد' : 5,
    'شهریور' : 6,
    'مهر' : 7,
    'آبان' : 8,
    'آذر' : 9,
    'دی' : 10,
    'بهمن' : 11,
    'اسفند' : 12
    }

YEARS = list(range(1385, 1406))

main_url = 'https://www.time.ir/fa/eventyear-%d8%aa%d9%82%d9%88%db%8c%d9%85-%d8%b3%d8%a7%d9%84%db%8c%d8%a7%d9%86%d9%87'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(main_url)

holiday_dates = set()
for year in YEARS:
    sbox = driver.find_element(By.ID, "ctl00_cphTop_Sampa_Web_View_EventUI_EventYearCalendar10cphTop_3417_txtYear")
    sbox.clear()
    sbox.send_keys(str(year))
    submit = driver.find_element(By.ID, "ctl00_cphTop_Sampa_Web_View_EventUI_EventYearCalendar10cphTop_3417_btnGo")
    submit.click()
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
 
    panel_lst = soup.find_all('div', attrs={'class': 'panel-body'})[1:]
    for panel in panel_lst:
        event_lst = panel.find_all('ul', attrs={'class': 'list-unstyled'})
        for event in event_lst:
            holiday_lst = event.find_all('li', attrs={'class': 'eventHoliday'})
            for holiday in holiday_lst:
                holiday_date = holiday.text.strip().split('\n')[0]
                holiday_day = int(holiday_date.split(' ')[0])
                holiday_month = MONTH_MAPP[holiday_date.split(' ')[1]]
#                 holiday_event = holiday.text.strip().split('\n')[1].strip()
                holiday_dates.add(JalaliDate(year, holiday_month, holiday_day).isoformat())   

pd.DataFrame({'Holiday_Date': sorted(list(holiday_dates))}).to_pickle('exp_data/holiday_dates.pickle')

driver.quit()