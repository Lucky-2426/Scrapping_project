from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

import os
import json
from random import uniform
import time
from datetime import datetime
import pandas as pd

from new_key_enum import Keys_enum

WAIT_XS = 0.05
WAIT_S = 0.5
WAIT_M = 4
WAIT_L = 10


class Driver(webdriver.Chrome):

    """
    ------------- Aim --------------
    Initialize the driver

    ---------- Parameters ----------
    (TYPE)       | NAME           | DESCRIPTION
    (Bool)       | run_background | Decides if the driver is executed on background
    """
    def __init__(self, email_usr, password, dataset, run_background = False):

        # Initialize the ChromeDriver
        DRIVER_PATH = os.path.join('..', '3. Driver', 'chromedriver.exe') 
        options = webdriver.ChromeOptions()
        # Make the window fullscreen at the start of the driver
        options.add_argument("--start-maximized")
        if run_background:
            # Run on background (less ressources used)
            options.add_argument("--headless")
        # Webdriver.Chrome constructor
        super().__init__(options = options, executable_path = DRIVER_PATH)
        
        # Get all the json file elements
        self.my_by_dict = {'NAME': By.NAME, 'CLASS': By.CLASS_NAME, 'ID': By.ID, 'XPATH': By.XPATH, 'CLASS_NAME': By.CLASS_NAME}
        self._load_json_elements()

        # Map the name called and the functions
        self.function_dict = {'Load'        : self.load_url,
                              'Fill'        : self.fill,
                              'Click'       : self.clickButton,
                              'Wait'        : self.wait,
                              'Get'         : self.get_page_contents,
                              'Scrap'       : self.scrap_element_on_page,
                              'Refresh'     : self.refresh_page,
                              'Export'      : self.export_data,
                              'Sleep'       : self.force_sleep,
                              'Scroll'      : self._scroll_on_page,
                              'Get elements': self.get_content_from_element_object,
                              'Get object'  : self.get_element_object,
                              'Close'       : self.close_driver
                             }

        # Initialize usefull variables
        self.attributes_scraped = set()
        self.elements_object = []
        self.email_usr = email_usr
        self.password  = password
        self.dataset = dataset

    """
    ------------- Aim --------------
    Driver loads a given url.

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | url           | Url to be loaded
    """
    def load_url(self, url = ""):
        if url == "":
            self.dataset.variables["urls_index"][0] += 1
            self.get(self.dataset.variables["urls"][self.dataset.variables["urls_index"][0]])
        else: 
            self.get(url)

    def close_driver(self):
        self.close()

    """
    ------------- Aim --------------
    Load page elements from login.json
    """
    def _load_json_elements(self):
        f = open(os.path.join('..', '7. Config', 'login.json'))
        self.page_elements = json.load(f)['page_elements']
        f.close()

    """
    ------------- Aim --------------
    Load login credentials from a json file

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | path          | Name of the file to load
    ------------ Output ------------
    (TYPE)       | NAME        | DESCRIPTION
    (dict)       | credentials | Dict of loaded credentials
    """
    # TODO a refaire
    def _load_json_credentials(self, path):
        f = open(os.path.join('..', '7. Config', path))
        credentials = json.load(f)['credentials']
        f.close()    
        return credentials   

    """
    ------------- Aim --------------
    Maps a given action to the corresponding function and executes it with given arguments

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | action        | Action to execute
    (dict)       | args          | Arguments for the execution
    """
    def do(self, action, args):
        self.function_dict[action](**args)

    """
    ------------- Aim --------------
    Returns random value for timeout

    ------------ Output ------------
    (TYPE)       | NAME   | DESCRIPTION
    (int)        |        | Random int
    """
    def _timeout(self):
        return uniform(4, 6)

    """
    ------------- Aim --------------
    Waits for a given duration

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (int)        | duration      | Duration to wait
    """
    def force_sleep(self, duration):
        time.sleep(duration)

 
    """
    ------------- Aim --------------
    Wait for an element to be loaded on the page

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | element_name  | Name of the element to be waited
    """   
    def wait(self, element_name):
        # get the enum and tag for the element
        enum, tag = self._send_elements_info(element_name)
        try:
            element_present = EC.presence_of_element_located((enum, tag))
            WebDriverWait(self, self._timeout()).until(element_present)
        except TimeoutException:
            pass

    """
    ------------- Aim --------------
    Refreshes the current page and waits for a given element to be loaded

    ---------- Parameters ----------
    (TYPE)       | NAME             | DESCRIPTION
    (str)        | wait_for_element | Element to wait for after refreshing the page
    """
    def refresh_page(self, wait_for_element):
        self.refresh()
        self.wait(wait_for_element)

    """
    ------------- Aim --------------
    Fills a specific field with given keys

    ---------- Parameters ----------
    (TYPE)          | NAME          | DESCRIPTION
    (str)           | element_name  | Name of the field element to fill
    (str) or (list) | key           | Key or list of keys to be sent to the field
    """
    # TODO a refaire
    def fill(self, element_name, key):
        # get the enum and tag for the element
        enum, tag = self._send_elements_info(element_name)
        page_line_edit = self.find_element(enum, tag)
        # Clear the field (sometimes text is already input)
        page_line_edit.clear()
        if "email_usr" in key:
            key = self.email_usr
        elif "password" in key:
            key = self.password
        # Verify if the input is a list
        if isinstance(key, list):
            for k in key:
                # Verify if the key is a specific key_enum or text
                if "Keys_enum" in k:
                    page_line_edit.send_keys(Keys_enum[k.split(".")[1]].value)
                else:
                    page_line_edit.send_keys(k)
        else:
            if "Keys_enum" in key:
                page_line_edit.send_keys(Keys_enum[key.split(".")[1]].value)
            else:
                page_line_edit.send_keys(key)

    """
    ------------- Aim --------------
    Clicks on a given button and waits for an element to be loaded on the page if specified

    ---------- Parameters ----------
    (TYPE)       | NAME             | DESCRIPTION
    (str)        | element_name     | Name of the button element to be clicked
    (str)        | wait_for_element | Element to wait for if specified
    """    
    def clickButton(self, element_name, wait_for_element = '', error_handling = False):
        # get the enum and tag for the button
        enum, tag = self._send_elements_info(element_name)
        try:
            self.find_element(enum, tag).click()
