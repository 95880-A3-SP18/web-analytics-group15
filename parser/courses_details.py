"""
This file is used to scrape detailed descriptions of each course
Author: Yunlu Huang
"""
from bs4 import BeautifulSoup
import pandas as pd
import os, sys, re, requests

def getCoursesDict(file):
    """
    This function is used to scrape the courses' urls from the CMU course website
    :param file: the local saved cmu course file
    :return: a course dictionary which save {course_id:course_url} pairs
    """
    print("Begin getCoursesDict()")
    htmlfile = open(file, 'r', encoding='latin-1')   # open a local html file, read only
    htmlpage = htmlfile.read()
    soup = BeautifulSoup(htmlpage, "html.parser")   # get a soup instance by the html file

    course_dict = {}   # save the courses id and the url
    find_url = re.compile(r'\'(.*?)\'')
    # find all courses in each department
    for department in soup.find_all('table', class_="table table-condensed table-striped"):
        # find each course in the department
        for courses in department.find('tbody').find_all('tr'):
            # find the course id column
            course_col = courses.find('td').find('a')
            # if the course id column has content
            if course_col is not None:
                href = course_col.get('onclick')
                full_url = "https://enr-apps.as.cmu.edu{}".format(find_url.findall(href)[2])
                course_id = course_col.get_text()
                course_dict[course_id] = full_url
    print("End getCoursesDict()")
    return course_dict


def getCourseDF(course_dict):
    """
    Scrape the detailed information from each course's url
    :param course_dict: the course dictionary which save {course_id:course_url} pairs
    :return: a dataframe object which save all courses' information
    """
    print("Begin getCourseDF()")
    total_list = [['Course_id', 'Course_url',
                   'Related URLs', 'Special Permission Required', 'Prerequisites',
                   'Corequisites', 'Cross-Listed Courses', 'Notes',
                   'Description']]   # the header of the dataframe

    for key, value in course_dict.items():
        response = requests.get(value)
        course_soup = BeautifulSoup(response.text, "html.parser")

        single_list = []   # this is used to save single course's information
        single_list.append(key)
        single_list.append(value)
        for row in course_soup.find_all('div', class_="col-md-6"):
            if (row.find('dt').get_text() == 'Related URLs'):
                try:
                    single_list.append(row.find('a').get_text())
                 except:
                    single_list.append('None')
            if (row.find('dt').get_text() == 'Special Permission Required'):
                single_list.append(row.find('dd').get_text())
            if (row.find('dt').get_text() == 'Prerequisites'):
                single_list.append(row.find('dd').get_text())
            if (row.find('dt').get_text() == 'Corequisites'):
                single_list.append(row.find('dd').get_text().strip())
            if (row.find('dt').get_text() == 'Cross-Listed Courses'):
                single_list.append(row.find('dd').get_text().strip())
            if (row.find('dt').get_text() == 'Notes'):
                single_list.append(row.find('dd').get_text().strip())
        description = course_soup.find('p', class_="text-left").get_text()
        single_list.append(description)
        total_list.append(single_list)

    course_df = pd.DataFrame(total_list[1:], columns=total_list[0])
    print("End getCourseDF()")
    return course_df


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))
    course_dict = getCoursesDict('/Users/yunlu/PycharmProjects/test/CMU_courses.htm')  # change the path to your path
    course_df = getCourseDF(course_dict)
    course_df.to_csv('Courses_Description.csv')
