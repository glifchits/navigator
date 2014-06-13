from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import config

driver = webdriver.PhantomJS()
driver.get('https://navigator.wlu.ca/login/student.htm')

driver.find_element_by_id('username').send_keys(str(config.STUDENT_ID))
driver.find_element_by_id('password').send_keys(str(config.PASSWORD))
driver.find_element_by_name('Login').click()

driver.get('https://navigator.wlu.ca/myAccount/co-op/applications.htm')

def html(el):
    return el.get_attribute('outerHTML')

results = []

for table in driver.find_elements_by_tag_name('table'):
    soup = BeautifulSoup(html(table))
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) != 5: continue
        info = [list(cell.stripped_strings) for cell in cells]
        jobinfo, company = info[0]
        jobid, jobtitle = jobinfo.replace('\t','').split('\n')
        jobid = int(jobid[1:-1])
        appdate, pkgname = info[1]
        appdate = datetime.strptime(appdate, "%b %d, %Y %I:%M %p")
        status = info[2][0] if len(info[2]) == 1 else ''
        job = [ jobid, company, jobtitle, appdate, status ]
        results.append(job)

filename = datetime.now().strftime('%Y-%m-%d_%H:%M.csv')
with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for job in results:
        writer.writerow(job)
