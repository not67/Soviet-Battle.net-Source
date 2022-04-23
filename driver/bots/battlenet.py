from apis.phone_numers import buy_number, get_code
from services.logger import logger
from db import save_account
from helpers.names import random_email, random_password
from names import get_first_name, get_full_name
from selenium.webdriver import Chrome
import functools
import sched
import time
from config import ACCOUNT_GENERATION_BASEURL, INI_CONFIG
from driver import Driver
from driver.session import DriverSession, DriverSessionStatus
from helpers.dates import random_birthdate
from enum import Enum

from utils.scheduler import setInterval

SELECTORS = {
    # Step one
    'country': '#capture-country',
    'birthdate_month': '.step__input--date--mm',
    'birthdate_year': '.step__input--date--yyyy',
    'birthdate_day': '.step__input--date--dd',

    "continue_button": "#flow-form-submit-btn",
    "back_button": "#flow-button-back",


    # Step two

    'f_name': '[name="first-name"]',
    'l_name': '[name="last-name"]',

    # Phone number validation

    "waiting_for_verification_code": "Enter the verification code sent to:",


    # IP Blocked text
    #"Please wait a moment and try again, we apologize for the inconvenience.",



    # Last step. Accept terms and conditions
    "TERMS_CONDITIONS_ONE": "#capture-opt-in-third-party-news-special-offers",
    "TERMS_CONDITIONS_TWO": '[data-capture-id="tou-agreements-implicit"]',

    # < input class = "step__checkbox" value = "41e60b3d-244d-4776-be75-e2c6b3eba9a3;187105" data-capture-id = "tou-agreements-implicit" name = "tou-agreements-implicit" type = "checkbox" >


    "PASSWORD": "#capture-password",

    # You're all set!
}


class BattlenetAccountCreatorStep(Enum):
    TRY_AGAIN = 'TRY_AGAIN'
    INSERT_COUNTRY_BIRTHDATE = 'INSERT_COUNTRY_BIRTHDATE'
    INSERT_FULL_NAME = 'INSERT_FULL_NAME'
    INSERT_EMAIL_PHONE_NUMBER = 'INSERT_EMAIL_PHONE_NUMBER'


MAX_PHONE_NUMBER_RETRIES = int(INI_CONFIG['MAX_PHONE_NUMBERS_RETRIES'])


