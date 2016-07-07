import unittest

class EmailList(unittest.TestResult):
    #This serves as the place for the email addresses that will receive the
    #Results from teh tests run and can be overwritten by a Jenkins project
    #Post-Build process and inherit the projects' file

    email_list =  {
        "brian.menzies@orasi.com"
        # "matt.watson@orasi.com",
    }