from config import INI_CONFIG
import json


def get():
    import requests

    response = requests.get("https://proxy.webshare.io/api/proxy/list/?page=1&countries=US-FR",
                            headers={"Authorization": "Token %s" % INI_CONFIG.get("WEBSHARE_API_KEY", "")})

    js = json.loads(response.text)
    proxies = []
    for proxy in js['results']:
        proxies.append(
            {
                "PROXY_HOST": proxy["proxy_address"],
                "PROXY_PORT": proxy["ports"]['http'],
                "PROXY_USER": proxy["username"],
                "PROXY_PASS": proxy["password"]
            }
        )
    return proxies
