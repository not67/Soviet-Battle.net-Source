from services.logger import logger
from enum import Enum
import json
import os

import fake_useragent
from config import TMP_FOLDER
from helpers.ostype import get_os
from proxies.rotator import ProxyRotator
from driver import Driver
from proxies.providers.webshare import get as get_proxy_list
import uuid
from db import save_session as save_session_db
import pickle


ProxyRotator.init(
    get_proxy_list()
)


class DriverSessionStatus(Enum):
    INCOMPLETE = 'INCOMPLETE'
    CAPTCHA_BLOCKED = 'CAPTCHA_BLOCKED'
    COMPLETED = 'COMPLETED'


class DriverSession:
    session_id: str
    # Initiate an account generation session
    proxy: dict
    driver: Driver
    step: int
    user_agent: str
    status: DriverSessionStatus
    status_history: list

    def set_status(self, status: DriverSessionStatus):
        # self.status_history.append(status)
        self.status = status
        logger.log('Session %s status changed to %s' %
                   (self.session_id, self.status))
        self.save_session()

    def __init__(self, **stored_session) -> None:
        #self.status = DriverSessionStatus.INCOMPLETE

        if stored_session:
            pass
            # self.session_id = stored_session['id']
            # self.proxy = json.loads(stored_session['proxy'])
            # self.step = stored_session['step']
            # self.status = stored_session['status']
            # self.user_agent = stored_session['user_agent']
            # cookies = pickle.loads(stored_session['cookies'])

            # self.driver = Driver(**{
            #     **self.proxy,
            #     "USER_AGENT": self.user_agent
            # })
            # for cookie in cookies:
            #     self.driver.add_cookie(cookie)
            # return
        self.user_agent = fake_useragent.UserAgent().random
        self.session_id = str(uuid.uuid4())
        # Retrieve proxy
        self.proxy = ProxyRotator.get()

        self.driver = Driver(**{
            **self.proxy,
            'USER_AGENT': self.user_agent
        })
        # Spawn chromedriver browser
        logger.log('Created session %s with proxy %s' %
                   (self.session_id, repr(self.proxy)))

    def save_session(self):
        save_session_db(self)

    @staticmethod
    def from_stored_session(sess):
        return DriverSession(
            sess
        )
