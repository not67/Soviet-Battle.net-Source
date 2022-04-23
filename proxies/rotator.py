from threading import Lock


class ProxyRotator:
    proxies: list
    last_proxy_index: int

    @staticmethod
    def init(proxies: list):
        ProxyRotator.proxies = proxies
        ProxyRotator.last_proxy_index = 0
        ProxyRotator.l = Lock()

    @staticmethod
    def get():
        with ProxyRotator.l:
            # Get least accessed proxy
            ind = ProxyRotator.last_proxy_index + 1
            if ind >= len(ProxyRotator.proxies):
                ind = 0
            ProxyRotator.last_proxy_index = ind
            return ProxyRotator.proxies[ind]
