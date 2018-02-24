# CMU Course Analytics Project

This is the the web analytics group project built by Guanqi Yu, Yunlu Huang, Dan Hou for course 95880-A3-SP 2018.
The main page we will use for scrapy and analytics is the [CMU Course Schedule Website](https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search)

## Deliverable 1 - Project Proposal

### **Who are your customers?**
CMU students and staffs.

### **What are their needs?**
Sometimes it's hard to find courses' information through SIO. Students need an easy-to-use/ more interacted friendly web interface for them to make simple query for CMU course. They also needs an insightful course analytics.

### **What specific problem(s) will you solve?**
We want to provide our customers a clearer summary of the courses' information. We plan to offer several choices(which solves different problems), and the customers can choose which problem they would like to inspect based on their needs. The problems we now consider to solve include:
- What courses (eg. in Heinz or SCS) are currently ongoing right now? /Given a time slot, which courses are available?
- What is the beginning time and location of a specific course?
- Which professor/staff teaches most of the courses?
- What are the most popular courses in this semester?
- Which time period has most of the courses?
- Which courses are 3/6/12 units?
- Which building holds most of the courses?
- ...


### **Why do these problems need solved?**
1. Because for simple queries, the process of logging into **SIO** and click **Registration** and search for course number/name is too complex. A simple web interface with the ease of simpler process would be more helpful for specific query.
2. Students/staffs sometimes need some insight of all of the courses in CMU, while SIO doesn't give too much of that.
3. Students can arrange their schedule more efficiently with these problems solved. For example, if a student want to choose a courses between 3:00pm to 6:00, he/she can simply use our platform to search courses.

### **Where are you going to pull the data from?**
 (For Now)[CMU Course Schedule Website](https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search)

## Deliverable 2 - Project Board
[Project Board Link](https://github.com/95880-A3-SP18/web-analytics-group15/projects/1)

## Deliverable 3 - Web Scrapped Data Review
[Web Scrapped Data & Code Link](https://github.com/95880-A3-SP18/web-analytics-group15/tree/master/parser)

## Deliverable 4 - Project Proposal
![Wireframe](https://github.com/95880-A3-SP18/web-analytics-group15/tree/master/docs/images/wireframe.jpeg)

The following are the pictures we drew for the wireframes. Our app will mainly have two page, one is the main page and one is graph page. In the main page, it can list the courses information and search specific courses. In the graph page, it can do some descriptive analysis on the data based on users' choices.

![Main Page](https://github.com/95880-A3-SP18/web-analytics-group15/tree/master/docs/images/MainPage.png)

![Graph Page](https://github.com/95880-A3-SP18/web-analytics-group15/blob/master/docs/images/GraphPage.png)

## Reference

- [CMU Course Find](https://www.cmucoursefind.xyz/)
- [Scotty Lab API](https://scottylabs.org/course-api/)
