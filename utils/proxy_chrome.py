from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import zipfile
import os


def proxy_chrome(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
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
    from helpers.ostype import get


    PLUGIN_PATH = os.path.join( 'proxy_auth_plugin.zip')

    pluginfile = os.getcwd() + \
        r'\extension\proxy_auth_plugin.zip' if os.name == 'nt' else '/var/log/python/proxy_auth_plugin.zip'

    with open(pluginfile, 'w+') as zp:
        pass
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    # extension support is not possible in incognito mode for now
    # co.add_argument('--incognito')
    # co.add_argument('--disable-gpu')
    # disable infobars
    co.add_argument('--disable-infobars')
    co.add_argument('--no-sandbox')
    co.add_argument('--disable-dev-shm-usage')
    co.add_experimental_option("excludeSwitches", [
                               'enable-automation', 'enable-logging', "ignore-certificate-errors"])
    co.add_experimental_option('useAutomationExtension', False)
    # location of chromedriver, please change it according to your project.

    co.add_extension(pluginfile)
    #co.add_argument("--window-size=%s" % "1,1")
    driver = webdriver.Chrome(chrome_options=co)
    # return the driver with added proxy configuration.

    driver.__d
    return driver
