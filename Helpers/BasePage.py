import os
from Helpers.FilePath import get_full_path
os.environ['PROJECTFOLDER'] = get_full_path('')
from hotdog.BasePage import HotDogBasePage
from appium.webdriver.common.mobileby import MobileBy as By
from hotdog.FindEither import FindEither
from random import randint
from time import sleep
import time

class ClearleapBasePage(HotDogBasePage):

    btn_screen_mirroring = (By.ID, 'showcase_button')
    loading_indicator = (By.ID, 'progress')
    cast_overlay = FindEither(selectors=[[By.NAME, 'OK']])

    def __init__(self, driver=None, url=None, sync=True):
        self.driver = driver
        super().__init__(driver, url)
        if sync:
            self.wait_for_loading()
            self.checkForCastOverlay()

    def checkForCastOverlay(self):
        present = self.is_element_present('cast_overlay', timeout=1)
        if present:
            self.cast_overlay.click()

    def sync(self, timeout=20):
        sleep(1)
        self.wait_for_loading()
        super().sync(timeout=timeout)

    def wait_for_loading(self, timeout=15):
        startTime = time.time()
        loading = self.is_element_present('loading_indicator', timeout=3)
        while loading:
            time.sleep(1)
            loading = self.is_element_present('loading_indicator')

            if time.time() - startTime > timeout:
                break
                #raise Exception('Timeout waiting for Loading Indicator. Timeout=[%s]' % timeout)
        return self

    def swipe(self, swipe_count=1, direction='up', element=None):
        while swipe_count != 0:
            if direction.lower() == 'down':
                if element is not None:
                    start_x = element.location['x']/2
                    end_x = start_x
                    start_y = element.location['y']
                    end_y = self.driver.get_window_size()['height'] - 100
                else:
                    size = self.driver.get_window_size()
                    start_x = size['width']/2
                    end_x = start_x
                    start_y = size['height'] * .2
                    end_y = size['height'] * .8
                self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
            else:
                super().swipe(direction, element, duration=1000)
            sleep(1.5) # Wait for scrolling to catch up
            swipe_count -= 1

    def get_random_asset(self, swipes=10):
        size = self.driver.get_window_size()
        start_x = size['width']/2
        end_x = start_x
        start_y = size['height'] * .85
        end_y = size['height'] * .225

        for i in range(randint(0, swipes)):
            self.driver.swipe(start_x, start_y, end_x, end_y, 1000)

        # Get a random series and store the image and episode title in a dictionary
        images = self.driver.find_elements_by_id('featured_image')
        titles = self.driver.find_elements_by_id('episode_title')
        # Movies tab doesn't display featured items
        if len(images) == 0 and len(titles) == 0:
            images = self.driver.find_elements_by_id('episode_image')
            titles = self.driver.find_elements_by_id('title')
            if images[0].location['y'] + 100 < titles[0].location['y']:
                images.elements.pop(0)
            if images[-1].location['y'] - 100 > titles[-1].location['y']:
                images.elements.pop(-1)
        random_int = randint(0, len(titles) - 1)
        if len(images) > len(titles):
            random_int -= 1
        dictionary = {'image' : images[random_int], 'title' : titles[random_int]}
        return dictionary