#            ActionChains(self).move_to_element(self.find_element(enum, tag)).click().perform()

            if wait_for_element != '':
                self.wait(wait_for_element)
            time.sleep(WAIT_S)
        except Exception as e:
            if error_handling:
                self.refresh()
                self.force_sleep(5)
                self.clickButton(element_name)
            else:
                print(e)
                print("Impossible d'appuyer sur le bouton: ", tag)
    
    """
    ------------- Aim --------------
    Export data to a given file. If data is not specified, exports the scraped page content

    ---------- Parameters ----------
    (TYPE)       | NAME      | DESCRIPTION
    (str)        | path      | Name of the export file
    (list)       | data      | Data to be exported
    """
    def export_data(self, path, data = None, columns = []):
        try:
            if data is not None:
                with open(path, 'a+') as file:
                    for row in data:
                        file.write(str(row) + '\n')
            else:
                # TODO à refaire
                filename = os.path.join('..', '2. Exports', '1. Export scraper', str(datetime.now().strftime("%Y_%m_%d-%H_%M")) + '-' + path + '.xlsx')
                print(filename)
                if not columns:
                    export_df = pd.DataFrame(self.dataset.variables['page_content'])
                else:
                    export_df = pd.DataFrame(self.dataset.variables['page_content'], columns = columns)
                print(export_df.columns)
                export_df.to_excel(filename)
        except Exception as e:
            print(e)
    
    """
    ------------- Aim --------------
    Scrap one or several elements on a page. If needed, the program will automaticaly scroll down.
    You can stipulate the page_locator togo to the following page and this will be repeated until
    you reach the page_limit. To click on the next paxt, you also have to specify the page_button
    element that must be stocked in the json file.
    If you are not able to reach the following page, you can specify a on_error event to perform
    another action.

    ---------- Parameters ----------
    (TYPE)          | NAME                | DESCRIPTION
    (str)           | element_name        | Element to reach on the page as it is defined in the json file
    (str) or (list) | attribute_to_get    | Element to get on the page specified 
    (str)           | password_user       | User's password to connect to LinkedIn

    ------------ Output ------------
    (TYPE)          | NAME                | DESCRIPTION
    (webdriver)     | driver              | The Chrome webdriver object logged on LinkedIn.
    """
    def scrap_element_on_page(self, element_name, attribute_to_get = '', page_locator = '', page_button = '', page_limit = -1, on_error = ''):
        enum, tag = self._send_elements_info(element_name)
        try:
            page_enum, page_tag = self._send_elements_info(page_locator)
            # number of pages detected to scrap
            number_of_pages = len(self.find_elements(page_enum, page_tag))
        except:
            pass


        # Max number of pages to scrap if page limit is not specified
        if page_limit == -1:
            page_limit = 1000000

        # TODO
        number_of_pages = 40
        for current_page in range(number_of_pages):
            
            # Scroll to the first element on the list of elements to scrap
            els = self.find_elements(enum, tag)
            self.execute_script("arguments[0].scrollIntoView();", els[0])
            time.sleep(2)
            current_view = 0

            # Scroll down on the page to let every element appear
            while current_view != len(els):
                els = self.find_elements(enum, tag)
                self.execute_script("arguments[0].scrollIntoView();", els[current_view])
                current_view += 1
                time.sleep(WAIT_XS)

            # Scrap all the wanted elements on the page
            element_scraped = self.find_elements(enum, tag)

            # Extract the attribute from the job offer
            for sub_part in element_scraped:
                attribute_data = sub_part.get_attribute(attribute_to_get)
                self.attributes_scraped.add(attribute_data)

            # Export data page by page
            for url in list(self.attributes_scraped):
                self.dataset.variables["urls"].append(url)
            self.export_data(os.path.join('..', '2. Exports', '1. Export scraper', 'elements_extracted.txt'), list(self.attributes_scraped))
            self.attributes_scraped.clear()
            
            # Verify if page limit is reached
            if current_page == page_limit - 1:
                break
            else:
                next_page_enum, next_page_tag = self._send_elements_info(page_button)
                if next_page_enum == By.XPATH:
                    res = next_page_tag.split('|')
                    new_tag = "//" + res[0] + "[contains(" + res[1] + ", '" + res[2] + str(current_page+2) + "')]"
                else:
                    new_tag = next_page_tag
                
                try:
                    self.find_element(next_page_enum, new_tag).click()
                    print('SUCCEEDED TO CLICK ON PAGE ', str(current_page + 2))
                except:
                    if on_error != '':
                        print('-----------------------------ERROR--------------------------')
                        res = on_error.split('|')
                        new_tag = "//" + res[0] + "[contains(" + res[1] + ", \"" + res[2] + str((current_page+1)*int(res[3])) + "\")]"
                        print(new_tag)
                        self.get(self.find_element(next_page_enum, new_tag).get_attribute("href"))
                    else:
                        print('Did not find: ', str(next_page_enum), str(new_tag))
                        break

    """
    ------------- Aim --------------
    Scraps the specified elements on the current page

    ---------- Parameters ----------
    (TYPE)          | NAME          | DESCRIPTION
    (str) or (list) | element_name  | Name or list of names of elements to be scraped on current page
    """
    def get_page_contents(self, element_name, attribute):
        current_page_element = []
        current_page_element.append(self.current_url)
        # Verify if element_name is a list
        # If it is a list, the attribute should be a list too. So, we'll browse them simultaneously
        if isinstance(element_name, list):  
            for index, element_on_page in enumerate(element_name):
                enum, tag = self._send_elements_info(element_on_page)
                try:
                    found_element = self.find_elements(enum, tag)
                    found_elements_text = []
                    for elem in found_element:
                        found_elements_text.append(elem.get_attribute(attribute[index]).encode("utf-8", "ignore").decode("utf-8").replace("\x1f", ""))

                    if found_elements_text != []:
                        concat_elem = " |_/- ".join(found_elements_text)
                        current_page_element.append(concat_elem)
                    else:
                        current_page_element.append("-")

                except Exception as e:
                    print(e)
                    current_page_element.append("-")
        
        # There is only one element (and so attribute) to get
        else:
            enum, tag = self._send_elements_info(element_on_page)
            try:
                current_page_element.append(self.find_element(enum, tag))
            except:
                current_page_element.append("-")
        self.dataset.variables['page_content'].append(current_page_element)


    def get_element_object(self, element_name):
        # TODO gerer element_name as list
        enum, tag = self._send_elements_info(element_name)
        try:
            self.elements_object = self.find_elements(enum, tag)
        except:
            pass


    def get_content_from_element_object(self, element_name, attribute):
        for object in self.elements_object:
            current_page_element = []
            # Verify if element_name is a list
            # If it is a list, the attribute should be a list too. So, we'll browse them simultaneously
            if isinstance(element_name, list):  
                for index, element_on_page in enumerate(element_name):
                    enum, tag = self._send_elements_info(element_on_page)
                    try:
                        found_element = object.find_elements(enum, "."+tag)
                        found_elements_text = []
                        for elem in found_element:
                            found_elements_text.append(elem.get_attribute(attribute[index]))
                        if found_elements_text:      
                            concat_elem = " |_/- ".join(found_elements_text)
                            current_page_element.append(concat_elem)
                        else:
                            current_page_element.append("-")

                    except Exception as e:
                        print(e)
                        current_page_element.append("-")
            
            # There is only one element (and so attribute) to get
            else:
                enum, tag = self._send_elements_info(element_on_page)
                try:
                    current_page_element.append(object.find_element(enum, tag))
                except:
                    current_page_element.append("-")
            self.dataset.variables["page_content"].append(current_page_element)
        # TODO A refaire
        self.elements_object = []



    """
    ------------- Aim --------------
    Scroll on page until an element is reached
    """
    def _scroll_on_page(self, element_name):
        # Scroll to the first element on the list of elements to scrap
        enum, tag = self._send_elements_info(element_name)
        els = self.find_elements(enum, tag)
        self.execute_script("arguments[0].scrollIntoView();", els[0])
        time.sleep(WAIT_S)
        current_view = 0

        # Scroll down on the page to let every element appear
        while current_view != len(els):
            els = self.find_elements(enum, tag)
            self.execute_script("arguments[0].scrollIntoView();", els[current_view])
            current_view += 1
            time.sleep(WAIT_XS)

    """
    ------------- Aim --------------
    Maps the name of a given element to its tag and 'By' enumeration

    ---------- Parameters ----------
    (TYPE)       | NAME          | DESCRIPTION
    (str)        | element_name  | Name of the element to be mapped

    ------------ Output ------------
    (TYPE)       | NAME   | DESCRIPTION
    (enum)       | enum   | 'By' enumeration of the given element
    (str)        | tag    | HTML tag of the given element
    """
    def _send_elements_info(self, element_name):
        tag  = self.page_elements[element_name]['tag']
        enum = self.my_by_dict[self.page_elements[element_name]['enum']]
        return enum, tag