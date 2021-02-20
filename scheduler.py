import requests
from bs4 import BeautifulSoup
from enum import Enum
import os
from login import Connection


def login(email, pswd):
  
        Headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        }

        daSession = requests.Session()
        
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
        print(soup)

        print(login_resp.history[0])
        if len(login_resp.history) != 0:
            if login_resp.history[0].status_code == requests.codes.found:
                
                print("It worked yay")
                return True
        else:
            print("didn't work :(")
            return False

def get_courses(daSession):
     
      id_resp = daSession.get("https://www.gradescope.com/account")
      parsed_id_resp = BeautifulSoup(id_resp.text, 'html.parser')
                
      courses = parsed_id_resp.find_all("a", class_ = "courseBox")
      courses_id =[]
      for course in courses:
        courses_id.append(course.get("href").split("/")[-1])
      print(courses_id)
      return True

login("jdn004@ucsd.edu","put realpass")

#connection = Connection()
#connection.login(os.getenv("login"), os.getenv("password"))
#connection.login("realemail", "realpass")
#connection.get_courses() dsfdsaf
