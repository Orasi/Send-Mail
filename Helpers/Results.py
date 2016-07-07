import unittest
import builtins
import smtplib
import logging

# from Helpers.BaseTest import BaseTest
from sauceclient import SauceClient

class UploadRegressionResults(unittest.TestResult):

    #Logging Setup for Sending and Writing the Email Method
    global logger
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    smtp_user = 'orasigeolock@gmail.com'
    smtp_pass = 'Orasi01!geolock'

    email_list =  {
        "brian.menzies@orasi.com",
        # "matt.watson@orasi.com",
    }
    # deviceAddress = '127.0.0.1'
    # devicePort = '7505'
    results_file_name = 'results.txt'


    def send_mail(self, results):
        sender = 'orasigeolock@gmail.com'
        # receivers = ['brian.menzies@orasi.com']
        subject = 'Clearleap Mobile Regression Test Results'
        message = 'FROM: orasigeolock@gmail.com\n' + \
                  'To: brian.menzies@orasi.com\n' + \
                  'Subject:' + subject + '\n\n' \
                                         'Mobile Regression Test Results:  \n' + results

        for to_address in self.email_list:
            try:
                smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
                smtpObj.starttls()
                smtpObj.ehlo()
                smtpObj.login(self.smtp_user, self.smtp_pass)
                smtpObj.sendmail(sender, [to_address], message)
                logger.info("Successfully sent email")
            except smtplib.SMTPException as e:
                logger.info("Error: unable to send email:" + str(e))