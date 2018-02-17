import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def retrive_html():
    url = "https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search"
    data = {
        "SEMESTER": "S18",
        "MINI": "NO",
        "GRAD_UNDER": "All",
        "PRG_LOCATION": "All",
        "DEPT": "ISM",
        #"LAST_NAME":
        #"FIRST_NAME":
        "BEG_TIME": "All",
        #"KEYWORD":
        "TITLE_ONLY":"YES"
        #SUBMT:
    }
    response = requests.post(url, data)
    if response.status_code == 200:
        return response.text
    else:
        print("retrieve content failed")


def parse_page(file):
    htmlfile = open(file, 'r', encoding='latin-1')  # open a local html file, read only
    htmlpage = htmlfile.read()
    soup = BeautifulSoup(htmlpage, 'html.parser')
    records = []
    # parse Course labels
    labels = []
    ths = soup.find("thead").tr.find_all('th')
    for th in ths:
        labels.append(th.get_text())
    labels[0] = 'Course_id' # consistent with Yunlu's data
    records.append(labels)

    department_titles = soup.find_all('h4', class_="department-title")
    department_tables = soup.find_all('table', class_="table table-condensed table-striped")
    for title, department in zip(department_titles, department_tables):
        name = title.get_text().strip()
        # find each course in the department
        courses = department.find('tbody').find_all('tr')
        for course in courses:
            tds = course.find_all('td')
            record = []
            for i in range(len(tds)):
                attribute = tds[i].get_text().strip()
                # MINI course or not
                if i == 4 and (attribute == '' or attribute == '&nbsp'):
                    attribute = 'N'
                if i in [0, 1, 2] and (attribute == '' or attribute == '&nbsp'):
                    attribute = records[-1][i]
                record.append(attribute)
            records.append(tuple(record))
        # write to csv
        course_df = pd.DataFrame(records[1:], columns=records[0])
        course_df.to_csv('./web-analytics-group15/parser/courses/{}.csv'.format(name))
        records.clear()
        records.append(labels)

parse_page('/Users/guanqiy/CMUCourse/95880/capstone/web-analytics-group15/parser/CMU_courses.htm')