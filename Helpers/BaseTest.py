import os
from Helpers.FilePath import get_full_path
os.environ['PROJECTFOLDER'] = get_full_path('')
import unittest
from appium import webdriver
from selenium import webdriver as seleniumWebdriver
import sys

from hotdog.Config import GetConfig

from appium_selector.DeviceSelector import DeviceSelector
import builtins
import threading

from hotdog.BaseTest import HotDogBaseTest

import smtplib
import logging

from Helpers.Results import UploadRegressionResults


class BaseTest(HotDogBaseTest):
    #Reference the New Results File in Helpers Folder
    # that Interacts with the Email Method
    defaultTestResult = UploadRegressionResults


    @classmethod
    def setUpClass(cls, platform='mobile'):
        if not hasattr(builtins, 'threadlocal'):
            runLocal = False
            builtins.threadlocal = threading.local()

            if HotDogBaseTest.SKIP_SELECTOR == 'True':
                # skip device selector, fill in defaults for running locally
                builtins.threadlocal.config = {
                    'desiredCaps': {'browserName': 'Local',
                                    'deviceName': 'Local',
                                    'platformName': 'Local',
                                    'version': 'Local'},
                    'options': {'manufacturer': 'local',
                                'mustard': False,
                                'provider': 'local-' + HotDogBaseTest.LOCAL_BROWSER,
                                'osv': 'Local',
                                'model': 'local',
                                }
                }
            else:
                # use selector to get device/platform
                builtins.threadlocal.config = DeviceSelector(platform=platform).getDevice()[0]
            try:
                builtins.threadlocal = cls.setApp(builtins.threadlocal)
            except:
                raise
            platform = builtins.threadlocal.config['desiredCaps']['platformName']
            if platform.upper() == 'ANDROID':
                builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('ANDROID_APP_URL')
            else:
                builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('IOS_APP_URL')

            provider = builtins.threadlocal.config['options']['provider']
            desired_caps = builtins.threadlocal.config['desiredCaps']
            try:
                if 'grid' in provider:
                    url = GetConfig('GRID_URL') + '/wd/hub'
                elif 'sauce' in provider:
                    url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (
                    GetConfig('SAUCE_USERNAME'), GetConfig('SAUCE_ACCESS'))
                    if desired_caps['browserName'] == 'internet explorer':
                        desired_caps['requireWindowFocus'] = True
                elif provider.lower() == 'local-chrome':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Chrome()
                elif provider.lower() == 'local-firefox':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Firefox()
                elif provider.lower() == 'local-ie':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Ie()
                else:
                    url = GetConfig('GRID_URL') + '/wd/hub'
                if not runLocal:
                    builtins.threadlocal.driver = webdriver.Remote(
                        url,
                        desired_caps
                    )
            except:
                # print("Testcase [%s] COULD NOT START on device [%s]" % (self._testMethodName, self.options['deviceName']))
                print(sys.exc_info()[1])
                raise unittest.SkipTest('Could not launch driver')

    def setUp(self):
        platform = builtins.threadlocal.config['desiredCaps']['platformName']
        if platform.upper() == 'ANDROID':
            builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('ANDROID_APP_URL')
        else:
            builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('IOS_APP_URL')
        super().setUp()

    def assertAlphabetical(self, list):
        for i in range(len(list) - 1):
            assert list[i].lower() < list[
                i + 1].lower(), 'Items not in alphabetical order.  Found entry [%s] before [%s]' % (list[i], list[i + 1])