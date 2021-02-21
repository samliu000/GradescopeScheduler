# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from enum import Enum
import os
from assignment import Assignment
# from login import Connection


def login(daSession, email, pswd):
    print("logging in")
    Headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

    init_resp = daSession.get("https://www.gradescope.com/", headers=Headers)
    parsed_init_resp = BeautifulSoup(init_resp.text, 'html.parser')
    
    for cookie in daSession.cookies:
        print (cookie.name, cookie.value)

    for form in parsed_init_resp.find_all('form'):
        if form.get("action") == "/login":
            for inp in form.find_all('input'):
                if inp.get('name') == "authenticity_token":
                    auth_token = inp.get('value')

    login_data = {
        "utf8": "✓",
        "session[email]": email,
        "session[password]": pswd,
        "session[remember_me]": 0,
        "commit": "Log In",
        "session[remember_me_sso]": 0,
        "authenticity_token": auth_token,
    }
    login_resp = daSession.post("https://www.gradescope.com/login", params=login_data)

    html=daSession.get("https://www.gradescope.com/account")
    soup = BeautifulSoup(html.text, "html.parser")
    #print(soup)

    #print(login_resp.history[0])
    if len(login_resp.history) != 0:
        if login_resp.history[0].status_code == requests.codes.found:
            print("Login Success")
            #print("It worked yay")
            return True
    else:
       # print("didn't work :(")
        return False

# get course URLS
def get_courses(daSession):
     
    id_resp = daSession.get("https://www.gradescope.com/account")
    parsed_id_resp = BeautifulSoup(id_resp.text, 'html.parser')
    
    # Find current courses
    currentCourse = parsed_id_resp.find("div", class_ = "courseList--coursesForTerm")
  #  print("\nPrinting first quarter: ")
    #print(currentCourse)

    # Get all the href url for the current courses
    courses = currentCourse.find_all("a" , class_ = "courseBox")
    courses_id =[]
    for course in courses:
        courses_id.append("https://www.gradescope.com" + course.get("href"))
    
    print("Printing all course URLs")
    print(courses_id)

    return courses_id



# use course URL to get assignment list
# @returns: 
def getAssignments(courseURL, daSession):

  id_resp = daSession.get(courseURL)
  parsed_id_resp = BeautifulSoup(id_resp.text, 'html.parser')

  # find table
  tableOfAssignment = parsed_id_resp.find("table", {"id":"assignments-student-table"})
  # print("\nPrinting table")
  #  print(tableOfAssignment)

  # find all assignemnts
  assignmentList = tableOfAssignment.find_all("tr", {"role":"row"})
  #  print("\nPrinting assignment list")
  # for assign in assignmentList:
  #     print(assign)

  listOfAssignments = []

  # for each assignment, find its title, due date, due time
  for assignment in assignmentList:
    # find title
    allText = assignment.text

    print("printing assignment");
    print(allText)

    title = "Filler"
    
    if(allText.find('Submitted') >= 0):
      submitIndex = allText.find('Submitted')
      title = allText[0:submitIndex]  
    elif(allText.find("No Submission") >= 0): 
      noSubmitIndex = allText.find('No Submission')
      title = allText[0:noSubmitIndex]
    else :
      slashIndex = allText.find('/')
      title = allText[0:slashIndex - 1]

    # find due date/time
    if(allText.find('Due Date') < 0):
      continue
    indexOfDueDate = allText.find('Due Date') + 10
    time = allText[indexOfDueDate:indexOfDueDate+17]
    
    listOfAssignments.append(Assignment(title, time))
    hi = Assignment(title, time)
    

  # for hi in listOfAssignments:
  #   print(hi.title + " " + hi.dueDateTime)
  return listOfAssignments

    

