CMU_coures.htm: this is a locally saved html file, courses_details.py will read this file and scrape data from it. (Due to some special characteristics the website has, I finally choose to save the source code locally then scrape it)

Course_detail.py: this is used to scrape the pop up window of each course in the website. When each course's id is clicked, a pop up window will appear. It contains some detailed information of this course.
As it will read the CMU_courses.htm, remember to change the file path in the code.

scrapper.py: parse the CMU_courses.htm to extract courses detail information according to different departments

Course_Description.csv: this file is the output of the Course_detail.py.

Courses Dir: Contains all courses information for 18 spring
