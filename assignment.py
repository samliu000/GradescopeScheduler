class Assignment:
  def __init__(self, title, dueDateTime):
    '''Create a course object that has lazy eval'd assignments'''
    self.title = title
    self.dueDateTime = dueDateTime
  
  def __str__(self):
    return "Title: " + self.title + " DueTime: " + self.dueDateTime
