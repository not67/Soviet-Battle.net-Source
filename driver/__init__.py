from time import sleep
from typing import Any

import fake_useragent
from helpers.ostype import get_os
import os
import zipfile
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import gc
from config import INI_CONFIG, TMP_FOLDER
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
# from proxy_handler import ProxyHandler, Proxy
from selenium.webdriver.common.proxy import Proxy, ProxyType

from helpers.hash import md5


class Driver(webdriver.Chrome):

    def __init__(self, *args, **kwargs) -> None:
        if type(kwargs) != dict:
            kwargs = {}

        chrome_options = self.prepare_chrome_options(
            kwargs['PROXY_HOST'],
            kwargs['PROXY_PORT'],
            kwargs['PROXY_USER'],
            kwargs['PROXY_PASS'],
            kwargs['USER_AGENT'],
        )
        super().__init__(
            options=chrome_options
        )

        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
            "const newProto = navigator.__proto__;"
            "delete newProto.webdriver;"
            "navigator.__proto__ = newProto;"
        })

    def __del__(self) -> None:
        # Force quit
        pass

    def set_element_value(self, el, value: str, send_keys: bool = False, checkbox=False):

        try:
            el.click()
        except:
            pass

        if send_keys:
            el.send_keys(value)
        elif checkbox:
            self.execute_script(
                "arguments[0].checked = %s" % str(value).lower(), el)
        else:
            # el.send_keys(value)
            self.execute_script(
                "arguments[0].value = `%s`" % value, el)

        sleep(1)

    def finish():
        print('Ending browser')
        gc.collect()
        return super().quit()

    def prepare_chrome_options(
        self,
        PROXY_HOST: str,
        PROXY_PORT: int,
        PROXY_USER: str,
        PROXY_PASS: str,
        USER_AGENT: str
    ):
        manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%(host)s",
                    port: parseInt(%(port)s)
                },
                bypassList: ["foobar.com"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%(user)s",
                    password: "%(pass)s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
            """ % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }

        # Generate filename by hashing with md5 all proxy arguments
        PLUGIN_PATH = os.path.join(
            TMP_FOLDER,
            'proxy_auth_plugin_%s.zip' % md5(
                PROXY_HOST + str(PROXY_PORT) + PROXY_USER + PROXY_PASS
            )
        )

        with open(PLUGIN_PATH, 'w+') as zp:
            pass

        with zipfile.ZipFile(PLUGIN_PATH, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        co = Options()
        # co = webdriver.ChromeOptions()
        # extension support is not possible in incognito mode for now
        # co.add_argument('--incognito')
        # co.add_argument('--disable-gpu')
        # disable infobars
        co.add_argument('--disable-infobars')
        # co.add_argument('--window-size=0,0')
        co.add_argument('--no-sandbox')
        UA = USER_AGENT
        co.add_argument(f'user-agent={UA}')
        co.add_argument('--disable-dev-shm-usage')
        co.add_experimental_option("excludeSwitches", [
            'enable-automation', 'enable-logging', "ignore-certificate-errors"])
        co.add_experimental_option('useAutomationExtension', False)
        # location of chromedriver, please change it according to your project.
        if INI_CONFIG['ENABLE_WEBSHARE_PROXY']:
            co.add_extension(PLUGIN_PATH)
        # co.add_argument("--window-size=%s" % "1,1")
        return co
