import time
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import scrap_params


class Boat:
    def __init__(self, name, imo):
        self.name = name
        self.imo = imo
        self.data_dict = {}
        self.data = {}
        self.photo = ''
        self.link = ''

    @staticmethod
    def save_data(boat):
        with open(scrap_params.scrap_results, 'a') as save:
            # save.writelines('{"Generic":' + json.dumps(self.data)+'}\n')
            # save.writelines('{{"Generic":' + json.dumps(boat.data)+'}, {"Link": "'+boat.link+'"}\n')
            boat.data_dict["Generic"] = boat.data
            boat.data_dict["Link"] = boat.link
            boat.data_dict["Photo"] = boat.photo
            save.writelines(json.dumps(boat.data_dict)+'\n')


class ScrapBot:
    def __init__(self):
        self.login = scrap_params.credentials[0]
        self.passcode = scrap_params.credentials[1]
        self.url = 'https://www.fleetmon.com/'

    def run_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)

    def find_boat_data(self, boat_name):
        boat = Boat(boat_name, self.boats[boat_name])
        print(boat.name, boat.imo, end='')
        try:
            search_input = self.browser.find_element_by_id('main-search-input')
            search_input.send_keys(boat.imo)
            time.sleep(1)
            xpath = f"//a[contains(text(),'{boat_name}')]"
            link = self.browser.find_element_by_xpath(xpath)
            boat.link = link.get_attribute('href')
            link.click()
            try:
                photo = self.browser.find_element_by_css_selector('#vessel-master-photo img.uk-cover')
                boat.photo = photo.get_attribute('src')
            except NoSuchElementException:
                boat.photo = None
            self.browser.find_element_by_css_selector('#general-vessel-info-footer a.btn-default').click()
            time.sleep(1)
            # find and save global data
            data = self.browser.find_elements_by_css_selector('.uk-first-column table tr td')
            for j in data:
                params_list = str(j.text).split('\n')
                if len(params_list) > 1:
                    parameter = params_list[1]
                    if parameter == '—':
                        parameter = None
                    boat.data[params_list[0]] = parameter
            boat.save_data(boat)
            print(' - Ok')

            self.browser.find_element_by_id('vessel-port-search-access').click()
            self.browser.find_element_by_id('main-search-input').clear()
            time.sleep(1)
        except NoSuchElementException:
            self.browser.find_element_by_id('main-search-input').clear()

    def scrap_boats(self):
        self.boats = bot.load_bots_list()
        print(f'Total boats in list {len(self.boats)}')
        try:
            last_record = bot.get_last_record()
            last_imo = last_record['Generic']["IMO"]
            last_name = last_record['Generic']["Name"]
            print(f'Last parsed record IMO: {last_imo} Name: {last_name}')
        except FileNotFoundError:
            last_imo = ''
            print('No previous results found')
        try:
            self.run_browser()
            self.browser.maximize_window()
            self.browser.get(self.url)
            self.browser.find_element_by_css_selector('.uk-navbar-right a[href="#modalLoginRegister"]').click()
            self.browser.find_element_by_name('username').send_keys(self.login)
            self.browser.find_element_by_name('password').send_keys(self.passcode)
            time.sleep(1)
            self.browser.find_element_by_id('button-sign-in').click()
            time.sleep(1)
            self.browser.find_element_by_id('vessel-port-search-access').click()
            for i in self.boats:
                if last_imo == '':
                    # print(i, self.boats[i])
                    self.find_boat_data(i)
                elif self.boats[i] == last_imo:
                    last_imo = ''
        finally:
            # time.sleep(3)
            self.browser.quit()

    @staticmethod
    def load_bots_list():
        boats_list = {}
        with open(scrap_params.boats_list, 'r') as file:
            for _line in file.readlines():
                vessel = _line.split(' ')
                if len(vessel) > 1:
                    name = ' '.join(vessel[1:len(vessel) - 2])
                    boats_list[name] = vessel[-2]
        return boats_list

    @staticmethod
    def get_last_record():
        with open(scrap_params.scrap_results, 'r') as file:
            lines = file.readlines()
        print(f'Records parsed earlier: {len(lines)} records')
        return json.loads(lines[-1])


if __name__ == '__main__':
    bot = ScrapBot()
    start_time = time.time()
    bot.scrap_boats()
    process_time = time.time() - start_time
    print(f'Process took {process_time} seconds')