class BattlenetAccountCreator(DriverSession):
    step: BattlenetAccountCreatorStep
    phone_numbers_retried: int
    current_phone_number_data: dict
    email: str
    password: str

    def __init__(self,):
        super().__init__()
        self.step = None
        self.phone_numbers_retried = 0

    def run(self):
        self.email = random_email()
        self.password = random_password()
        try:
            return self.step_one()
        except Exception as ex:
            try:
                self.driver.quit()
            except:
                pass
            raise ex

    def on_captcha_status_changed(self, is_present: bool):
        if is_present:
            self.driver.maximize_window()
        else:
            self.driver.minimize_window()

    def look_for_captchas(self, recurse=False):
        try:
            time.sleep(0.125)
            has_captcha = self.driver.execute_script(
                """let el = document.querySelector('[title="arkose-enforcement"]')
                if (el){
                    return el.style.width != '';
                }
                return false;
                """)
            if has_captcha:
                if not recurse:
                    logger.log('Session %s received CAPTCHA. Waiting to solve' %
                               self.session_id)
                    self.set_status(DriverSessionStatus.CAPTCHA_BLOCKED)
                self.look_for_captchas(recurse=True)
            else:
                if recurse:
                    self.set_status(DriverSessionStatus.INCOMPLETE)
                    logger.log('CAPTCHA SOLVED for Session %s' %
                               self.session_id)
                return

        except Exception as ex:
            pass

    def set_status(self, status: DriverSessionStatus):
        if status == DriverSessionStatus.CAPTCHA_BLOCKED:
            self.on_captcha_status_changed(True)
        else:
            if self.status == DriverSessionStatus.CAPTCHA_BLOCKED and self.status != status:
                self.on_captcha_status_changed(False)

        self.status = str(status)

        logger.log('Session %s status changed to %s' %
                   (self.session_id, self.status))
        # self.save_session()

    def set_step(self, step: BattlenetAccountCreatorStep):
        self.step = str(step)

    def driver_action(self, func, *args, **kwargs):
        self.look_for_captchas()
        return func(*args, **kwargs)

    def get_element(self, selector, timeout=10):
        tstart = int(time.time())
        while True:
            try:
                return self.driver_action(self.driver.find_element_by_css_selector, selector)
            except Exception as ex:
                pass
            time.sleep(0.125)
            if int(time.time()) - tstart > timeout:
                raise Exception('Timeout waiting for element %s' % selector)

    def get_element_by_text(self, text_str: str, typeof_el: str):
        js = """
        let isFound = false;
        [].slice.call(document.querySelectorAll(`%s`))
   .filter(a => a.textContent.match(`%s`))
   .forEach(a => {isFound = true;});return isFound;""" % (text_str, typeof_el)

        return self.driver.execute_script(js)

    def step_one(self):
        self.set_step(BattlenetAccountCreatorStep.INSERT_COUNTRY_BIRTHDATE)

        self.driver_action(self.driver.get, url=ACCOUNT_GENERATION_BASEURL)

        # Set country
        country_el = self.get_element(SELECTORS['country'])

        self.driver.set_element_value(
            country_el, INI_CONFIG['ACCOUNT_COUNTRY_CODE'])

        # Set birthdate
        fake_date = random_birthdate()
        # Day
        day_el = self.get_element(SELECTORS['birthdate_day'])

        self.driver.set_element_value(day_el, fake_date['day'])

        # Month
        month_el = self.get_element(SELECTORS['birthdate_month'])

        self.driver.set_element_value(month_el, fake_date['month'])

        # Year
        year_el = self.get_element(SELECTORS['birthdate_year'])
        self.driver.set_element_value(year_el, fake_date['year'])

        self.click_continue()

        return self.step_two()

    def click_continue(self):
        self.get_element(SELECTORS['continue_button']).click()
        time.sleep(2)

    def go_back(self):
        self.get_element(SELECTORS['back_button']).click()
        time.sleep(2)

    def step_two(self):
        self.set_step(BattlenetAccountCreatorStep.INSERT_FULL_NAME)
        # Fake name

        # Wait for name to show
        f_name_el = self.get_element(SELECTORS['f_name'])
        self.driver.set_element_value(f_name_el, get_first_name())

        l_name_el = self.get_element(SELECTORS['l_name'])
        self.driver.set_element_value(l_name_el, get_first_name())

        self.click_continue()

        return self.step_three()

    def step_three(self):
        if self.phone_numbers_retried >= MAX_PHONE_NUMBER_RETRIES:
            raise Exception('Max phone numbers retries reached')

        self.driver.set_element_value(
            self.get_element('#capture-email'),
            self.email
        )

        # Fields = field-0

        self.current_phone_number_data = buy_number()

        self.driver.set_element_value(
            self.get_element('#capture-phone-number'),
            self.current_phone_number_data['phone']
        )

        self.click_continue()
        return self.step_four()

    def step_four(self):
        # Seek for code validation
        code_received = False
        timeout = False
        tstart = int(time.time())
        while not code_received and not timeout:
            code = get_code(self.current_phone_number_data['id'])
            if code:
                code_received = True
            timeout = False if int(time.time()) - tstart < 120 else True
            time.sleep(5)

            if not code_received and timeout:
                if self.phone_numbers_retried >= MAX_PHONE_NUMBER_RETRIES:
                    raise Exception('Max phone numbers retries reached')
                self.go_back()
                return self.step_two()

        for i in range(6):
            phone_code_input_el = self.get_element('#field-%s' % str(i))
            phone_code_input_el.send_keys(code[i])
        self.click_continue()
        return self.step_five()

    def step_five(self):
        # Accept terms and conditions
        self.driver.set_element_value(self.get_element(
            '[name="tou-agreements-implicit"][type="checkbox"]'), 'true', checkbox=True)

        self.click_continue()

        return self.step_six()

    def step_six(self):
        # password

        self.driver.set_element_value(self.get_element(
            '[id="capture-password"]'), self.password)

        self.click_continue()
        return self.step_seven()

    def step_seven(self):
        # Set name
        # Just continue

        self.click_continue()

        time.sleep(3)

        self.driver.quit()

        return [
            self.email,
            self.current_phone_number_data['phone'],
            self.password
        ]
        # Now save account
